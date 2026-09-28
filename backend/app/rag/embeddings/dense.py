from typing import List

from fastembed import TextEmbedding as FastEmbedTextEmbedding
from app.rag.config import rag_settings


class DenseEmbeddingService:
    def __init__(self) -> None:
        self.model = FastEmbedTextEmbedding(rag_settings.RAG_DENSE_MODEL)
        self._dimension: int = 384

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        batch_size = max(1, rag_settings.RAG_EMBED_BATCH_SIZE)
        vectors: List[List[float]] = []
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            for item in self.model.embed(batch):
                vectors.append(item.tolist())
        return vectors

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

    @property
    def dimension(self) -> int:
        return self._dimension
