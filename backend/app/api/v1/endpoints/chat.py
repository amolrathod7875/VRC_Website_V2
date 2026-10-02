from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatSource, ChatRetrieval
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
from app.rag.conversation.conversation_service import ConversationService
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
    try:
        llm = LLMFactory.create()
    except Exception as exc:
        raise RuntimeError(f"Generation provider unavailable: {exc}") from exc
    generator = GenerationService(llm_provider=llm)
    return RAGService(
        dense=dense,
        sparse=sparse,
        retriever=retriever,
        generator=generator,
        context_builder=context_builder,
    )


def _generation_ready() -> bool:
    try:
        provider = (rag_settings.LLM_PROVIDER or "").lower().strip()
        if provider == "groq":
            return bool(rag_settings.GROQ_API_KEY or __import__("os").environ.get("GROQ_API_KEY"))
        return False
    except Exception:
        return False


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=422, detail="Message must not be empty")

    try:
        service = _build_rag_service(db)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    conversation_service = ConversationService(db)

    try:
        conversation = await conversation_service.get_or_create_conversation(
            str(request.conversation_id) if request.conversation_id else None
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    await conversation_service.append_user_message(conversation.id, request.message.strip())

    recent_messages = await conversation_service.get_recent_messages(conversation.id, limit=8)
    active_context = conversation_service.get_active_product_context(recent_messages)
    augmented_query = conversation_service.build_augmented_query(request.message.strip(), recent_messages, active_context)

    try:
        result = await service.answer(
            question=request.message.strip(),
            filters=None,
            retrieval_query=augmented_query,
            recent_messages=recent_messages,
        )
    except Exception as exc:
        await db.commit()
        raise HTTPException(status_code=500, detail="RAG pipeline failed") from exc

    sources = [ChatSource(**source) for source in result.get("sources", [])]
    retrieval_data = result.get("retrieval")
    retrieval = ChatRetrieval(**retrieval_data) if retrieval_data else None
    answer = result.get("answer", "")

    await conversation_service.append_assistant_message(
        conversation_id=conversation.id,
        content=answer,
        sources=result.get("sources", []),
        retrieval_metadata=result.get("retrieval"),
    )

    await db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        answer=answer,
        sources=sources,
        retrieval=retrieval,
    )


@router.get("/status")
async def chat_status(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    dense_embedding_ready = False
    sparse_embedding_ready = False
    qdrant_connected = False
    try:
        DenseEmbeddingService()
        dense_embedding_ready = True
    except Exception:
        pass
    try:
        SparseEmbeddingService()
        sparse_embedding_ready = True
    except Exception:
        pass
    try:
        QdrantStore().client.get_collections()
        qdrant_connected = True
    except Exception:
        pass
    try:
        total_result = await db.execute(select(func.count(RagDocument.id)).where(RagDocument.status == "indexed"))
        indexed_count = total_result.scalar_one() or 0
    except Exception:
        indexed_count = 0
    ocr_available = False
    try:
        from app.rag.ingestion.ocr.ocr_service import ocr_service_from_settings
        ocr_available = ocr_service_from_settings() is not None
    except Exception:
        pass
    rag_ready = dense_embedding_ready and sparse_embedding_ready and qdrant_connected and indexed_count > 0
    return {
        "rag_ready": rag_ready,
        "dense_embedding_ready": dense_embedding_ready,
        "sparse_embedding_ready": sparse_embedding_ready,
        "qdrant_connected": qdrant_connected,
        "generation_ready": _generation_ready(),
        "ocr_available": ocr_available,
        "indexed_documents": indexed_count,
    }
