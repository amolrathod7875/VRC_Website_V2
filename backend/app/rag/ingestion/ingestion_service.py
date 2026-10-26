import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from app.rag.utils.hashing import calculate_sha256
from app.rag.utils.ids import generate_document_id_for
from app.rag.ingestion.pdf_parser import extract_pages, page_needs_ocr
from app.rag.ingestion.pdf_table_parser import extract_tables
from app.rag.ingestion.ocr_corrections import apply_ocr_corrections
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.multi_product_chunker import chunk_multi_product_catalogue, _product_slug_from_heading
from app.rag.ingestion.system_catalogue_chunker import chunk_system_catalogue
from app.rag.ingestion.company_parser import parse_company_text
from app.rag.ingestion.company_chunker import chunk_company_sections
from app.rag.ingestion.metadata_builder import build_catalogue_metadata, build_company_metadata
from app.rag.vectorstore.qdrant_store import QdrantStore
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.rag.utils.ids import stable_point_id
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.document_registry import DocumentRegistry
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

_MULTI_PRODUCT_FAMILIES = {
    "automatic_gun": "automatic-spray-guns",
    "conventional guns": "kingfisher",
    "manual_guns": "manual-spray-guns",
}

_SYSTEM_CATALOGUE_SLUGS = {
    "dragon",
    "polyurea",
    "tube-varnish-coating-system",
    "vrc-mix-hp",
    "vrc-mix-low-medium-pressure",
}


def _is_multi_product_document(document_name: str) -> bool:
    doc_lower = document_name.lower()
    return any(name in doc_lower for name in _MULTI_PRODUCT_FAMILIES)


def _is_system_catalogue_document(document_name: str, product_slug: str) -> bool:
    slug = (product_slug or "").lower()
    doc_lower = document_name.lower()
    if slug in _SYSTEM_CATALOGUE_SLUGS:
        return True
    if "system" in doc_lower and "coating" in doc_lower:
        return True
    if "vrc mix" in doc_lower and "pressure" in doc_lower:
        return True
    return False


def _family_slug_for_document(document_name: str) -> Optional[str]:
    doc_lower = document_name.lower()
    for key, slug in _MULTI_PRODUCT_FAMILIES.items():
        if key in doc_lower:
            return slug
    return None


class IngestionService:
    def __init__(
        self,
        qdrant_store: QdrantStore,
        dense: DenseEmbeddingService,
        sparse: SparseEmbeddingService,
        document_registry: Optional[DocumentRegistry] = None,
    ) -> None:
        self.qdrant_store = qdrant_store
        self.dense = dense
        self.sparse = sparse
        self.document_registry = document_registry or DocumentRegistry(qdrant_store=qdrant_store)

    def _get_document_state(self, document_name: str, source_type: str) -> Optional[Dict[str, Any]]:
        """Get document state from Qdrant registry by document_name."""
        return self.document_registry.get_document_state_by_name(document_name)

    def _get_deterministic_document_id(self, document_name: str, source_type: str) -> str:
        """Generate deterministic document ID for a source file."""
        return generate_document_id_for(document_name, source_type)

    async def ingest_catalogue(self, file_path: Path) -> Dict[str, Any]:
        document_name = file_path.name
        sha256 = calculate_sha256(file_path)
        source_type = SOURCE_TYPE_CATALOGUE

        existing_state = self._get_document_state(document_name, source_type)
        if existing_state and existing_state.get("sha256") == sha256:
            logger.info("Catalogue unchanged, skipping: %s", document_name)
            return {"status": "skipped", "document_name": document_name, "reason": "unchanged"}

        document_id = self._get_deterministic_document_id(document_name, source_type)
        old_document_id = existing_state.get("document_id") if existing_state else None

        if existing_state and existing_state.get("sha256") != sha256:
            logger.info("Catalogue changed, will replace: %s (old hash: %s, new hash: %s)",
                        document_name, existing_state.get("sha256"), sha256)

        try:
            pages, ocr_results = extract_pages(str(file_path), enable_ocr=True)
            tables = extract_tables(str(file_path))
            pages, tables = apply_ocr_corrections(document_name, pages, tables)
            if not pages:
                raise ValueError("No pages extracted")

            product_slug = get_canonical_slug(document_name) or document_name.lower().replace(" ", "_").replace(".pdf", "")
            is_multi = _is_multi_product_document(document_name)
            is_system = _is_system_catalogue_document(document_name, product_slug)

            if is_multi:
                chunks = chunk_multi_product_catalogue(document_name, pages, tables, document_id, ocr_results=ocr_results)
                family_slug = _family_slug_for_document(document_name)
                child_slugs = sorted({c.get("product_slug") for c in chunks if c.get("product_slug")})
                if family_slug and family_slug not in child_slugs:
                    child_slugs.insert(0, family_slug)
                parent_slug = family_slug or (child_slugs[0] if child_slugs else product_slug)
                for chunk in chunks:
                    chunk_slug = chunk.get("product_slug")
                    if chunk_slug and chunk_slug != family_slug:
                        chunk["parent_product_slug"] = family_slug
            elif is_system:
                chunks = chunk_system_catalogue(document_name, pages, tables, product_slug, document_id, ocr_results=ocr_results)
                parent_slug = product_slug
                child_slugs = [product_slug]
            else:
                chunks = chunk_catalogue(document_name, pages, tables, product_slug, document_id, ocr_results=ocr_results)
                parent_slug = product_slug
                child_slugs = [product_slug]

            if not chunks:
                raise ValueError("No chunks generated")

            texts = [c["text"] for c in chunks]
            logger.info("Embedding %d catalogue chunks for %s", len(texts), document_name)
            dense_vectors = self.dense.embed_documents(texts)
            sparse_vectors = self.sparse.embed_documents(texts)

            payloads = []
            for idx, chunk in enumerate(chunks):
                chunk_with_slugs = dict(chunk)
                chunk_with_slugs["product_slug"] = chunk.get("product_slug") or parent_slug
                chunk_with_slugs["product_slugs"] = child_slugs
                metadata = build_catalogue_metadata(document_id, document_name, str(file_path), sha256, parent_slug, chunk_with_slugs)
                payloads.append(metadata)

            logger.info("Uploading %d points to Qdrant for %s", len(payloads), document_name)
            await self.qdrant_store.upsert_points(
                document_id=document_id,
                dense_vectors=dense_vectors,
                sparse_vectors=sparse_vectors,
                payloads=payloads,
            )

            if old_document_id and old_document_id != document_id:
                deleted = self.document_registry.delete_document_points(old_document_id)
                logger.info("Deleted %d stale points for %s (old doc_id: %s)", deleted, document_name, old_document_id)

            # Generic legacy/stale point cleanup: remove any points for this
            # document whose IDs are not part of the newly generated set. This
            # handles legacy point IDs, changed chunk counts, and partial prior
            # ingestions without deleting by document name in bulk.
            new_point_ids = {
                stable_point_id(document_id, str(pl.get("chunk_id", idx)))
                for idx, pl in enumerate(payloads)
            }
            stale_ids: list[str] = []
            offset = None
            while True:
                batch, offset = self.qdrant_store.client.scroll(
                    collection_name=self.qdrant_store.collection_name,
                    scroll_filter=Filter(must=[FieldCondition(key="document_name", match=MatchValue(value=document_name))]),
                    limit=200,
                    with_payload=False,
                    with_vectors=False,
                    offset=offset,
                )
                for pt in batch:
                    if str(pt.id) not in new_point_ids:
                        stale_ids.append(str(pt.id))
                if not offset:
                    break
            if stale_ids:
                self.qdrant_store.client.delete(
                    collection_name=self.qdrant_store.collection_name,
                    points_selector=stale_ids,
                )
                logger.info("Deleted %d stale/legacy points for %s", len(stale_ids), document_name)

            return {"status": "indexed", "document_name": document_name, "chunks": len(chunks), "document_id": document_id}

        except Exception as exc:
            logger.exception("Failed to ingest catalogue %s", document_name)
            return {"status": "failed", "document_name": document_name, "error": str(exc)}

    async def ingest_company(self, file_path: Path) -> Dict[str, Any]:
        document_name = file_path.name
        sha256 = calculate_sha256(file_path)
        source_type = SOURCE_TYPE_COMPANY_MASTER

        existing_state = self._get_document_state(document_name, source_type)
        if existing_state and existing_state.get("sha256") == sha256:
            logger.info("Company master unchanged, skipping: %s", document_name)
            return {"status": "skipped", "document_name": document_name, "reason": "unchanged"}

        document_id = self._get_deterministic_document_id(document_name, source_type)
        old_document_id = existing_state.get("document_id") if existing_state else None

        if existing_state and existing_state.get("sha256") != sha256:
            logger.info("Company master changed, will replace: %s (old hash: %s, new hash: %s)",
                        document_name, existing_state.get("sha256"), sha256)

        try:
            text = file_path.read_text(encoding="utf-8")
            sections = parse_company_text(text)
            chunks = chunk_company_sections(sections, document_id)
            if not chunks:
                raise ValueError("No chunks generated")

            total = len(chunks)
            logger.info("Parsed %d sections, %d company chunks", len(sections), total)

            texts = [c["text"] for c in chunks]
            dense_vectors = []
            sparse_vectors = []
            batch_size = max(1, rag_settings.RAG_EMBED_BATCH_SIZE)
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                logger.info("Embedding company chunks: %d / %d", end, total)
                batch_texts = texts[start:end]
                dense_vectors.extend(self.dense.embed_documents(batch_texts))
                sparse_vectors.extend(self.sparse.embed_documents(batch_texts))

            payloads = []
            for chunk in chunks:
                metadata = build_company_metadata(document_id, document_name, str(file_path), sha256, chunk)
                payloads.append(metadata)

            qdrant_batch = max(1, rag_settings.RAG_QDRANT_UPSERT_BATCH_SIZE)
            for start in range(0, len(payloads), qdrant_batch):
                end = min(start + qdrant_batch, len(payloads))
                logger.info("Uploading company points: %d / %d", end, len(payloads))
                await self.qdrant_store.upsert_points(
                    document_id=document_id,
                    dense_vectors=dense_vectors[start:end],
                    sparse_vectors=sparse_vectors[start:end],
                    payloads=payloads[start:end],
                )

            if old_document_id and old_document_id != document_id:
                deleted = self.document_registry.delete_document_points(old_document_id)
                logger.info("Deleted %d stale points for %s (old doc_id: %s)", deleted, document_name, old_document_id)

            new_point_ids = {
                stable_point_id(document_id, str(pl.get("chunk_id", idx)))
                for idx, pl in enumerate(payloads)
            }
            stale_ids: list[str] = []
            offset = None
            while True:
                batch, offset = self.qdrant_store.client.scroll(
                    collection_name=self.qdrant_store.collection_name,
                    scroll_filter=Filter(must=[FieldCondition(key="document_name", match=MatchValue(value=document_name))]),
                    limit=200,
                    with_payload=False,
                    with_vectors=False,
                    offset=offset,
                )
                for pt in batch:
                    if str(pt.id) not in new_point_ids:
                        stale_ids.append(str(pt.id))
                if not offset:
                    break
            if stale_ids:
                self.qdrant_store.client.delete(
                    collection_name=self.qdrant_store.collection_name,
                    points_selector=stale_ids,
                )
                logger.info("Deleted %d stale/legacy points for %s", len(stale_ids), document_name)

            logger.info("Successfully indexed company master: %s (%d chunks)", document_name, len(chunks))
            return {"status": "indexed", "document_name": document_name, "chunks": len(chunks), "document_id": document_id}

        except Exception as exc:
            logger.exception("Failed to ingest company knowledge %s", document_name)
            return {"status": "failed", "document_name": document_name, "error": str(exc)}