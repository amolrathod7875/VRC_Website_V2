from unittest.mock import AsyncMock

from app.rag.generation.generation_service import GenerationService
from app.rag.generation.prompts import SYSTEM_PROMPT, ANSWER_UNAVAILABLE


def test_system_prompt_contains_grounding_rules() -> None:
    prompt = SYSTEM_PROMPT.lower()
    assert "answer only using the supplied retrieved context" in prompt
    assert "never fabricate" in prompt
    assert "unknown" in prompt
    assert "tbc" in prompt
    assert "catalogue" in prompt
    assert "company master" in prompt
    assert "absence of mention is not evidence of absence" in prompt
    assert "do not infer that a product, feature, certification, service, country, application, or capability is absent merely because it is not listed" in prompt


def test_answer_unavailable_message() -> None:
    assert ANSWER_UNAVAILABLE == "This information is not available in the current VR Coatings knowledge base."


def test_generation_service_returns_answer_with_mocked_provider() -> None:
    mock_provider = AsyncMock()
    mock_provider.generate.return_value = "30:1"
    service = GenerationService(llm_provider=mock_provider)
    import asyncio

    result = asyncio.run(service.generate_answer("What is the pressure ratio?", "Tiger 30:150 has a pressure ratio of 30:1."))
    assert result["answer"] == "30:1"
    assert result["provider_error"] is False


def test_generation_service_returns_unavailable_for_empty_context() -> None:
    mock_provider = AsyncMock()
    service = GenerationService(llm_provider=mock_provider)
    import asyncio

    result = asyncio.run(service.generate_answer("What is the pressure ratio?", ""))
    assert result["answer"] == ANSWER_UNAVAILABLE
    assert result["provider_error"] is False
    mock_provider.generate.assert_not_called()


def test_generation_service_handles_provider_failure() -> None:
    mock_provider = AsyncMock()
    mock_provider.generate.side_effect = RuntimeError("Groq unavailable")
    service = GenerationService(llm_provider=mock_provider)
    import asyncio

    result = asyncio.run(service.generate_answer("What is the pressure ratio?", "Tiger 30:150"))
    assert "unable to generate" in result["answer"]
    assert result["provider_error"] is True


def test_generation_service_uses_answer_unavailable_for_none_response() -> None:
    mock_provider = AsyncMock()
    mock_provider.generate.return_value = ""
    service = GenerationService(llm_provider=mock_provider)
    import asyncio

    result = asyncio.run(service.generate_answer("What is the pressure ratio?", "Tiger 30:150"))
    assert result["answer"] == ANSWER_UNAVAILABLE
