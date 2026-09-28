from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.config import rag_settings
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.generation.generation_service import GenerationService
from app.rag.generation.factory import LLMFactory
from app.rag.services.rag_service import RAGService
from app.models.rag_document import RagDocument
from sqlalchemy import select, func

router = APIRouter()


def _build_rag_service(db: AsyncSession) -> RAGService:
    qdrant_store = QdrantStore()
    dense = DenseEmbeddingService()
    sparse = SparseEmbeddingService()
    retriever = HybridRetriever(qdrant_store=qdrant_store)
    reranker = Reranker()
    context_builder = ContextBuilder(reranker=reranker)
    llm = LLMFactory.create()
    generator = GenerationService(llm_provider=llm, context_builder=context_builder)
    return RAGService(dense=dense, sparse=sparse, retriever=retriever, generator=generator)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    service = _build_rag_service(db)
    result = await service.answer(question=request.message, filters=None)
    sources = [ChatSource(**source) for source in result.get("sources", [])]
    return ChatResponse(answer=result.get("answer", ""), sources=sources)


@router.get("/status")
async def chat_status(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    try:
        total_result = await db.execute(select(func.count(RagDocument.id)).where(RagDocument.status == "indexed"))
        indexed_count = total_result.scalar_one() or 0
        qdrant_connected = True
        try:
            QdrantStore().client.get_collections()
        except Exception:
            qdrant_connected = False
        return {
            "rag_ready": indexed_count > 0 and qdrant_connected,
            "qdrant_connected": qdrant_connected,
            "indexed_documents": indexed_count,
        }
    except Exception:
        return {"rag_ready": False, "qdrant_connected": False, "indexed_documents": 0}
