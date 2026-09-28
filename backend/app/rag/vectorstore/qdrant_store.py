from typing import Any, Dict, List, Optional
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, SparseVectorParams, PayloadSchemaType, Fusion, Prefetch, SparseVector, Filter, FieldCondition, MatchValue, FusionQuery
from app.rag.config import rag_settings
from app.rag.constants import STATUS_INDEXED

_POINT_ID_NAMESPACE = uuid.UUID("12345678-1234-5678-1234-567812345678")


def _stable_point_id(document_id: str, chunk_id: str) -> str:
    raw = f"{document_id}:{chunk_id}"
    return str(uuid.uuid5(_POINT_ID_NAMESPACE, raw))


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
            ("content_type", PayloadSchemaType.KEYWORD),
        ]:
            try:
                self.client.create_payload_index(collection_name=self.collection_name, field_name=field, field_schema=schema_type)
            except Exception:
                pass

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
                point_id = _stable_point_id(document_id, str(payload.get("chunk_id", idx)))
                points.append({
                    "id": point_id,
                    "vector": {
                        "dense": batch_dense[idx],
                        "sparse": SparseVector(indices=sparse.get("indices", []), values=sparse.get("values", [])),
                    },
                    "payload": payload,
                })
            self.client.upsert(collection_name=self.collection_name, points=points)

    async def delete_by_document_id(self, document_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]),
        )

    async def hybrid_search(self, dense_query: List[float], sparse_query: Dict[str, Any], limit: int) -> List[Any]:
        sparse_vector = SparseVector(indices=sparse_query.get("indices", []), values=sparse_query.get("values", []))
        results = self.client.query_points(
            collection_name=self.collection_name,
            prefetch=[
                Prefetch(query=dense_query, using="dense", limit=limit * 2),
                Prefetch(query=sparse_vector, using="sparse", limit=limit * 2),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            limit=limit,
            with_payload=True,
        )
        return results.points
