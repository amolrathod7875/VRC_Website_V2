import time
import logging
from typing import Any, Dict, List, Optional
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.generation.generation_service import GenerationService
from app.rag.generation.factory import LLMFactory
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings
from app.rag.generation.prompts import ANSWER_UNAVAILABLE
from app.rag.retrieval.query_classifier import evaluate_evidence_guard, classify_query
from app.rag.constants import SOURCE_TYPE_CATALOGUE

logger = logging.getLogger(__name__)

_COMPARISON_HINTS = [" compare ", " vs ", " versus ", "difference between "]


def _should_apply_product_filter(question: str, active_context: Optional[Dict[str, Optional[str]]], intent: Any) -> bool:
    if not active_context or not active_context.get("product_slug"):
        return False
    if intent.value in ("product_comparison", "governance"):
        return False
    if intent.value == "general_company":
        return False
    normalized = f" {question.strip().lower()} "
    if any(hint in normalized for hint in _COMPARISON_HINTS):
        return False
    return True


def _cross_product_guard(question: str, active_context: Optional[Dict[str, Optional[str]]], chunks: List[Dict[str, Any]]) -> tuple[bool, str]:
    if not active_context or not active_context.get("product_slug"):
        return False, ""
    intent = classify_query(question)
    if intent.value not in ("product_technical", "product_application", "model_identifier"):
        return False, ""
    resolved_slug = active_context.get("product_slug", "")
    catalogue_sources = [c for c in chunks if c.get("source_type") == SOURCE_TYPE_CATALOGUE]
    if not catalogue_sources:
        return False, ""
    matching = [c for c in catalogue_sources if c.get("product_slug") == resolved_slug]
    if not matching:
        return True, ANSWER_UNAVAILABLE
    return False, ""


class RAGService:
    def __init__(
        self,
        dense: DenseEmbeddingService,
        sparse: SparseEmbeddingService,
        retriever: HybridRetriever,
        generator: GenerationService,
        context_builder: ContextBuilder,
    ) -> None:
        self.dense = dense
        self.sparse = sparse
        self.retriever = retriever
        self.generator = generator
        self.context_builder = context_builder

    async def answer(
        self,
        question: str,
        filters: Dict[str, Any] | None = None,
        retrieval_query: Optional[str] = None,
        recent_messages: Optional[List[Dict[str, Any]]] = None,
        active_context: Optional[Dict[str, Optional[str]]] = None,
    ) -> Dict[str, Any]:
        start = time.perf_counter()

        effective_query = retrieval_query or question
        intent = classify_query(question)

        retrieval_filters = dict(filters or {})
        if _should_apply_product_filter(question, active_context, intent):
            retrieval_filters.setdefault("product_slug", active_context.get("product_slug"))

        dense_query = self.dense.embed_query(effective_query)
        sparse_query = self.sparse.embed_query(effective_query)

        retrieval_start = time.perf_counter()
        chunks = await self.retriever.retrieve(
            dense_query=dense_query,
            sparse_query=sparse_query,
            filters=retrieval_filters or None,
        )
        retrieval_duration = (time.perf_counter() - retrieval_start) * 1000

        if not chunks:
            logger.info(
                "No retrieval results for question",
                extra={
                    "question_length": len(question),
                    "retrieval_candidates": 0,
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round((time.perf_counter() - start) * 1000, 2),
                    "provider_error": False,
                    "query_intent": intent.value,
                },
            )
            return {
                "answer": ANSWER_UNAVAILABLE,
                "sources": [],
                "retrieval": {
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round((time.perf_counter() - start) * 1000, 2),
                },
            }

        guard_triggered, guard_answer = _cross_product_guard(question, active_context, chunks)
        if guard_triggered:
            total_duration = (time.perf_counter() - start) * 1000
            logger.info(
                "Cross-product evidence guard triggered",
                extra={
                    "question_length": len(question),
                    "retrieval_candidates": len(chunks),
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round(total_duration, 2),
                    "provider_error": False,
                    "query_intent": intent.value,
                    "cross_product_guard": True,
                },
            )
            return {
                "answer": guard_answer or ANSWER_UNAVAILABLE,
                "sources": [],
                "retrieval": {
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round(total_duration, 2),
                },
            }

        built = self.context_builder.build(chunks, effective_query)
        context = built.get("context", "")
        sources = built.get("sources", [])
        selected_chunks = built.get("chunks", [])

        guard_triggered, guard_answer = evaluate_evidence_guard(question, context)
        if guard_triggered:
            total_duration = (time.perf_counter() - start) * 1000
            logger.info(
                "Evidence guard triggered",
                extra={
                    "question_length": len(question),
                    "retrieval_candidates": len(chunks),
                    "chunks_used": len(selected_chunks),
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round(total_duration, 2),
                    "provider_error": False,
                    "query_intent": intent.value,
                    "evidence_guard_triggered": True,
                },
            )
            return {
                "answer": guard_answer,
                "sources": sources,
                "retrieval": {
                    "chunks_used": len(selected_chunks),
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round(total_duration, 2),
                },
            }

        if not context:
            logger.info(
                "Empty context after building",
                extra={
                    "question_length": len(question),
                    "retrieval_candidates": len(chunks),
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round((time.perf_counter() - start) * 1000, 2),
                    "provider_error": False,
                    "query_intent": intent.value,
                },
            )
            return {
                "answer": ANSWER_UNAVAILABLE,
                "sources": sources,
                "retrieval": {
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": 0.0,
                    "total_duration_ms": round((time.perf_counter() - start) * 1000, 2),
                },
            }

        conversation_context = ""
        if recent_messages:
            from app.rag.conversation.conversation_service import ConversationService
            cs = ConversationService.__new__(ConversationService)
            conversation_context = cs.build_generation_context(recent_messages, context)

        gen_start = time.perf_counter()
        try:
            gen_result = await self.generator.generate_answer(
                question=question,
                context=conversation_context or context,
                conversation_context=conversation_context,
            )
        except Exception as exc:
            total_duration = (time.perf_counter() - start) * 1000
            logger.error(
                "RAG pipeline generation error: %s",
                exc,
                extra={
                    "question_length": len(question),
                    "retrieval_candidates": len(chunks),
                    "chunks_used": len(selected_chunks),
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": round((time.perf_counter() - gen_start) * 1000, 2),
                    "total_duration_ms": round(total_duration, 2),
                    "provider_error": True,
                    "query_intent": intent.value,
                },
            )
            return {
                "answer": "I'm currently unable to generate an answer. Please try again later.",
                "sources": [],
                "retrieval": {
                    "chunks_used": 0,
                    "retrieval_duration_ms": round(retrieval_duration, 2),
                    "generation_duration_ms": round((time.perf_counter() - gen_start) * 1000, 2),
                    "total_duration_ms": round(total_duration, 2),
                    "provider_error": True,
                },
            }

        generation_duration = (time.perf_counter() - gen_start) * 1000
        total_duration = (time.perf_counter() - start) * 1000

        logger.info(
            "RAG pipeline completed",
            extra={
                "question_length": len(question),
                "retrieval_candidates": len(chunks),
                "chunks_used": len(selected_chunks),
                "retrieval_duration_ms": round(retrieval_duration, 2),
                "generation_duration_ms": round(generation_duration, 2),
                "total_duration_ms": round(total_duration, 2),
                "provider_error": bool(gen_result.get("provider_error")),
                "query_intent": intent.value,
            },
        )

        return {
            "answer": gen_result.get("answer", ANSWER_UNAVAILABLE),
            "sources": sources,
            "retrieval": {
                "chunks_used": len(selected_chunks),
                "retrieval_duration_ms": round(retrieval_duration, 2),
                "generation_duration_ms": round(generation_duration, 2),
                "total_duration_ms": round(total_duration, 2),
            },
        }
