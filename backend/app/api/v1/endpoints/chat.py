import asyncio
import logging
import time
import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
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
from app.rag.generation.prompts import ANSWER_UNAVAILABLE
from app.rag.services.rag_service import RAGService
from app.rag.conversation.conversation_service import ConversationService
from app.rag.greeting_detector import is_greeting_only, is_assistant_identity
from app.rag.greeting_response import get_greeting_response, get_assistant_identity_response
from app.rag.retrieval.query_classifier import QueryIntent, is_vr_coatings_domain_query, is_catalogue_request
from app.rag.catalogue_resolver import CatalogueResolver
from app.rag.constants import SOURCE_TYPE_COMPANY_MASTER

router = APIRouter()

logger = logging.getLogger(__name__)


def _build_rag_service() -> RAGService:
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


_rag_service = None
_generation_service = None
_rag_service_error: Exception | None = None
_generation_service_error: Exception | None = None
_service_lock = asyncio.Lock()
_original_build_rag_service = None
_original_build_generation_service = None


def _register_original_builders() -> None:
    global _original_build_rag_service, _original_build_generation_service
    _original_build_rag_service = _build_rag_service
    _original_build_generation_service = _build_generation_service


_register_original_builders()


async def get_rag_service() -> RAGService:
    global _rag_service, _rag_service_error
    builder = _build_rag_service
    if builder is not _original_build_rag_service:
        return await asyncio.to_thread(builder)

    if _rag_service is not None:
        return _rag_service
    async with _service_lock:
        if _rag_service is not None:
            return _rag_service
        if _rag_service_error is not None:
            raise RuntimeError("RAG service initialization failed") from _rag_service_error
        try:
            service = await asyncio.to_thread(builder)
        except Exception as exc:
            _rag_service_error = exc
            raise RuntimeError("RAG service initialization failed") from exc
        _rag_service = service
        globals()["_embedding_models_ready"] = True
        return service


async def get_generation_service() -> GenerationService:
    global _generation_service, _generation_service_error
    builder = _build_generation_service
    if builder is not _original_build_generation_service:
        return await asyncio.to_thread(builder)

    if _generation_service is not None:
        return _generation_service
    async with _service_lock:
        if _generation_service is not None:
            return _generation_service
        if _generation_service_error is not None:
            raise RuntimeError("Generation service initialization failed") from _generation_service_error
        try:
            service = await asyncio.to_thread(builder)
        except Exception as exc:
            _generation_service_error = exc
            raise RuntimeError("Generation service initialization failed") from exc
        _generation_service = service
        return service


def _provider_status_code(exc: BaseException) -> int | None:
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        status = getattr(current, "status_code", None)
        if status is None:
            response = getattr(current, "response", None)
            status = getattr(response, "status_code", None)
        if isinstance(status, int):
            return status
        current = current.__cause__ or current.__context__
    return None


def _chat_error_to_http(exc: Exception, stage: str, request_id: str, elapsed_ms: float) -> HTTPException:
    status_code = getattr(exc, "status_code", None)
    if not isinstance(status_code, int):
        status_code = _provider_status_code(exc)

    if status_code == 429:
        http_status = 429
        detail = "The AI service is rate-limited. Please try again shortly."
    elif status_code in (401, 403):
        http_status = 502
        detail = "The AI service authentication failed."
    elif status_code is not None and status_code >= 500:
        http_status = 502
        detail = "The AI service is temporarily unavailable."
    elif isinstance(exc, (ConnectionError, TimeoutError, asyncio.TimeoutError)):
        http_status = 503
        detail = "A backend dependency is temporarily unavailable."
    else:
        message = str(exc).lower()
        if "qdrant" in message or "connection" in message:
            http_status = 503
            detail = "A backend dependency is temporarily unavailable."
        elif "embedding" in message:
            http_status = 503
            detail = "A backend dependency is temporarily unavailable."
        elif "groq" in message and ("rate" in message or "429" in message):
            http_status = 429
            detail = "The AI service is rate-limited. Please try again shortly."
        else:
            http_status = 500
            detail = "An unexpected error occurred."

    logger.exception(
        "Chat request failed",
        extra={
            "request_id": request_id,
            "stage": stage,
            "exception_type": type(exc).__name__,
            "provider_http_status": status_code,
            "elapsed_ms": round(elapsed_ms, 2),
        },
    )
    headers = {}
    if http_status == 429:
        headers["Retry-After"] = "10"
    return HTTPException(status_code=http_status, detail=detail, headers=headers or None)


# Extend ChatRequest to include optional history for stateless operation
class ChatRequestWithHistory(ChatRequest):
    history: Optional[List[Dict[str, Any]]] = Field(default=None, description="Recent conversation history from frontend")


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequestWithHistory) -> ChatResponse:
    request_id = uuid.uuid4().hex
    started_at = time.perf_counter()
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=422, detail="Message must not be empty")

    conversation_service = ConversationService()

    # Use or generate conversation_id
    conversation_id = request.conversation_id if request.conversation_id else conversation_service.generate_conversation_id()

    # Validate and use client-provided history
    recent_messages = conversation_service.validate_history(request.history or [])
    
    # Add current user message to history for context building
    user_msg = {"role": "user", "content": request.message.strip()}
    recent_messages_with_current = recent_messages + [user_msg]
    
    active_context = conversation_service.get_active_product_context(recent_messages_with_current)

    message = request.message.strip()

    # PATH A: deterministic conversational responses (no retrieval, no generation).
    if is_greeting_only(message):
        answer = get_greeting_response(message)
        return ChatResponse(
            conversation_id=conversation_id,
            answer=answer,
            sources=[],
            retrieval=None,
            show_sources=False,
            intent=QueryIntent.GREETING.value,
        )

    if is_assistant_identity(message):
        answer = get_assistant_identity_response()
        return ChatResponse(
            conversation_id=conversation_id,
            answer=answer,
            sources=[],
            retrieval=None,
            show_sources=False,
            intent=QueryIntent.ASSISTANT_IDENTITY.value,
        )

    if is_catalogue_request(message):
        resolver = CatalogueResolver()
        resolved_slug, catalogues = await resolver.resolve_from_message(message)
        if resolved_slug and catalogues:
            product_name = catalogues[0]["product_name"]
            answer = f"Sure \u2014 here is the {product_name} product catalogue."
        elif resolved_slug:
            answer = f"I couldn\u2019t find a VR Coatings catalogue for that product right now."
        else:
            answer = "I couldn\u2019t find a VR Coatings catalogue for that product."
        return ChatResponse(
            conversation_id=conversation_id,
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
            service = await get_rag_service()
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            raise _chat_error_to_http(exc, "rag_service_init", request_id, elapsed_ms)

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
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            raise _chat_error_to_http(exc, "rag_pipeline", request_id, elapsed_ms)
    else:
        # PATH C: general chat via Groq directly.
        try:
            service = await get_generation_service()
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            raise _chat_error_to_http(exc, "generation_service_init", request_id, elapsed_ms)

        try:
            result = await service.generate_general_answer(
                question=message,
                recent_messages=recent_messages,
            )
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            raise _chat_error_to_http(exc, "general_generation", request_id, elapsed_ms)

    intent = QueryIntent(result.get("intent", QueryIntent.UNKNOWN.value))
    answer = result.get("answer", "")

    show_sources = _should_show_sources(intent, active_context, answer, result.get("sources", []))
    filtered_sources = _filter_sources_for_ui(result.get("sources", []), active_context, intent)

    if answer == ANSWER_UNAVAILABLE:
        show_sources = False
        filtered_sources = []

    sources = [ChatSource(**source) for source in filtered_sources]
    retrieval_data = result.get("retrieval")
    retrieval = ChatRetrieval(**retrieval_data) if retrieval_data else None

    resolved_slug = active_context.get("product_slug") if active_context else None
    catalogues: list[dict[str, Any]] = []
    show_catalogues = False
    if resolved_slug:
        resolver = CatalogueResolver()
        catalogues = await resolver.resolve(resolved_slug)
        show_catalogues = bool(catalogues)

    return ChatResponse(
        conversation_id=conversation_id,
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

    if intent == QueryIntent.PRODUCT_DISCOVERY:
        return bool(sources)

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
    intent: QueryIntent | None = None,
) -> list:
    resolved_slug = (active_context or {}).get("product_slug")
    resolved_document = (active_context or {}).get("document")

    seen = set()
    filtered: list = []
    for src in sources:
        source_type = src.get("source_type")
        document = src.get("document")
        product_slug = src.get("product_slug")

        # Hide raw Company Master from user-facing sources for product-specific queries.
        # For discovery queries, company_master may legitimately contain industry/application evidence.
        if source_type == SOURCE_TYPE_COMPANY_MASTER and intent != QueryIntent.PRODUCT_DISCOVERY:
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
async def chat_status() -> Dict[str, Any]:
    qdrant_connected = False
    indexed_count = 0
    try:
        store = QdrantStore()
        collection_name = rag_settings.QDRANT_COLLECTION_NAME
        info = await asyncio.to_thread(store.client.get_collection, collection_name)
        qdrant_connected = True
        indexed_count = int(getattr(info, "points_count", 0) or 0)
    except Exception:
        try:
            store = QdrantStore()
            await asyncio.to_thread(store.client.get_collections)
            qdrant_connected = True
        except Exception:
            qdrant_connected = False

    generation_ready = _generation_ready()
    rag_ready = qdrant_connected and indexed_count > 0 and generation_ready
    return {
        "rag_ready": rag_ready,
        "dense_embedding_ready": globals().get("_embedding_models_ready", False),
        "sparse_embedding_ready": globals().get("_embedding_models_ready", False),
        "qdrant_connected": qdrant_connected,
        "generation_ready": generation_ready,
        "ocr_available": False,
        "indexed_documents": indexed_count,
    }
