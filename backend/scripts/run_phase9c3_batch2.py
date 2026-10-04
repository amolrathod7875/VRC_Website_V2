"""
Phase 9C.3 — Batch 2 Chunking Remediation Ingestion

Ingests approved P2 catalogues:
1. Paint Preparation Unit.pdf -> canonical slug: paint-preparation-unit
2. PORTABLE PRESSURE FEED POT.pdf -> canonical slug: portable-pressure-feed-pot
3. turbine.pdf -> canonical slug: turbine
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

# Canonical slugs for approved documents
APPROVED_DOCS = {
    "Paint Preparation Unit.pdf": "paint-preparation-unit",
    "PORTABLE PRESSURE FEED POT.pdf": "portable-pressure-feed-pot",
    "turbine.pdf": "turbine",
}

STILL_REVIEW_REQUIRED = set()


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


async def get_postgres_counts() -> tuple[int, int]:
    async with async_session_factory() as db:
        doc_result = await db.execute(select(func.count(RagDocument.id)))
        doc_count = doc_result.scalar_one() or 0
        run_result = await db.execute(select(func.count(RagIngestionRun.id)))
        run_count = run_result.scalar_one() or 0
        return doc_count, run_count


async def ingest_document(file_path: Path, product_slug: str) -> dict:
    document_name = file_path.name
    sha256 = calculate_sha256(file_path)

    async with async_session_factory() as db:
        existing = await db.execute(
            select(RagDocument).where(RagDocument.document_name == document_name)
        )
        existing_doc = existing.scalar_one_or_none()

        if existing_doc and existing_doc.sha256 == sha256:
            logger.info(f"Skipping {document_name}: unchanged")
            return {"status": "skipped", "reason": "unchanged"}

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

            # Initialize services
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
            logger.info(f"Successfully indexed {document_name}: {len(chunks)} chunks")
            return {"status": "indexed", "document_name": document_name, "chunks": len(chunks)}
        except Exception as exc:
            existing_doc.status = "failed"
            existing_doc.last_error = str(exc)
            run.status = "failed"
            run.error = str(exc)
            await db.commit()
            logger.exception(f"Failed to ingest {document_name}: {exc}")
            return {"status": "failed", "document_name": document_name, "error": str(exc)}


async def main() -> None:
    logger.info("Phase 9C.3 Batch 2 Ingestion")
    logger.info(f"Qdrant URL: {QDRANT_URL}")
    logger.info(f"Qdrant collection: {QDRANT_COLLECTION}")

    # Record initial state
    qdrant_before = await get_qdrant_point_count()
    docs_before, runs_before = await get_postgres_counts()
    logger.info(f"Initial state: Qdrant={qdrant_before}, PostgreSQL docs={docs_before}, runs={runs_before}")

    results = {}
    for doc_name, product_slug in APPROVED_DOCS.items():
        file_path = CATALOGUE_DIR / doc_name
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            results[doc_name] = {"status": "not_found"}
            continue
        logger.info(f"Ingesting {doc_name} -> {product_slug}")
        result = await ingest_document(file_path, product_slug)
        results[doc_name] = result

    # Record final state
    qdrant_after = await get_qdrant_point_count()
    docs_after, runs_after = await get_postgres_counts()
    logger.info(f"Final state: Qdrant={qdrant_after}, PostgreSQL docs={docs_after}, runs={runs_after}")

    # Print summary
    logger.info("=" * 60)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 60)
    for doc_name, result in results.items():
        logger.info(f"{doc_name}: {result}")
    logger.info(f"Qdrant delta: {qdrant_after - qdrant_before}")
    logger.info(f"PostgreSQL docs delta: {docs_after - docs_before}")
    logger.info(f"PostgreSQL runs delta: {runs_after - runs_before}")

    # Save report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "qdrant_before": qdrant_before,
        "qdrant_after": qdrant_after,
        "qdrant_delta": qdrant_after - qdrant_before,
        "postgres_docs_before": docs_before,
        "postgres_docs_after": docs_after,
        "postgres_runs_before": runs_before,
        "postgres_runs_after": runs_after,
        "results": results,
        "approved_docs": APPROVED_DOCS,
        "still_review_required": list(STILL_REVIEW_REQUIRED),
    }
    report_path = Path("/home/vr-coatings/Desktop/website_V2/backend/rag_debug/phase9c3_batch2_ingestion_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Report saved to {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
