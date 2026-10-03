from typing import Any, Dict, List, Optional
from app.rag.config import rag_settings
from app.rag.vectorstore.qdrant_store import QdrantStore


class HybridRetriever:
    def __init__(self, qdrant_store: QdrantStore) -> None:
        self.qdrant_store = qdrant_store

    async def retrieve(
        self,
        dense_query: List[float],
        sparse_query: Any,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        results = await self.qdrant_store.hybrid_search(
            dense_query=dense_query,
            sparse_query=sparse_query,
            limit=rag_settings.RAG_FINAL_TOP_K,
            filters=filters,
        )
        chunks = []
        for result in results:
            payload = result.payload or {}
            payload["score"] = result.score
            chunks.append(payload)
        return chunks
