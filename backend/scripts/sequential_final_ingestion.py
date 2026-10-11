"""
Sequential ingestion for final 5 catalogues with per-document reconciliation.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

from app.core.config import settings
from app.core.database import Base, async_session_factory
from app.models.rag_document import RagDocument, RagIngestionRun
from app.rag.ingestion.pdf_parser import extract_pages
from app.rag.ingestion.new_chunker import chunk_catalogue
from app.rag.ingestion.metadata_builder import build_catalogue_metadata
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.product_identity import get_canonical_slug
from app.rag.utils.ids import generate_document_id
from app.rag.config import rag_settings
from sqlalchemy import select, func

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATALOGUE_DIR = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues")
QDRANT_URL = getattr(settings, 'QDRANT_URL', '') or rag_settings.QDRANT_URL
QDRANT_API_KEY = getattr(settings, 'QDRANT_API_KEY', '') or rag_settings.QDRANT_API_KEY
QDRANT_COLLECTION = rag_settings.QDRANT_COLLECTION_NAME

# Ingestion order as specified
INGESTION_ORDER = [
    ("dragon.pdf", "dragon"),
    ("polyurea.pdf", "polyurea"),
    ("TUBE VARNISH COATING SYSTEM.pdf", "tube-varnish-coating-system"),
    ("VRC MIX (LOW - MEDIUM) PRESSURE.pdf", "vrc-mix-low-medium-pressure"),
    ("Barrel Pump.pdf", "barrel-pump"),
]

def calculate_sha256(file_path: Path) -> str:
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


async def get_qdrant_point_count() -> int:
    from qdrant_client import QdrantClient
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)
    count = client.count(collection_name=QDRANT_COLLECTION).count
    return count


async def get_postgres_counts():
    async with async_session_factory() as db:
        doc_result = await db.execute(select(func.count(RagDocument.id)))
        doc_count = doc_result.scalar_one() or 0
        run_result = await db.execute(select(func.count(RagIngestionRun.id)))
        run_count = run_result.scalar_one() or 0
        return doc_count, run_count


async def ingest_document(file_path: Path, product_slug: str, qdrant_before: int, docs_before: int, runs_before: int) -> dict:
    document_name = file_path.name
    sha256 = calculate_sha256(file_path)

    async with async_session_factory() as db:
        existing = await db.execute(
            select(RagDocument).where(RagDocument.document_name == document_name)
        )
        existing_doc = existing.scalar_one_or_none()

        if existing_doc and existing_doc.sha256 == sha256:
            logger.info(f"Skipping {document_name}: unchanged")
            return {"status": "skipped", "reason": "unchanged", "qdrant_before": qdrant_before, "qdrant_after": qdrant_before}

        if existing_doc:
            document_id = existing_doc.qdrant_document_id or generate_document_id()
        else:
            document_id = generate_document_id()
            existing_doc = RagDocument(
                document_name=document_name,
                source_type="catalogue",
                storage_path=str(file_path),
                sha256=sha256,
                status="processing",
                qdrant_document_id=document_id,
                product_slug=product_slug,
            )
            db.add(existing_doc)
            await db.flush()

        run = RagIngestionRun(
            document_id=existing_doc.id,
            document_name=document_name,
            source_type="catalogue",
            status="started",
        )
        db.add(run)
        await db.flush()

        try:
            pages, ocr_results = extract_pages(str(file_path), enable_ocr=True)
            tables = []
            if not pages:
                raise ValueError("No pages extracted")
            chunks = chunk_catalogue(document_name, pages, tables, product_slug, document_id, ocr_results=ocr_results)
            if not chunks:
                raise ValueError("No chunks generated")

            logger.info(f"Generated {len(chunks)} chunks for {document_name}")

            dense = DenseEmbeddingService()
            sparse = SparseEmbeddingService()

            texts = [c["text"] for c in chunks]
            dense_vectors = dense.embed_documents(texts)
            sparse_vectors = sparse.embed_documents(texts)

            qdrant_store = QdrantStore()
            if existing_doc.qdrant_document_id:
                await qdrant_store.delete_by_document_id(document_id)

            payloads = []
            for idx, chunk in enumerate(chunks):
                metadata = build_catalogue_metadata(document_id, document_name, str(file_path), sha256, product_slug, chunk)
                payloads.append(metadata)

            logger.info(f"Uploading {len(payloads)} points to Qdrant for {document_name}...")
            await qdrant_store.upsert_points(
                document_id=document_id,
                dense_vectors=dense_vectors,
                sparse_vectors=sparse_vectors,
                payloads=payloads,
            )

            existing_doc.sha256 = sha256
            existing_doc.qdrant_document_id = document_id
            existing_doc.chunk_count = len(chunks)
            existing_doc.status = "indexed"
            existing_doc.last_ingested_at = datetime.now(timezone.utc)
            run.status = "indexed"
            run.chunks_created = len(chunks)
            await db.commit()

            qdrant_after = await get_qdrant_point_count()
            docs_after, runs_after = await get_postgres_counts()
            
            logger.info(f"Successfully indexed {document_name}: {len(chunks)} chunks")
            return {
                "status": "indexed",
                "document_name": document_name,
                "product_slug": product_slug,
                "sha256": sha256,
                "chunks": len(chunks),
                "qdrant_before": qdrant_before,
                "qdrant_after": qdrant_after,
                "expected_delta": len(chunks),
                "actual_delta": qdrant_after - qdrant_before,
                "docs_before": docs_before,
                "docs_after": docs_after,
                "runs_before": runs_before,
                "runs_after": runs_after,
            }
        except Exception as exc:
            existing_doc.status = "failed"
            existing_doc.last_error = str(exc)
            run.status = "failed"
            run.error = str(exc)
            await db.commit()
            logger.exception(f"Failed to ingest {document_name}: {exc}")
            return {"status": "failed", "document_name": document_name, "error": str(exc)}


async def main() -> None:
    logger.info("=" * 60)
    logger.info("FINAL CATALOGUE INTEGRATION - PHASE 9C.7")
    logger.info("Sequential Ingestion of Final 5 PDFs")
    logger.info("=" * 60)
    logger.info(f"Qdrant URL: {QDRANT_URL}")
    logger.info(f"Qdrant collection: {QDRANT_COLLECTION}")

    # Initial baseline
    qdrant_initial = await get_qdrant_point_count()
    docs_initial, runs_initial = await get_postgres_counts()
    logger.info(f"BASELINE: Qdrant={qdrant_initial}, PostgreSQL docs={docs_initial}, runs={runs_initial}")

    results = {}
    qdrant_before = qdrant_initial
    docs_before = docs_initial
    runs_before = runs_initial

    for doc_name, product_slug in INGESTION_ORDER:
        file_path = CATALOGUE_DIR / doc_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            results[doc_name] = {"status": "not_found"}
            continue
        
        logger.info(f"\n{'='*60}")
        logger.info(f"INGESTING: {doc_name} -> {product_slug}")
        logger.info(f"{'='*60}")
        
        result = await ingest_document(file_path, product_slug, qdrant_before, docs_before, runs_before)
        results[doc_name] = result
        
        # Update baseline for next document
        if result.get("status") == "indexed":
            qdrant_before = result["qdrant_after"]
            docs_before = result["docs_after"]
            runs_before = result["runs_after"]
            logger.info(f"  Qdrant: {result['qdrant_before']} -> {result['qdrant_after']} (delta: {result['actual_delta']}, expected: {result['expected_delta']})")
            logger.info(f"  PostgreSQL docs: {result['docs_before']} -> {result['docs_after']}")
            logger.info(f"  PostgreSQL runs: {result['runs_before']} -> {result['runs_after']}")
        elif result.get("status") == "skipped":
            logger.info(f"  SKIPPED: {result['reason']}")
        
        # Small delay between documents
        await asyncio.sleep(1)

    # Final reconciliation
    qdrant_final = await get_qdrant_point_count()
    docs_final, runs_final = await get_postgres_counts()
    
    logger.info(f"\n{'='*60}")
    logger.info("FINAL RECONCILIATION")
    logger.info(f"{'='*60}")
    logger.info(f"Initial Qdrant: {qdrant_initial}")
    logger.info(f"Final Qdrant: {qdrant_final}")
    logger.info(f"Total Qdrant delta: {qdrant_final - qdrant_initial}")
    logger.info(f"Initial PostgreSQL docs: {docs_initial}")
    logger.info(f"Final PostgreSQL docs: {docs_final}")
    logger.info(f"Initial PostgreSQL runs: {runs_initial}")
    logger.info(f"Final PostgreSQL runs: {runs_final}")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "baseline": {
            "qdrant_initial": qdrant_initial,
            "postgres_docs_initial": docs_initial,
            "postgres_runs_initial": runs_initial,
        },
        "final": {
            "qdrant_final": qdrant_final,
            "postgres_docs_final": docs_final,
            "postgres_runs_final": runs_final,
        },
        "results": results,
        "ingestion_order": [d[0] for d in INGESTION_ORDER],
    }
    report_path = Path("/home/vr-coatings/Desktop/website_V2/backend/rag_debug/final_ingestion_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    logger.info(f"Report saved to {report_path}")


if __name__ == "__main__":
    asyncio.run(main())