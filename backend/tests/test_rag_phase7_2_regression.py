import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.rag.conversation.conversation_service import ConversationService
from app.rag.retrieval.query_classifier import classify_query, QueryIntent
from app.rag.services.rag_service import RAGService
from app.rag.generation.prompts import ANSWER_UNAVAILABLE
from app.rag.ingestion.ingestion_service import IngestionService
from app.models.rag_document import RagDocument
from app.core.config import Settings


def test_normalize_technical_terms_output_expands():
    cs = ConversationService.__new__(ConversationService)
    result = cs._normalize_technical_terms("What is its output?")
    assert "output per cycle" in result
    assert result == "What is its output per cycle?"


def test_normalize_technical_terms_applications_expands():
    cs = ConversationService.__new__(ConversationService)
    result = cs._normalize_technical_terms("What applications is it used for?")
    assert "applications/use" in result
    assert result == "What applications/use is it used for?"


def test_normalize_technical_terms_pressure_ratio_preserved():
    cs = ConversationService.__new__(ConversationService)
    result = cs._normalize_technical_terms("What about pressure ratio?")
    assert result == "What about pressure ratio?"


def test_normalize_technical_terms_standalone_ratio_expands():
    cs = ConversationService.__new__(ConversationService)
    result = cs._normalize_technical_terms("What about ratio?")
    assert "pressure ratio" in result


def test_normalize_technical_terms_standalone_pressure_expands():
    cs = ConversationService.__new__(ConversationService)
    result = cs._normalize_technical_terms("What about pressure?")
    assert "pressure ratio" in result


def test_build_augmented_query_preserves_model_identifier():
    cs = ConversationService.__new__(ConversationService)
    question = "What is its output?"
    recent_messages = [
        {
            "role": "user",
            "content": "Tell me about Tiger 30:150.",
            "sources": [],
            "retrieval_metadata": {},
        },
        {
            "role": "assistant",
            "content": "The Tiger 30:150 has an output per cycle of 150 cc.",
            "sources": [
                {
                    "source_type": "catalogue",
                    "document": "Tiger.pdf",
                    "product": "Tiger",
                    "product_slug": "tiger",
                    "model": "30:150",
                }
            ],
            "retrieval_metadata": {},
        },
    ]
    active_context = cs.get_active_product_context(recent_messages)
    augmented = cs.build_augmented_query(question, recent_messages, active_context)
    assert "30:150" in augmented
    assert "30 150" not in augmented
    assert "30/150" not in augmented
    assert "30-150" not in augmented
    assert "output per cycle" in augmented


def test_build_augmented_query_output_classifies_as_product_technical():
    cs = ConversationService.__new__(ConversationService)
    question = "What is its output?"
    recent_messages = [
        {
            "role": "user",
            "content": "Tell me about Tiger 30:150.",
            "sources": [],
            "retrieval_metadata": {},
        },
        {
            "role": "assistant",
            "content": "The Tiger 30:150 has an output per cycle of 150 cc.",
            "sources": [
                {
                    "source_type": "catalogue",
                    "document": "Tiger.pdf",
                    "product": "Tiger",
                    "product_slug": "tiger",
                    "model": "30:150",
                }
            ],
            "retrieval_metadata": {},
        },
    ]
    active_context = cs.get_active_product_context(recent_messages)
    augmented = cs.build_augmented_query(question, recent_messages, active_context)
    intent = classify_query(augmented)
    assert intent == QueryIntent.PRODUCT_TECHNICAL


def test_context_builder_uses_augmented_query_for_intent():
    from app.rag.retrieval.context_builder import ContextBuilder
    from app.rag.retrieval.reranker import Reranker

    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {
            "text": "Output per cycle: 150 cc",
            "source_type": "catalogue",
            "section": "technical_model",
            "authority_priority": 100,
            "score": 0.5,
        }
    ]
    result = builder.build(chunks, "What is its output per cycle? tiger 30:150")
    assert result["chunks"][0]["text"] == "Output per cycle: 150 cc"


def test_output_followup_retrieves_technical_evidence():
    mock_dense = MagicMock()
    mock_dense.embed_query.return_value = [0.1] * 384
    mock_sparse = MagicMock()
    mock_sparse.embed_query.return_value = {"indices": [0], "values": [0.1]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {
            "text": "Output per cycle: 150 cc",
            "source_type": "catalogue",
            "document_name": "Tiger.pdf",
            "model": "30:150",
            "product_slug": "tiger",
            "score": 0.9,
        }
    ]
    mock_context_builder = MagicMock()
    mock_context_builder.build.return_value = {
        "context": "Output per cycle: 150 cc",
        "sources": [{"document": "Tiger.pdf", "model": "30:150"}],
        "chunks": [{"text": "Output per cycle: 150 cc"}],
    }
    mock_generator = AsyncMock()
    mock_generator.generate_answer.return_value = {"answer": "150 cc", "provider_error": False}

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )

    result = asyncio.run(
        service.answer("What is its output?", retrieval_query="What is its output per cycle? tiger 30:150")
    )
    assert result["answer"] == "150 cc"


def test_pressure_followup_remains_thirty_colon_one():
    mock_dense = MagicMock()
    mock_dense.embed_query.return_value = [0.1] * 384
    mock_sparse = MagicMock()
    mock_sparse.embed_query.return_value = {"indices": [0], "values": [0.1]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {
            "text": "Pressure ratio: 30:1",
            "source_type": "catalogue",
            "document_name": "Tiger.pdf",
            "model": "30:150",
            "product_slug": "tiger",
            "score": 0.9,
        }
    ]
    mock_context_builder = MagicMock()
    mock_context_builder.build.return_value = {
        "context": "Pressure ratio: 30:1",
        "sources": [{"document": "Tiger.pdf", "model": "30:150"}],
        "chunks": [{"text": "Pressure ratio: 30:1"}],
    }
    mock_generator = AsyncMock()
    mock_generator.generate_answer.return_value = {"answer": "30:1", "provider_error": False}

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )

    result = asyncio.run(
        service.answer("And pressure ratio?", retrieval_query="And pressure ratio? tiger 30:150")
    )
    assert result["answer"] == "30:1"


def test_price_followup_remains_unavailable():
    mock_dense = MagicMock()
    mock_dense.embed_query.return_value = [0.1] * 384
    mock_sparse = MagicMock()
    mock_sparse.embed_query.return_value = {"indices": [0], "values": [0.1]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {
            "text": "Tiger 30:150 technical data",
            "source_type": "catalogue",
            "document_name": "Tiger.pdf",
        }
    ]
    mock_context_builder = MagicMock()
    mock_context_builder.build.return_value = {
        "context": "Tiger 30:150 technical data",
        "sources": [{"document": "Tiger.pdf"}],
        "chunks": [{"text": "Tiger 30:150 technical data"}],
    }
    mock_generator = AsyncMock()
    mock_generator.generate_answer.return_value = {"answer": ANSWER_UNAVAILABLE, "provider_error": False}

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )

    result = asyncio.run(
        service.answer("How much does it cost?", retrieval_query="How much does it cost? tiger 30:150")
    )
    assert result["answer"] == ANSWER_UNAVAILABLE


def test_topic_switching_does_not_augment_non_ambiguous_question():
    cs = ConversationService.__new__(ConversationService)
    question = "When was VR Coatings founded?"
    recent_messages = [
        {
            "role": "user",
            "content": "Tell me about Tiger 30:150.",
            "sources": [],
            "retrieval_metadata": {},
        },
        {
            "role": "assistant",
            "content": "The Tiger 30:150 is a pump.",
            "sources": [
                {
                    "source_type": "catalogue",
                    "document": "Tiger.pdf",
                    "product_slug": "tiger",
                    "model": "30:150",
                }
            ],
            "retrieval_metadata": {},
        },
    ]
    active_context = cs.get_active_product_context(recent_messages)
    augmented = cs.build_augmented_query(question, recent_messages, active_context)
    assert augmented == question
    assert "tiger" not in augmented.lower()
    assert "30:150" not in augmented


def test_evidence_guard_requires_fresh_retrieval():
    from app.rag.retrieval.query_classifier import evaluate_evidence_guard

    question = "What is its output?"
    context = "Output per cycle: 150 cc"
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is False


def test_registry_skips_unchanged_tiger():
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = RagDocument(
        document_name="Tiger.pdf",
        sha256="9d9fa3fcbe4050d4bb60649ea87303c9bff9dcb2a6dcb687e4b83d1720e7e44e",
    )
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result
    mock_qdrant = MagicMock()
    mock_dense = MagicMock()
    mock_sparse = MagicMock()

    service = IngestionService(db=mock_db, qdrant_store=mock_qdrant, dense=mock_dense, sparse=mock_sparse)

    result = asyncio.run(
        service.ingest_catalogue(
            __import__("pathlib").Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues/Tiger.pdf")
        )
    )
    assert result["status"] == "skipped"
    assert result["reason"] == "unchanged"


def test_registry_skips_unchanged_company_master():
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = RagDocument(
        document_name="VR_Coatings_RAG_Monolithic_Knowledge_Base.txt",
        sha256="f8c67d3b747c7a9a50e8fc2b424a4f9e549ffeaa2f4a977a19225aebb958c1f0",
    )
    mock_db = AsyncMock()
    mock_db.execute.return_value = mock_result
    mock_qdrant = MagicMock()
    mock_dense = MagicMock()
    mock_sparse = MagicMock()

    service = IngestionService(db=mock_db, qdrant_store=mock_qdrant, dense=mock_dense, sparse=mock_sparse)

    result = asyncio.run(
        service.ingest_company(
            __import__("pathlib").Path("/home/vr-coatings/Desktop/website_V2/backend/storage/knowledge/VR_Coatings_RAG_Monolithic_Knowledge_Base.txt")
        )
    )
    assert result["status"] == "skipped"
    assert result["reason"] == "unchanged"


def test_database_url_reads_from_environment():
    settings = Settings(DATABASE_URL="postgresql+psycopg://vrcoatings:vrcoatings@postgres:5432/vrcoatings")
    assert settings.DATABASE_URL == "postgresql+psycopg://vrcoatings:vrcoatings@postgres:5432/vrcoatings"
