import asyncio
from unittest.mock import AsyncMock, patch
import pytest
from groq import APIStatusError
from app.rag.generation.groq_provider import GroqProvider
from app.rag.services.rag_service import RAGService
from app.rag.generation.prompts import ANSWER_UNAVAILABLE


def test_groq_429_retry_is_bounded() -> None:
    provider = GroqProvider()
    provider.client = AsyncMock()

    call_count = 0

    async def failing_call(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            raise APIStatusError(
                message="Too Many Requests",
                response=AsyncMock(status_code=429, headers={"retry-after": "0.1"}),
                body=None,
            )
        return AsyncMock(choices=[AsyncMock(message=AsyncMock(content="30:1"))])

    provider.client.chat.completions.create = failing_call

    async def run_test():
        return await provider.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt="What is the pressure ratio?",
            context="Tiger 30:150 has a pressure ratio of 30:1.",
        )

    result = asyncio.run(run_test())
    assert result == "30:1"
    assert call_count == 3


def test_groq_repeated_429_returns_error() -> None:
    provider = GroqProvider()
    provider.client = AsyncMock()

    call_count = 0

    async def always_failing(**kwargs):
        nonlocal call_count
        call_count += 1
        raise APIStatusError(
            message="Too Many Requests",
            response=AsyncMock(status_code=429, headers={"retry-after": "0.1"}),
            body=None,
        )

    provider.client.chat.completions.create = always_failing

    async def run_test():
        try:
            await provider.generate(
                system_prompt="You are a helpful assistant.",
                user_prompt="What is the pressure ratio?",
                context="Tiger 30:150 has a pressure ratio of 30:1.",
            )
        except RuntimeError:
            return "error"
        return "ok"

    result = asyncio.run(run_test())
    assert result == "error"
    assert call_count == 3


def test_rag_service_graceful_failure_after_groq_retry_exhausted() -> None:
    mock_dense = AsyncMock()
    mock_dense.embed_query.return_value = [0.1] * 384
    mock_sparse = AsyncMock()
    mock_sparse.embed_query.return_value = {"indices": [0], "values": [0.1]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {
            "text": "Tiger 30:150 has a pressure ratio of 30:1.",
            "source_type": "catalogue",
            "document_name": "Tiger.pdf",
            "section": "technical_specifications",
        }
    ]

    class SyncContextBuilder:
        def build(self, chunks, query):
            return {
                "context": "Tiger 30:150 has a pressure ratio of 30:1.",
                "sources": [],
                "chunks": [],
            }

    mock_context_builder = SyncContextBuilder()

    failing_provider = GroqProvider()
    failing_provider.client = AsyncMock()
    call_count = 0

    async def always_failing(**kwargs):
        nonlocal call_count
        call_count += 1
        raise APIStatusError(
            message="Too Many Requests",
            response=AsyncMock(status_code=429, headers={"retry-after": "0.1"}),
            body=None,
        )

    failing_provider.client.chat.completions.create = always_failing
    from app.rag.generation.generation_service import GenerationService
    mock_generator = GenerationService(llm_provider=failing_provider)

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )
    result = asyncio.run(service.answer("What is the pressure ratio of Tiger 30:150?"))
    assert "unable to generate" in result["answer"]
