"""Qdrant-first document registry.

Provides deterministic, DB-free document identity and ingestion-state detection.
Qdrant payload metadata is the authoritative source for which documents have
been indexed, their SHA-256, and their current chunk count.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny

from app.rag.config import rag_settings
from app.rag.vectorstore.qdrant_store import QdrantStore

logger = logging.getLogger(__name__)


class DocumentRegistry:
    """Repository abstraction over document-level Qdrant metadata.

    Each point in the Qdrant collection carries a ``document_id`` and
    ``document_name`` payload field. This class aggregates those point-level
    payloads into document-level information, replacing the former
    ``rag_documents`` Postgres registry.
    """

    PAGE_SIZE = 200

    def __init__(self, qdrant_store: Optional[QdrantStore] = None) -> None:
        self.qdrant_store = qdrant_store or QdrantStore()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _scroll_by_document_id(self, document_id: str) -> List[Any]:
        """Return all points whose ``document_id`` payload matches."""
        points: List[Any] = []
        offset = None
        while True:
            batch, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                scroll_filter=Filter(
                    must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
                ),
                limit=self.PAGE_SIZE,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            points.extend(batch)
            if not offset:
                break
        return points

    def _scroll_by_document_name(self, document_name: str) -> List[Any]:
        """Return all points whose ``document_name`` payload matches."""
        points: List[Any] = []
        offset = None
        while True:
            batch, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                scroll_filter=Filter(
                    must=[FieldCondition(key="document_name", match=MatchValue(value=document_name))]
                ),
                limit=self.PAGE_SIZE,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            points.extend(batch)
            if not offset:
                break
        return points

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def document_exists(self, document_id: str) -> bool:
        points = self._scroll_by_document_id(document_id)
        return len(points) > 0

    def get_document_state(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Return aggregated document-level metadata from first matching point."""
        points = self._scroll_by_document_id(document_id)
        if not points:
            return None
        payload = points[0].payload or {}
        return {
            "document_id": payload.get("document_id", document_id),
            "document_name": payload.get("document_name"),
            "source_type": payload.get("source_type"),
            "product_slug": payload.get("product_slug"),
            "product_slugs": payload.get("product_slugs"),
            "parent_product_slug": payload.get("parent_product_slug"),
            "sha256": payload.get("sha256") or payload.get("source_hash"),
            "storage_path": payload.get("storage_path"),
            "chunk_count": len(points),
        }

    def get_document_hash(self, document_id: str) -> Optional[str]:
        state = self.get_document_state(document_id)
        if state:
            return state["sha256"]
        return None

    def get_document_point_count(self, document_id: str) -> int:
        points = self._scroll_by_document_id(document_id)
        return len(points)

    def get_document_state_by_name(self, document_name: str) -> Optional[Dict[str, Any]]:
        """Look up document state by filename (the canonical source name)."""
        points = self._scroll_by_document_name(document_name)
        if not points:
            return None
        payload = points[0].payload or {}
        return {
            "document_id": payload.get("document_id"),
            "document_name": payload.get("document_name"),
            "source_type": payload.get("source_type"),
            "product_slug": payload.get("product_slug"),
            "product_slugs": payload.get("product_slugs"),
            "parent_product_slug": payload.get("parent_product_slug"),
            "sha256": payload.get("sha256") or payload.get("source_hash"),
            "storage_path": payload.get("storage_path"),
            "chunk_count": len(points),
        }

    def delete_document_points(self, document_id: str) -> int:
        """Delete all points belonging to ``document_id``. Returns deleted count."""
        points = self._scroll_by_document_id(document_id)
        if not points:
            return 0
        point_ids = [p.id for p in points]
        self.qdrant_store.client.delete(
            collection_name=self.qdrant_store.collection_name,
            points_selector=point_ids,
        )
        return len(point_ids)

    def delete_document_points_by_name(self, document_name: str) -> int:
        """Delete all points belonging to ``document_name`` (handles both old and new doc IDs)."""
        points = self._scroll_by_document_name(document_name)
        if not points:
            return 0
        point_ids = [p.id for p in points]
        self.qdrant_store.client.delete(
            collection_name=self.qdrant_store.collection_name,
            points_selector=point_ids,
        )
        return len(point_ids)

    def list_indexed_documents(self) -> List[Dict[str, Any]]:
        """Return a deduplicated list of document-level metadata from Qdrant payloads."""
        documents: Dict[str, Dict[str, Any]] = {}
        offset = None
        while True:
            points, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                limit=self.PAGE_SIZE,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            for point in points:
                payload = point.payload or {}
                doc_id = payload.get("document_id") or payload.get("document_name")
                if not doc_id:
                    continue
                if doc_id not in documents:
                    documents[doc_id] = self.get_document_state(doc_id) or {
                        "document_id": doc_id,
                        "document_name": payload.get("document_name"),
                        "source_type": payload.get("source_type"),
                        "product_slug": payload.get("product_slug"),
                        "sha256": payload.get("sha256") or payload.get("source_hash"),
                        "chunk_count": 0,
                    }
                documents[doc_id]["chunk_count"] = documents[doc_id].get("chunk_count", 0) + 1
            if not offset:
                break
        return list(documents.values())

    def update_document_payload(
        self, document_id: str, updates: Dict[str, Any]
    ) -> int:
        """Patch payload fields on all points belonging to ``document_id``."""
        points = self._scroll_by_document_id(document_id)
        if not points:
            return 0
        point_ids = [p.id for p in points]
        self.qdrant_store.client.set_payload(
            collection_name=self.qdrant_store.collection_name,
            payload=updates,
            points=point_ids,
        )
        return len(point_ids)

    def find_documents_by_product_slug(self, product_slug: str) -> List[Dict[str, Any]]:
        """Find all documents that match the given product_slug."""
        from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny

        documents: Dict[str, Dict[str, Any]] = {}
        offset = None
        scroll_filter = Filter(
            should=[
                FieldCondition(key="product_slug", match=MatchValue(value=product_slug)),
                FieldCondition(key="parent_product_slug", match=MatchValue(value=product_slug)),
            ]
        )
        while True:
            points, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                scroll_filter=scroll_filter,
                limit=self.PAGE_SIZE,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            for point in points:
                payload = point.payload or {}
                doc_id = payload.get("document_id") or payload.get("document_name")
                if not doc_id:
                    continue
                if doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "document_name": payload.get("document_name"),
                        "source_type": payload.get("source_type"),
                        "product_slug": payload.get("product_slug"),
                        "product_slugs": payload.get("product_slugs"),
                        "parent_product_slug": payload.get("parent_product_slug"),
                        "sha256": payload.get("sha256") or payload.get("source_hash"),
                        "storage_path": payload.get("storage_path"),
                        "chunk_count": 0,
                    }
                documents[doc_id]["chunk_count"] = documents[doc_id].get("chunk_count", 0) + 1
            if not offset:
                break
        return list(documents.values())

    @staticmethod
    def create(qdrant_store: Optional[QdrantStore] = None) -> "DocumentRegistry":
        return DocumentRegistry(qdrant_store=qdrant_store)
