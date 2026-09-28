from typing import Any, Dict, List
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.generation.generation_service import GenerationService
from app.rag.generation.factory import LLMFactory
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings


class RAGService:
    def __init__(
        self,
        dense: DenseEmbeddingService,
        sparse: SparseEmbeddingService,
        retriever: HybridRetriever,
        generator: GenerationService,
    ) -> None:
        self.dense = dense
        self.sparse = sparse
        self.retriever = retriever
        self.generator = generator

    async def answer(self, question: str, filters: Dict[str, Any] | None = None) -> Dict[str, Any]:
        dense_query = self.dense.embed_query(question)
        sparse_query = self.sparse.embed_query(question)
        chunks = await self.retriever.retrieve(dense_query=dense_query, sparse_query=sparse_query, filters=filters)
        result = await self.generator.generate_answer(question=question, chunks=chunks)
        return result
