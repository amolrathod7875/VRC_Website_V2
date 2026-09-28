from typing import Dict, List

from fastembed import SparseTextEmbedding
from app.rag.config import rag_settings


class SparseEmbeddingService:
    def __init__(self) -> None:
        self.model = SparseTextEmbedding(rag_settings.RAG_SPARSE_MODEL)

    def embed_documents(self, texts: List[str]) -> List[Dict[str, List[float]]]:
        batch_size = max(1, rag_settings.RAG_EMBED_BATCH_SIZE)
        results: List[Dict[str, List[float]]] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            for item in self.model.embed(batch):
                results.append({"indices": item.indices.tolist(), "values": item.values.tolist()})
        return results

    def embed_query(self, text: str) -> Dict[str, List[float]]:
        for item in self.model.embed([text]):
            return {"indices": item.indices.tolist(), "values": item.values.tolist()}
        return {"indices": [], "values": []}