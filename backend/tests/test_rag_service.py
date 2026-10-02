from unittest.mock import AsyncMock, MagicMock

from app.rag.services.rag_service import RAGService
from app.rag.generation.prompts import ANSWER_UNAVAILABLE


def test_rag_service_returns_unavailable_when_no_retrieval() -> None:
    mock_dense = MagicMock()
    mock_dense.embed_query.return_value = [0.1, 0.2]
    mock_sparse = MagicMock()
    mock_sparse.embed_query.return_value = {"indices": [1], "values": [0.5]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = []
    mock_generator = AsyncMock()
    mock_context_builder = MagicMock()

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )

    import asyncio

    result = asyncio.run(service.answer("What is the pressure ratio?"))
    assert result["answer"] == ANSWER_UNAVAILABLE
    assert result["retrieval"]["chunks_used"] == 0
    mock_generator.generate_answer.assert_not_called()
    mock_context_builder.build.assert_not_called()


def test_rag_service_includes_retrieval_metadata() -> None:
    mock_dense = MagicMock()
    mock_dense.embed_query.return_value = [0.1, 0.2]
    mock_sparse = MagicMock()
    mock_sparse.embed_query.return_value = {"indices": [1], "values": [0.5]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {"text": "Pressure ratio: 30:1", "source_type": "catalogue", "model": "30:150", "product_slug": "tiger"}
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

    import asyncio

    result = asyncio.run(service.answer("What is the pressure ratio?"))
    assert result["answer"] == "30:1"
    assert result["retrieval"]["chunks_used"] == 1
    assert "retrieval_duration_ms" in result["retrieval"]
    assert "generation_duration_ms" in result["retrieval"]
    assert "total_duration_ms" in result["retrieval"]


def test_rag_service_handles_provider_failure() -> None:
    mock_dense = MagicMock()
    mock_dense.embed_query.return_value = [0.1, 0.2]
    mock_sparse = MagicMock()
    mock_sparse.embed_query.return_value = {"indices": [1], "values": [0.5]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {"text": "Pressure ratio: 30:1", "source_type": "catalogue", "model": "30:150", "product_slug": "tiger"}
    ]
    mock_context_builder = MagicMock()
    mock_context_builder.build.return_value = {
        "context": "Pressure ratio: 30:1",
        "sources": [],
        "chunks": [{"text": "Pressure ratio: 30:1"}],
    }
    mock_generator = AsyncMock()
    mock_generator.generate_answer.side_effect = RuntimeError("Groq unavailable")

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )

    import asyncio

    result = asyncio.run(service.answer("What is the pressure ratio?"))
    assert "unable to generate" in result["answer"]
    assert result["retrieval"]["provider_error"] is True