"""Deterministic mock GenerationService for Phase 10 evaluation."""
from __future__ import annotations
from typing import Any, Dict, List
from app.rag.generation.prompts import ANSWER_UNAVAILABLE


class MockGenerationService:
    provider_name = "mock"
    model_name = "mock-deterministic"

    def __init__(self, echo_context: bool = True) -> None:
        self.echo_context = echo_context
        self.calls: List[Dict[str, Any]] = []

    def _record(self, method: str, **kwargs: Any) -> None:
        self.calls.append({"method": method, **kwargs})

    async def generate_answer(self, question, context, conversation_context=""):
        self._record("generate_answer", question=question, context=context, conversation_context=conversation_context)
        if not context or not context.strip():
            return {"answer": ANSWER_UNAVAILABLE, "sources": [], "provider_error": False}
        return {"answer": context if self.echo_context else context[:120], "sources": [], "provider_error": False}

    async def generate_general_answer(self, question, conversation_history=""):
        self._record("generate_general_answer", question=question, conversation_history=conversation_history)
        return {"answer": f"GENERAL-CHAT-MOCK:{question}", "sources": [], "provider_error": False}

    def reset(self):
        self.calls.clear()


def make_mock_generator():
    return MockGenerationService()