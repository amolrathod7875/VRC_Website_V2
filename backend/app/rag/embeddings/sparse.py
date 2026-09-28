from typing import Dict, List, Any
from app.rag.config import rag_settings


class SparseEmbeddingService:
    def embed_documents(self, texts: List[str]) -> List[Dict[str, Any]]:
        raise NotImplementedError("BM25 sparse embedding via Qdrant is not yet integrated.")

    def embed_query(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError("BM25 sparse query embedding via Qdrant is not yet integrated.")
