from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatSource, ChatRetrieval, CatalogueReference
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
from app.rag.greeting_detector import is_greeting_only, is_assistant_identity
from app.rag.greeting_response import get_greeting_response, get_assistant_identity_response
from app.rag.retrieval.query_classifier import QueryIntent, is_vr_coatings_domain_query, is_catalogue_request
from app.rag.catalogue_resolver import CatalogueResolver
from app.models.rag_document import RagDocument
from app.rag.constants import SOURCE_TYPE_COMPANY_MASTER
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


def _build_generation_service() -> GenerationService:
    try:
        llm = LLMFactory.create()
    except Exception as exc:
        raise RuntimeError(f"Generation provider unavailable: {exc}") from exc
    return GenerationService(llm_provider=llm)


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

    message = request.message.strip()

    # PATH A: deterministic conversational responses (no retrieval, no generation).
    if is_greeting_only(message):
        answer = get_greeting_response(message)
        await conversation_service.append_assistant_message(
            conversation_id=conversation.id,
            content=answer,
            sources=[],
            retrieval_metadata=None,
        )
        await db.commit()
        return ChatResponse(
            conversation_id=conversation.id,
            answer=answer,
            sources=[],
            retrieval=None,
            show_sources=False,
            intent=QueryIntent.GREETING.value,
        )

    if is_assistant_identity(message):
        answer = get_assistant_identity_response()
        await conversation_service.append_assistant_message(
            conversation_id=conversation.id,
            content=answer,
            sources=[],
            retrieval_metadata=None,
        )
        await db.commit()
        return ChatResponse(
            conversation_id=conversation.id,
            answer=answer,
            sources=[],
            retrieval=None,
            show_sources=False,
            intent=QueryIntent.ASSISTANT_IDENTITY.value,
        )

    if is_catalogue_request(message):
        resolver = CatalogueResolver(db=db)
        resolved_slug, catalogues = await resolver.resolve_from_message(message)
        if resolved_slug and catalogues:
            product_name = catalogues[0]["product_name"]
            answer = f"Sure \u2014 here is the {product_name} product catalogue."
        elif resolved_slug:
            answer = f"I couldn\u2019t find a VR Coatings catalogue for that product right now."
        else:
            answer = "I couldn\u2019t find a VR Coatings catalogue for that product."
        await conversation_service.append_assistant_message(
            conversation_id=conversation.id,
            content=answer,
            sources=[],
            retrieval_metadata=None,
        )
        await db.commit()
        return ChatResponse(
            conversation_id=conversation.id,
            answer=answer,
            sources=[],
            retrieval=None,
            show_sources=False,
            intent=QueryIntent.CATALOGUE_REQUEST.value,
            catalogues=[CatalogueReference(**c) for c in catalogues],
            show_catalogues=bool(catalogues),
        )

    # Determine whether this is a VR Coatings domain query.
    domain_query = is_vr_coatings_domain_query(message, active_context, recent_messages)

    if domain_query:
        # PATH B: VR Coatings RAG.
        try:
            service = _build_rag_service(db)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        augmented_query = conversation_service.build_augmented_query(message, recent_messages, active_context)

        try:
            result = await service.answer(
                question=message,
                filters=None,
                retrieval_query=augmented_query,
                recent_messages=recent_messages,
                active_context=active_context,
            )
        except Exception as exc:
            await db.commit()
            raise HTTPException(status_code=500, detail="RAG pipeline failed") from exc
    else:
        # PATH C: general chat via Groq directly.
        try:
            service = _build_generation_service()
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        try:
            result = await service.answer_general(
                question=message,
                recent_messages=recent_messages,
            )
        except Exception as exc:
            await db.commit()
            raise HTTPException(status_code=500, detail="General chat generation failed") from exc

    intent = QueryIntent(result.get("intent", QueryIntent.UNKNOWN.value))
    show_sources = _should_show_sources(intent, active_context, result.get("answer", ""), result.get("sources", []))
    filtered_sources = _filter_sources_for_ui(result.get("sources", []), active_context)

    sources = [ChatSource(**source) for source in filtered_sources]
    retrieval_data = result.get("retrieval")
    retrieval = ChatRetrieval(**retrieval_data) if retrieval_data else None
    answer = result.get("answer", "")

    resolved_slug = active_context.get("product_slug") if active_context else None
    catalogues: list[dict[str, Any]] = []
    show_catalogues = False
    if resolved_slug and intent in (
        QueryIntent.PRODUCT_TECHNICAL,
        QueryIntent.PRODUCT_APPLICATION,
        QueryIntent.MODEL_IDENTIFIER,
        QueryIntent.CATALOGUE_REQUEST,
    ):
        resolver = CatalogueResolver(db=db)
        catalogues = await resolver.resolve(resolved_slug)
        show_catalogues = bool(catalogues)

    await conversation_service.append_assistant_message(
        conversation_id=conversation.id,
        content=answer,
        sources=filtered_sources,
        retrieval_metadata=result.get("retrieval"),
    )

    await db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        answer=answer,
        sources=sources,
        retrieval=retrieval,
        show_sources=show_sources,
        intent=intent.value,
        catalogues=[CatalogueReference(**c) for c in catalogues],
        show_catalogues=show_catalogues,
    )


def _should_show_sources(
    intent: QueryIntent,
    active_context: Dict[str, Optional[str]],
    answer: str,
    sources: list,
) -> bool:
    if intent in (
        QueryIntent.GREETING,
        QueryIntent.ASSISTANT_IDENTITY,
        QueryIntent.GENERAL_CHAT,
        QueryIntent.GENERAL_COMPANY,
        QueryIntent.CONTACT_LOCATION,
        QueryIntent.GOVERNANCE,
        QueryIntent.UNKNOWN,
    ):
        return False

    if intent in (
        QueryIntent.PRODUCT_TECHNICAL,
        QueryIntent.PRODUCT_APPLICATION,
        QueryIntent.MODEL_IDENTIFIER,
        QueryIntent.PRODUCT_COMPARISON,
    ):
        has_product_context = bool(active_context and active_context.get("product_slug"))
        has_catalogue_sources = any(src.get("source_type") == "catalogue" for src in sources)
        return has_product_context or has_catalogue_sources

    return False


def _filter_sources_for_ui(
    sources: list,
    active_context: Dict[str, Optional[str]],
) -> list:
    resolved_slug = (active_context or {}).get("product_slug")
    resolved_document = (active_context or {}).get("document")

    seen = set()
    filtered: list = []
    for src in sources:
        source_type = src.get("source_type")
        document = src.get("document")
        product_slug = src.get("product_slug")

        # Hide raw Company Master from user-facing sources.
        if source_type == SOURCE_TYPE_COMPANY_MASTER:
            continue

        # For product queries, prefer sources matching the resolved product.
        if resolved_slug and product_slug and product_slug != resolved_slug:
            continue

        # Deduplicate by document_name.
        doc_key = document
        if doc_key in seen:
            continue
        seen.add(doc_key)

        filtered.append(src)

    # Limit to a reasonable number of source cards.
    return filtered[:3]


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
