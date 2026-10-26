from typing import Any, Dict, List, Optional
import uuid
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, SparseVectorParams, PayloadSchemaType, Fusion, Prefetch, SparseVector, Filter, FieldCondition, MatchValue, MatchAny, FusionQuery
from app.rag.config import rag_settings
from app.rag.constants import STATUS_INDEXED
from app.rag.utils.ids import stable_point_id

logger = logging.getLogger(__name__)


class QdrantStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
        self.collection_name = rag_settings.QDRANT_COLLECTION_NAME

    async def ensure_collection(self) -> None:
        try:
            collections = self.client.get_collections().collections
            if any(col.name == self.collection_name for col in collections):
                return
        except Exception as exc:
            raise RuntimeError(f"Unable to connect to Qdrant: {exc}") from exc

        dense_size = 384
        try:
            from app.rag.embeddings.dense import DenseEmbeddingService
            dense_size = DenseEmbeddingService().dimension
        except Exception:
            pass

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={"dense": VectorParams(size=dense_size, distance=Distance.COSINE)},
            sparse_vectors_config={"sparse": SparseVectorParams()},
        )
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        for field, schema_type in [
            ("source_type", PayloadSchemaType.KEYWORD),
            ("product_slug", PayloadSchemaType.KEYWORD),
            ("document_id", PayloadSchemaType.KEYWORD),
            ("document_name", PayloadSchemaType.KEYWORD),
            ("sha256", PayloadSchemaType.KEYWORD),
            ("content_type", PayloadSchemaType.KEYWORD),
            ("model", PayloadSchemaType.KEYWORD),
            ("parent_product_slug", PayloadSchemaType.KEYWORD),
        ]:
            try:
                self.client.create_payload_index(collection_name=self.collection_name, field_name=field, field_schema=schema_type)
            except Exception:
                pass

    @property
    def _indexed_payload_fields(self) -> set:
        """Payload fields that have a Qdrant keyword index (safe to filter on)."""
        return {"source_type", "product_slug", "document_id", "document_name", "sha256", "content_type", "model", "parent_product_slug"}

    async def upsert_points(
        self,
        document_id: str,
        dense_vectors: List[List[float]],
        sparse_vectors: List[Dict[str, Any]],
        payloads: List[Dict[str, Any]],
    ) -> None:
        batch_size = max(1, rag_settings.RAG_QDRANT_UPSERT_BATCH_SIZE)
        for start in range(0, len(payloads), batch_size):
            batch_payloads = payloads[start:start + batch_size]
            batch_dense = dense_vectors[start:start + batch_size]
            batch_sparse = sparse_vectors[start:start + batch_size]
            points = []
            for idx, payload in enumerate(batch_payloads):
                sparse = batch_sparse[idx]
                point_id = stable_point_id(document_id, str(payload.get("chunk_id", idx)))
                points.append({
                    "id": point_id,
                    "vector": {
                        "dense": batch_dense[idx],
                        "sparse": SparseVector(indices=sparse.get("indices", []), values=sparse.get("values", [])),
                    },
                    "payload": payload,
                })
            self.client.upsert(collection_name=self.collection_name, points=points)

    def delete_by_document_name(self, document_name: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(must=[FieldCondition(key="document_name", match=MatchValue(value=document_name))]),
        )

    async def delete_by_document_id(self, document_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]),
        )

    def _build_qdrant_filter(self, filters: Optional[Dict[str, Any]]) -> Optional[Filter]:
        if not filters:
            return None
        # Only filter on payload fields that have a Qdrant keyword index. Passing an
        # unindexed key (e.g. "model") raises a 400 from the Qdrant API. Unknown keys
        # are skipped with a warning rather than silently mis-filtering.
        must = []
        should = []
        for key, value in filters.items():
            if value is None:
                continue
            # A list of product slugs (comparison queries) maps to the indexed
            # product_slug field with a MatchAny condition so any of the named
            # products can match.
            if key == "product_slugs" and isinstance(value, (list, tuple)):
                vals = [v for v in value if v]
                if vals:
                    must.append(
                        FieldCondition(key="product_slug", match=MatchAny(any=vals))
                    )
                continue
            # A list of document names (parent -> child catalogue fallback) maps to
            # the indexed document_name field with MatchAny.
            if key == "document_names" and isinstance(value, (list, tuple)):
                vals = [v for v in value if v]
                if vals:
                    must.append(
                        FieldCondition(key="document_name", match=MatchAny(any=vals))
                    )
                continue
            # Family retrieval: OR condition across product_slug and
            # parent_product_slug. Value is a list of dicts, each containing
            # product_slug and/or parent_product_slug. Matches points where ANY
            # of the specified child/family conditions hold.
            if key == "product_slug_or_parent" and isinstance(value, (list, tuple)):
                for entry in value:
                    if not isinstance(entry, dict):
                        continue
                    entry_conditions = []
                    child_slug = entry.get("product_slug")
                    if child_slug:
                        entry_conditions.append(
                            FieldCondition(key="product_slug", match=MatchValue(value=child_slug))
                        )
                    parent_slug = entry.get("parent_product_slug")
                    if parent_slug:
                        entry_conditions.append(
                            FieldCondition(key="parent_product_slug", match=MatchValue(value=parent_slug))
                        )
                    if entry_conditions:
                        should.append(Filter(should=entry_conditions))
                continue
            if key not in self._indexed_payload_fields:
                logger.warning(
                    "Skipping Qdrant filter on unindexed payload field %r", key
                )
                continue
            must.append(FieldCondition(key=key, match=MatchValue(value=value)))
        if not must and not should:
            return None
        return Filter(must=must if must else None, should=should if should else None)

    async def hybrid_search(self, dense_query: List[float], sparse_query: Dict[str, Any], limit: int, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        sparse_vector = SparseVector(indices=sparse_query.get("indices", []), values=sparse_query.get("values", []))
        qdrant_filter = self._build_qdrant_filter(filters)
        results = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(query=dense_query, using="dense", limit=limit * 2),
                Prefetch(query=sparse_vector, using="sparse", limit=limit * 2),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit,
            with_payload=True,
            query_filter=qdrant_filter,
        )
        return results.points

    async def update_payloads_by_document_id(self, document_id: str, updates: Dict[str, Any]) -> int:
        """Update payload fields for all points belonging to a document.

        Returns the number of points updated.
        """
        points = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]),
            limit=4096,
            with_payload=True,
        )[0]
        if not points:
            return 0
        updated = 0
        for point in points:
            payload = dict(point.payload or {})
            payload.update(updates)
            self.client.set_payload(
                collection_name=self.collection_name,
                payload=payload,
                points=[point.id],
            )
            updated += 1
        return updated
