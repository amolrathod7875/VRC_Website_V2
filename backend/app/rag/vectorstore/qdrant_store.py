from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, SparseVectorParams, PayloadSchemaType
from app.rag.config import rag_settings
from app.rag.constants import STATUS_INDEXED


class QdrantStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
        self.collection_name = rag_settings.QDRANT_COLLECTION_NAME

    async def ensure_collection(self) -> None:
        try:
            collections = self.client.get_collections().collections
            if any(col.name == self.collection_name for col in collections):
                return
        except Exception:
            raise RuntimeError("Unable to connect to Qdrant")

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={"dense": VectorParams(size=self._dense_dimension(), distance=Distance.COSINE)},
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

    def _dense_dimension(self) -> int:
        return 384

    async def upsert_points(
        self,
        document_id: str,
        dense_vectors: List[List[float]],
        sparse_vectors: List[Dict[str, Any]],
        payloads: List[Dict[str, Any]],
    ) -> None:
        points = []
        for idx, payload in enumerate(payloads):
            points.append({
                "id": payload.get("chunk_id"),
                "vector": {
                    "dense": dense_vectors[idx],
                    "sparse": sparse_vectors[idx],
                },
                "payload": payload,
            })
        self.client.upsert(collection_name=self.collection_name, points=points)

    async def delete_by_document_id(self, document_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={"filter": {"must": [{"key": "document_id", "match": {"value": document_id}}]}},
        )

    async def hybrid_search(self, dense_query: List[float], sparse_query: Dict[str, Any], limit: int) -> List[Any]:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=("dense", dense_query),
            limit=limit,
            with_payload=True,
        )
        return results
