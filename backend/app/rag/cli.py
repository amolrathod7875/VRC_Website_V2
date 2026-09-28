import argparse
import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.database import Base
from app.rag.ingestion.ingestion_service import IngestionService
from app.rag.ingestion.pdf_parser import extract_pages, page_needs_ocr
from app.rag.ingestion.pdf_table_parser import extract_tables
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.company_parser import parse_company_text
from app.rag.ingestion.company_chunker import chunk_company_sections
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings

logger = logging.getLogger(__name__)


def get_session() -> AsyncSession:
    engine = create_async_engine(rag_settings.database_url(), echo=False, future=True)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session_factory()


def _write_debug_file(path: str, payload: Any) -> None:
    debug_path = Path(path)
    if not debug_path.is_absolute():
        debug_path = Path.cwd() / debug_path
    debug_path.parent.mkdir(parents=True, exist_ok=True)
    debug_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


async def _ingest_catalogue(file_path: str) -> None:
    async with get_session() as db:
        qdrant = QdrantStore()
        try:
            await qdrant.ensure_collection()
        except RuntimeError as exc:
            logger.error("Qdrant unavailable: %s", exc)
            print(f"Qdrant unavailable: {exc}")
            return
        service = IngestionService(db=db, qdrant_store=qdrant, dense=DenseEmbeddingService(), sparse=SparseEmbeddingService())
        result = await service.ingest_catalogue(Path(file_path))
        logger.info(result)
        print(result)


async def _ingest_company(file_path: str) -> None:
    async with get_session() as db:
        qdrant = QdrantStore()
        try:
            await qdrant.ensure_collection()
        except RuntimeError as exc:
            logger.error("Qdrant unavailable: %s", exc)
            print(f"Qdrant unavailable: {exc}")
            return
        service = IngestionService(db=db, qdrant_store=qdrant, dense=DenseEmbeddingService(), sparse=SparseEmbeddingService())
        result = await service.ingest_company(Path(file_path))
        logger.info(result)
        print(result)


async def _inspect_catalogue(file_path: str) -> None:
    pages = extract_pages(file_path)
    tables = extract_tables(file_path)
    document_id = "inspect-dry-run"
    product_slug = Path(file_path).stem.lower().replace(" ", "_")
    chunks = chunk_catalogue(Path(file_path).name, pages, tables, product_slug, document_id)
    report = {
        "document": Path(file_path).name,
        "pages": len(pages),
        "tables_detected": len(tables),
        "ocr_required_pages": [p["page_number"] for p in pages if page_needs_ocr(p["text"])],
        "chunks": len(chunks),
        "chunk_types": _count_chunk_types(chunks),
        "chunk_preview": [_chunk_preview(chunk) for chunk in chunks[:20]],
        "warnings": [],
    }
    _write_debug_file("rag_debug/Tiger_chunks.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


async def _inspect_company(file_path: str) -> None:
    text = Path(file_path).read_text(encoding="utf-8")
    sections = parse_company_text(text)
    document_id = "inspect-company-dry-run"
    chunks = chunk_company_sections(sections, document_id)
    report = {
        "document": Path(file_path).name,
        "total_lines": len(text.splitlines()),
        "sections": len(sections),
        "chunks": len(chunks),
        "section_titles": [s.get("section_title") for s in sections],
        "chunk_preview": [_chunk_preview(chunk) for chunk in chunks[:20]],
    }
    _write_debug_file("rag_debug/company_master_chunks.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def _chunk_preview(chunk: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "chunk_id": chunk.get("chunk_id"),
        "source_type": chunk.get("source_type"),
        "section": chunk.get("section"),
        "content_type": chunk.get("content_type"),
        "product": chunk.get("product"),
        "product_slug": chunk.get("product_slug"),
        "model": chunk.get("model"),
        "page_number": chunk.get("page_number"),
        "line_start": chunk.get("line_start"),
        "line_end": chunk.get("line_end"),
        "authority_priority": chunk.get("authority_priority"),
        "text_preview": (chunk.get("text", "")[:300]).replace("\n", " "),
    }


def _count_chunk_types(chunks: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for chunk in chunks:
        key = chunk.get("section") or chunk.get("content_type") or "other"
        counts[key] = counts.get(key, 0) + 1
    return counts


async def _search(query: str) -> None:
    async with get_session() as db:
        qdrant = QdrantStore()
        try:
            await qdrant.ensure_collection()
        except RuntimeError as exc:
            logger.error("Qdrant unavailable: %s", exc)
            print(f"Qdrant unavailable: {exc}")
            return
        retriever = HybridRetriever(qdrant_store=qdrant)
        dense = DenseEmbeddingService()
        dense_query = dense.embed_query(query)
        sparse_query = SparseEmbeddingService().embed_query(query)
        chunks = await retriever.retrieve(dense_query=dense_query, sparse_query=sparse_query, filters=None)
        for idx, chunk in enumerate(chunks, start=1):
            print(f"RANK {idx}: score={chunk.get('score')}")
            print(f"  document={chunk.get('document_name')} product={chunk.get('product')} section={chunk.get('section')} model={chunk.get('model')} page={chunk.get('page_number')} authority={chunk.get('authority_priority')}")
            print(f"  text={(chunk.get('text','')[:300]).replace(chr(10), ' ')}")
            print("")


def main() -> None:
    parser = argparse.ArgumentParser(description="VR Coatings RAG ingestion CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ingest-all", help="Ingest catalogues and company master")

    catalogue_parser = subparsers.add_parser("ingest-catalogues", help="Ingest all catalogues")
    catalogue_parser.add_argument("path", nargs="?", default=rag_settings.RAG_CATALOGUE_ROOT)

    company_parser = subparsers.add_parser("ingest-company", help="Ingest company master")
    company_parser.add_argument("path", nargs="?", default=rag_settings.RAG_COMPANY_KB_PATH)

    file_parser = subparsers.add_parser("ingest-file", help="Ingest a single file")
    file_parser.add_argument("path", help="Path to PDF or TXT file")

    inspect_parser = subparsers.add_parser("inspect-file", help="Inspect parsing without indexing")
    inspect_parser.add_argument("path", help="Path to PDF or TXT file")

    subparsers.add_parser("status", help="Show ingestion status")

    search_parser = subparsers.add_parser("search", help="Retrieval-only search")
    search_parser.add_argument("query", help="Search query")

    args = parser.parse_args()
    if args.command == "ingest-all":
        asyncio.run(_ingest_catalogue(rag_settings.RAG_CATALOGUE_ROOT))
        asyncio.run(_ingest_company(rag_settings.RAG_COMPANY_KB_PATH))
    elif args.command == "ingest-catalogues":
        asyncio.run(_ingest_catalogue(args.path))
    elif args.command == "ingest-company":
        asyncio.run(_ingest_company(args.path))
    elif args.command == "ingest-file":
        path = Path(args.path)
        if path.suffix.lower() == ".pdf":
            asyncio.run(_ingest_catalogue(args.path))
        else:
            asyncio.run(_ingest_company(args.path))
    elif args.command == "inspect-file":
        path = Path(args.path)
        if path.suffix.lower() == ".pdf":
            asyncio.run(_inspect_catalogue(args.path))
        else:
            asyncio.run(_inspect_company(args.path))
    elif args.command == "search":
        asyncio.run(_search(args.query))
    elif args.command == "status":
        print("Status command not implemented in CLI yet.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
