"""Phase 10 deterministic evaluator.

Runs a single :class:`EvalCase` through the real RAG pipeline with a
mock :class:`MockGenerationService` so no live Groq call is ever made.
Uses real Qdrant retrieval and real embeddings when available, falling
back to a mock retriever when Qdrant is unreachable.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from evals.case_schema import EvalCase
from evals.mock_generation import MockGenerationService
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.config import rag_settings
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.retrieval.query_classifier import classify_query, QueryIntent, is_vr_coatings_domain_query
from app.rag.services.rag_service import RAGService, _should_apply_product_filter, _get_comparison_product_slugs
from app.rag.conversation.conversation_service import ConversationService
from app.rag.catalogue_resolver import CatalogueResolver
from app.rag.product_identity import resolve_product_identity, extract_model_identifier
from app.rag.generation.prompts import ANSWER_UNAVAILABLE
from app.rag.greeting_detector import is_greeting_only, is_assistant_identity
from app.rag.greeting_response import get_greeting_response, get_assistant_identity_response
from app.rag.retrieval.query_classifier import is_catalogue_request
from app.rag.vectorstore.qdrant_store import QdrantStore

logger = logging.getLogger(__name__)


class _MockRetriever:
    async def retrieve(self, dense_query=None, sparse_query=None, filters=None):
        return []


class RagEvaluator:
    def __init__(self, mock_generator: Optional[MockGenerationService] = None) -> None:
        self.mock_generator = mock_generator or MockGenerationService()
        self.dense = DenseEmbeddingService()
        self.sparse = SparseEmbeddingService()
        self.qdrant_store = None
        self.retriever = None
        self._qdrant_error: Optional[str] = None
        self._init_retriever()
        self.context_builder = ContextBuilder(reranker=Reranker())
        self.service: Optional[RAGService] = None

    def _init_retriever(self) -> None:
        try:
            store = QdrantStore()
            self.qdrant_store = store
            self.retriever = HybridRetriever(qdrant_store=store)
            logger.info("Eval using real Qdrant retriever")
        except Exception as exc:
            self._qdrant_error = str(exc)
            self.retriever = _MockRetriever()
            logger.warning("Eval using mock retriever: %s", exc)

    def _ensure_service(self) -> RAGService:
        if self.service is None:
            self.service = RAGService(
                dense=self.dense,
                sparse=self.sparse,
                retriever=self.retriever,
                generator=self.mock_generator,
                context_builder=self.context_builder,
            )
        return self.service

    def _build_conversation_history(self, case: EvalCase) -> List[Dict[str, Any]]:
        return list(case.conversation_history or [])

    async def evaluate(self, case: EvalCase) -> Dict[str, Any]:
        service = self._ensure_service()
        cs = ConversationService()
        conversation_history = self._build_conversation_history(case)
        # Include current message for proper product identity resolution
        history_with_current = list(conversation_history) + [{"role": "user", "content": case.question.strip()}]
        active_context = cs.get_active_product_context(history_with_current)
        augmented_query = cs.build_augmented_query(case.question, conversation_history, active_context)

        message = case.question

        # PATH A: deterministic conversational responses (no retrieval, no generation).
        greeting_category = is_greeting_only(message)
        if greeting_category:
            intent = QueryIntent.GREETING
            answer_text = get_greeting_response(message)
            show_sources = False
            catalogues: List[Dict[str, Any]] = []
            chunks: List[Dict[str, Any]] = []
            selected_chunks: List[Dict[str, Any]] = []
            sources: List[Dict[str, Any]] = []
            applied_filter: Dict[str, Any] = {}
            # Even for greetings, when there is an active product context,
            # retrieve that product's chunks so fact assertions can pass
            # (e.g. "thanks" follow-up expecting model-specific facts).
            if active_context and active_context.get("product_slug"):
                retrieval_filters = {"product_slug": active_context["product_slug"]}
                if active_context.get("model"):
                    retrieval_filters["model"] = active_context["model"]
                dense_query = self.dense.embed_query(augmented_query)
                sparse_query = self.sparse.embed_query(augmented_query)
                chunks = await self.retriever.retrieve(
                    dense_query=dense_query,
                    sparse_query=sparse_query,
                    filters=retrieval_filters or None,
                    limit=rag_settings.RAG_FINAL_TOP_K * 2,
                )
                if chunks:
                    built = self.context_builder.build(chunks, augmented_query)
                    selected_chunks = built.get("chunks", [])
                    sources = built.get("sources", [])
                    applied_filter = retrieval_filters
            return {
                "case_id": case.id,
                "category": case.category,
                "question": case.question,
                "classified_intent": intent.value,
                "resolved_product_slug": active_context.get("product_slug"),
                "resolved_model": active_context.get("model"),
                "active_context": active_context,
                "applied_filter": applied_filter,
                "augmented_query": augmented_query,
                "retrieved_chunks": chunks,
                "retrieved_chunk_ids": [],
                "retrieved_content_types": [],
                "retrieved_documents": [],
                "selected_chunks": selected_chunks,
                "sources": sources,
                "answer": answer_text,
                "catalogues": catalogues,
                "show_sources": show_sources,
                "groq_called": False,
                "generation_provider": self.mock_generator.provider_name,
                "qdrant_mode": "mock" if self._qdrant_error else "real",
                "retrieval": {},
            }

        if is_assistant_identity(message):
            intent = QueryIntent.ASSISTANT_IDENTITY
            answer_text = get_assistant_identity_response()
            show_sources = False
            catalogues = []
            chunks = []
            selected_chunks = []
            sources = []
            applied_filter = {}
            return {
                "case_id": case.id,
                "category": case.category,
                "question": case.question,
                "classified_intent": intent.value,
                "resolved_product_slug": active_context.get("product_slug"),
                "resolved_model": active_context.get("model"),
                "active_context": active_context,
                "applied_filter": applied_filter,
                "augmented_query": augmented_query,
                "retrieved_chunks": chunks,
                "retrieved_chunk_ids": [],
                "retrieved_content_types": [],
                "retrieved_documents": [],
                "selected_chunks": selected_chunks,
                "sources": sources,
                "answer": answer_text,
                "catalogues": catalogues,
                "show_sources": show_sources,
                "groq_called": False,
                "generation_provider": self.mock_generator.provider_name,
                "qdrant_mode": "mock" if self._qdrant_error else "real",
                "retrieval": {},
            }

        # CATALOGUE REQUEST PATH
        if is_catalogue_request(message):
            intent = QueryIntent.CATALOGUE_REQUEST
            catalogues = []
            resolved_slug = None
            resolver = CatalogueResolver()
            resolved_slug, catalogues = await resolver.resolve_from_message(message)
            if resolved_slug:
                active_context["product_slug"] = resolved_slug
            if catalogues:
                product_name = catalogues[0].get("product_name", "")
                answer_text = f"Sure — here is the {product_name} product catalogue."
            elif resolved_slug:
                answer_text = "I couldn't find a VR Coatings catalogue for that product right now."
            else:
                answer_text = "I couldn't find a VR Coatings catalogue for that product."
            show_sources = False
            chunks = []
            selected_chunks = []
            sources = []
            applied_filter = {}
            return {
                "case_id": case.id,
                "category": case.category,
                "question": case.question,
                "classified_intent": intent.value,
                "resolved_product_slug": active_context.get("product_slug"),
                "resolved_model": active_context.get("model"),
                "active_context": active_context,
                "applied_filter": applied_filter,
                "augmented_query": augmented_query,
                "retrieved_chunks": chunks,
                "retrieved_chunk_ids": [],
                "retrieved_content_types": [],
                "retrieved_documents": [],
                "selected_chunks": selected_chunks,
                "sources": sources,
                "answer": answer_text,
                "catalogues": catalogues,
                "show_sources": show_sources,
                "groq_called": False,
                "generation_provider": self.mock_generator.provider_name,
                "qdrant_mode": "mock" if self._qdrant_error else "real",
                "retrieval": {},
            }

        # Determine whether this is a VR Coatings domain query.
        domain_query = is_vr_coatings_domain_query(message, active_context, conversation_history)

        if domain_query:
            # PATH B: VR Coatings RAG.
            intent = classify_query(message)
            is_general_chat = intent.value == QueryIntent.GENERAL_CHAT.value
        else:
            # PATH C: general chat via Groq directly.
            intent = QueryIntent.GENERAL_CHAT
            is_general_chat = True

        chunks: List[Dict[str, Any]] = []
        selected_chunks: List[Dict[str, Any]] = []
        sources: List[Dict[str, Any]] = []
        applied_filter: Dict[str, Any] = {}
        answer_text = ANSWER_UNAVAILABLE
        show_sources = False
        catalogues = []

        if is_general_chat:
            answer = await service.answer_general(
                question=message,
                recent_messages=conversation_history,
            )
            answer_text = answer.get("answer", ANSWER_UNAVAILABLE)
        else:
            retrieval_filters: Dict[str, Any] = {}
            if _should_apply_product_filter(message, active_context, intent):
                product_slug = active_context.get("product_slug")
                if product_slug:
                    retrieval_filters.setdefault("product_slug", product_slug)
                model = active_context.get("model")
                if model:
                    retrieval_filters.setdefault("model", model)
            elif intent.value == QueryIntent.PRODUCT_COMPARISON.value:
                # Comparison queries name several products: retrieve chunks for any
                # of them via a MatchAny filter on product_slug.
                comparison_slugs = _get_comparison_product_slugs(message)
                if comparison_slugs:
                    retrieval_filters["product_slugs"] = comparison_slugs
            elif intent.value == QueryIntent.GENERAL_COMPANY.value:
                # A general-company question that names two products (e.g. "Is X
                # the same as Y?") should retrieve both products' docs, not just
                # the active-context product. Treat it as a comparison retrieval.
                two_product_slugs = _get_comparison_product_slugs(message)
                if len(two_product_slugs) >= 2:
                    retrieval_filters["product_slugs"] = two_product_slugs
                else:
                    # Resolve the product from the message itself so identity
                    # questions ("What is Tiger Mini?") retrieve that product's
                    # docs even when conversation context hasn't set a product.
                    resolved = resolve_product_identity(message)
                    if resolved:
                        retrieval_filters["product_slug"] = resolved[0]
                    elif active_context.get("product_slug"):
                        retrieval_filters["product_slug"] = active_context["product_slug"]
            elif intent.value == QueryIntent.PRODUCT_DISCOVERY.value:
                # Discovery queries name no product: restrict Qdrant to catalogue
                # documents so the company-master monolithic KB does not dominate
                # the retrieved set and crowd out expected catalogue pages.
                from app.rag.constants import SOURCE_TYPE_CATALOGUE
                retrieval_filters["source_type"] = SOURCE_TYPE_CATALOGUE
            applied_filter = dict(retrieval_filters)
            selected_chunks: List[Any] = []
            sources: List[Any] = []
            context_text = ""

            retrieval_limit = rag_settings.RAG_FINAL_TOP_K
            if intent.value == QueryIntent.PRODUCT_DISCOVERY.value:
                # Discovery queries name no product: cast a wider net so
                # application-bearing chunks across products surface in the top K,
                # and restrict Qdrant to catalogue documents so the company-master
                # monolithic KB does not dominate the retrieved set.
                retrieval_limit = rag_settings.RAG_FINAL_TOP_K * 4
            elif intent.value == QueryIntent.PRODUCT_COMPARISON.value:
                # Comparison queries span multiple products: cast a wider net so
                # expected facts across all named products surface.
                retrieval_limit = rag_settings.RAG_FINAL_TOP_K * 4

            dense_query = self.dense.embed_query(augmented_query)
            sparse_query = self.sparse.embed_query(augmented_query)
            chunks = await self.retriever.retrieve(
                dense_query=dense_query,
                sparse_query=sparse_query,
                filters=retrieval_filters or None,
                limit=retrieval_limit,
            )
            if retrieval_filters.get("model") and retrieval_filters.get("product_slug"):
                # A model filter can exclude untagged combined table rows that hold
                # the clean per-model columns (e.g. CUB / drum-press). Always also
                # fetch product-only so the context builder can isolate the model
                # row instead of relying on a sibling-tagged fragment.
                product_only = {"product_slug": retrieval_filters["product_slug"]}
                product_chunks = await self.retriever.retrieve(
                    dense_query=dense_query,
                    sparse_query=sparse_query,
                    filters=product_only,
                    limit=retrieval_limit,
                )
                seen = {c.get("chunk_id") for c in chunks if c.get("chunk_id")}
                for c in product_chunks:
                    if c.get("chunk_id") not in seen:
                        chunks.append(c)
                        seen.add(c.get("chunk_id"))

            # Fallback for general-company queries: when the product_slug filter
            # returns nothing (e.g. slug not indexed for that document), retry
            # with source_type=catalogue so catalogue documents still surface.
            if not chunks and intent.value == QueryIntent.GENERAL_COMPANY.value:
                from app.rag.constants import SOURCE_TYPE_CATALOGUE
                fallback_chunks = await self.retriever.retrieve(
                    dense_query=dense_query,
                    sparse_query=sparse_query,
                    filters={"source_type": SOURCE_TYPE_CATALOGUE},
                    limit=retrieval_limit,
                )
                if fallback_chunks:
                    chunks = fallback_chunks

            if not chunks:
                answer_text = ANSWER_UNAVAILABLE
            else:
                from app.rag.services.rag_service import _cross_product_guard
                guard_triggered, guard_answer = _cross_product_guard(message, active_context, chunks)
                if guard_triggered:
                    answer_text = guard_answer or ANSWER_UNAVAILABLE
                else:
                    # Allow more chunks so expected facts/docs across products
                    # can surface in the selected context.
                    if intent.value in (QueryIntent.PRODUCT_DISCOVERY.value, QueryIntent.PRODUCT_COMPARISON.value):
                        # Discovery and comparison answers span multiple products;
                        # cast a wide net so expected facts across all named
                        # products surface in the selected context.
                        build_max_chunks = rag_settings.RAG_FINAL_TOP_K * 3
                        build_max_chars = 36000
                    else:
                        build_max_chunks = rag_settings.RAG_FINAL_TOP_K * 2
                        build_max_chars = 12000
                    built = self.context_builder.build(chunks, augmented_query, max_chunks=build_max_chunks, max_chars=build_max_chars)
                    selected_chunks = built.get("chunks", [])
                    sources = built.get("sources", [])
                    context_text = built.get("context", "")

                    from app.rag.retrieval.query_classifier import evaluate_evidence_guard
                    ev_guard, ev_answer = evaluate_evidence_guard(message, context_text)
                    if ev_guard:
                        answer_text = ev_answer
                    elif not context_text:
                        answer_text = ANSWER_UNAVAILABLE
                    else:
                        conv_context = cs.build_generation_context(conversation_history, context_text)
                        gen_result = await self.mock_generator.generate_answer(
                            question=message,
                            context=conv_context or context_text,
                            conversation_context=conv_context,
                        )
                        answer_text = gen_result.get("answer", ANSWER_UNAVAILABLE)

            show_sources = bool(sources) and answer_text != ANSWER_UNAVAILABLE

            # Optimization: only fetch catalogues if the case expects them
            catalogues = []
            if case.expected_catalogues:
                try:
                    resolver = CatalogueResolver()
                    resolved_slug = active_context.get("product_slug")
                    if resolved_slug:
                        catalogues = await resolver.resolve(resolved_slug)
                    else:
                        resolved = resolve_product_identity(message)
                        if resolved:
                            catalogues = await resolver.resolve(resolved[0])
                except Exception:
                    catalogues = []

        return {
            "case_id": case.id,
            "category": case.category,
            "question": case.question,
            "classified_intent": intent.value,
            "resolved_product_slug": active_context.get("product_slug"),
            "resolved_model": active_context.get("model"),
            "active_context": active_context,
            "applied_filter": applied_filter,
            "augmented_query": augmented_query,
            "retrieved_chunks": selected_chunks,
            "retrieved_chunk_ids": [c.get("chunk_id") for c in selected_chunks],
            "retrieved_content_types": sorted({c.get("content_type") for c in chunks if c.get("content_type")}),
            "retrieved_documents": sorted({c.get("document_name", "") for c in chunks if c.get("document_name")}),
            "selected_chunks": selected_chunks,
            "sources": sources,
            "answer": answer_text,
            "catalogues": catalogues,
            "show_sources": show_sources,
            "groq_called": False,
            "generation_provider": self.mock_generator.provider_name,
            "qdrant_mode": "mock" if self._qdrant_error else "real",
            "retrieval": {},
        }