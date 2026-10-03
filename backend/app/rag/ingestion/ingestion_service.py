import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import Base
from app.models.rag_document import RagDocument, RagIngestionRun
from app.rag.utils.hashing import calculate_sha256
from app.rag.utils.ids import generate_document_id
from app.rag.ingestion.pdf_parser import extract_pages, page_needs_ocr
from app.rag.ingestion.pdf_table_parser import extract_tables
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.company_parser import parse_company_text
from app.rag.ingestion.company_chunker import chunk_company_sections
from app.rag.ingestion.metadata_builder import build_catalogue_metadata, build_company_metadata
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.config import rag_settings
from app.rag.constants import (
    SOURCE_TYPE_CATALOGUE,
    SOURCE_TYPE_COMPANY_MASTER,
    STATUS_INDEXED,
    STATUS_FAILED,
    STATUS_PROCESSING,
)
from app.rag.product_identity import get_canonical_slug

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(
        self,
        db: AsyncSession,
        qdrant_store: QdrantStore,
        dense: DenseEmbeddingService,
        sparse: SparseEmbeddingService,
    ) -> None:
        self.db = db
        self.qdrant_store = qdrant_store
        self.dense = dense
        self.sparse = sparse

    async def _get_document(self, document_name: str) -> Optional[RagDocument]:
        result = await self.db.execute(select(RagDocument).where(RagDocument.document_name == document_name))
        return result.scalar_one_or_none()

    async def ingest_catalogue(self, file_path: Path) -> Dict[str, Any]:
        document_name = file_path.name
        sha256 = calculate_sha256(file_path)
        existing = await self._get_document(document_name)
        if existing and existing.sha256 == sha256:
            return {"status": "skipped", "document_name": document_name, "reason": "unchanged"}

        if existing:
            document_id = existing.qdrant_document_id or generate_document_id()
        else:
            document_id = generate_document_id()
            existing = RagDocument(
                document_name=document_name,
                source_type=SOURCE_TYPE_CATALOGUE,
                storage_path=str(file_path),
                sha256=sha256,
                status=STATUS_PROCESSING,
                qdrant_document_id=document_id,
            )
            self.db.add(existing)
            await self.db.flush()

        run = RagIngestionRun(
            document_id=existing.id,
            document_name=document_name,
            source_type=SOURCE_TYPE_CATALOGUE,
            status="started",
        )
        self.db.add(run)
        await self.db.flush()

        try:
            pages, ocr_results = extract_pages(str(file_path), enable_ocr=True)
            tables = extract_tables(str(file_path))
            if not pages:
                raise ValueError("No pages extracted")
            product_slug = get_canonical_slug(document_name) or document_name.lower().replace(" ", "_").replace(".pdf", "")
            chunks = chunk_catalogue(document_name, pages, tables, product_slug, document_id, ocr_results=ocr_results)
            if not chunks:
                raise ValueError("No chunks generated")

            texts = [c["text"] for c in chunks]
            print(f"Embedding {len(texts)} catalogue chunks...")
            dense_vectors = self.dense.embed_documents(texts)
            sparse_vectors = self.sparse.embed_documents(texts)

            if existing.qdrant_document_id:
                await self.qdrant_store.delete_by_document_id(document_id)

            payloads = []
            for idx, chunk in enumerate(chunks):
                metadata = build_catalogue_metadata(document_id, document_name, str(file_path), sha256, product_slug, chunk)
                payloads.append(metadata)

            print(f"Uploading {len(payloads)} points to Qdrant...")
            await self.qdrant_store.upsert_points(
                document_id=document_id,
                dense_vectors=dense_vectors,
                sparse_vectors=sparse_vectors,
                payloads=payloads,
            )

            existing.sha256 = sha256
            existing.qdrant_document_id = document_id
            existing.chunk_count = len(chunks)
            existing.status = STATUS_INDEXED
            existing.last_ingested_at = existing.updated_at
            run.status = STATUS_INDEXED
            run.chunks_created = len(chunks)
            await self.db.commit()
            return {"status": "indexed", "document_name": document_name, "chunks": len(chunks)}
        except Exception as exc:
            existing.status = STATUS_FAILED
            existing.last_error = str(exc)
            run.status = STATUS_FAILED
            run.error = str(exc)
            await self.db.commit()
            logger.exception("Failed to ingest catalogue %s", document_name)
            return {"status": "failed", "document_name": document_name, "error": str(exc)}

    async def ingest_company(self, file_path: Path) -> Dict[str, Any]:
        document_name = file_path.name
        sha256 = calculate_sha256(file_path)
        existing = await self._get_document(document_name)
        if existing and existing.sha256 == sha256:
            return {"status": "skipped", "document_name": document_name, "reason": "unchanged"}

        if existing:
            document_id = existing.qdrant_document_id or generate_document_id()
        else:
            document_id = generate_document_id()
            existing = RagDocument(
                document_name=document_name,
                source_type=SOURCE_TYPE_COMPANY_MASTER,
                storage_path=str(file_path),
                sha256=sha256,
                status=STATUS_PROCESSING,
                qdrant_document_id=document_id,
            )
            self.db.add(existing)
            await self.db.flush()

        run = RagIngestionRun(
            document_id=existing.id,
            document_name=document_name,
            source_type=SOURCE_TYPE_COMPANY_MASTER,
            status="started",
        )
        self.db.add(run)
        await self.db.flush()

        try:
            text = file_path.read_text(encoding="utf-8")
            sections = parse_company_text(text)
            chunks = chunk_company_sections(sections, document_id)
            if not chunks:
                raise ValueError("No chunks generated")

            total = len(chunks)
            print(f"Parsed {len(sections)} sections, {total} company chunks")

            texts = [c["text"] for c in chunks]
            dense_vectors = []
            sparse_vectors = []
            batch_size = max(1, rag_settings.RAG_EMBED_BATCH_SIZE)
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                print(f"Embedding company chunks: {end} / {total}")
                batch_texts = texts[start:end]
                dense_vectors.extend(self.dense.embed_documents(batch_texts))
                sparse_vectors.extend(self.sparse.embed_documents(batch_texts))

            if existing.qdrant_document_id:
                await self.qdrant_store.delete_by_document_id(document_id)

            payloads = []
            for chunk in chunks:
                metadata = build_company_metadata(document_id, document_name, str(file_path), sha256, chunk)
                payloads.append(metadata)

            qdrant_batch = max(1, rag_settings.RAG_QDRANT_UPSERT_BATCH_SIZE)
            for start in range(0, len(payloads), qdrant_batch):
                end = min(start + qdrant_batch, len(payloads))
                print(f"Uploading company points: {end} / {len(payloads)}")
                await self.qdrant_store.upsert_points(
                    document_id=document_id,
                    dense_vectors=dense_vectors[start:end],
                    sparse_vectors=sparse_vectors[start:end],
                    payloads=payloads[start:end],
                )

            existing.sha256 = sha256
            existing.qdrant_document_id = document_id
            existing.chunk_count = len(chunks)
            existing.status = STATUS_INDEXED
            existing.last_ingested_at = existing.updated_at
            run.status = STATUS_INDEXED
            run.chunks_created = len(chunks)
            await self.db.commit()
            return {"status": "indexed", "document_name": document_name, "chunks": len(chunks)}
        except Exception as exc:
            existing.status = STATUS_FAILED
            existing.last_error = str(exc)
            run.status = STATUS_FAILED
            run.error = str(exc)
            await self.db.commit()
            logger.exception("Failed to ingest company knowledge %s", document_name)
            return {"status": "failed", "document_name": document_name, "error": str(exc)}
