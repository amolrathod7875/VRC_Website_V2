import time
import logging
from typing import Any, Dict, List
from app.rag.config import rag_settings
from app.rag.generation.base import BaseLLMProvider
from app.rag.generation.factory import LLMFactory
from app.rag.generation.prompts import SYSTEM_PROMPT, GENERAL_CHAT_SYSTEM_PROMPT, ANSWER_UNAVAILABLE

logger = logging.getLogger(__name__)


class GenerationService:
    def __init__(self, llm_provider: BaseLLMProvider) -> None:
        self.llm_provider = llm_provider

    async def generate_answer(self, question: str, context: str, conversation_context: str = "") -> Dict[str, Any]:
        if not context or not context.strip():
            return {
                "answer": ANSWER_UNAVAILABLE,
                "sources": [],
                "provider_error": False,
            }

        if conversation_context and conversation_context.strip():
            full_context = f"{conversation_context}\n\n{context}"
        else:
            full_context = context

        user_prompt = f"Question: {question}"
        gen_start = time.perf_counter()
        try:
            answer = await self.llm_provider.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                context=context,
            )
        except Exception as exc:
            latency_ms = (time.perf_counter() - gen_start) * 1000
            logger.error(
                "Generation provider error: %s",
                exc,
                extra={
                    "provider": getattr(self.llm_provider, "provider_name", type(self.llm_provider).__name__),
                    "model": getattr(self.llm_provider, "model_name", "unknown"),
                    "latency_ms": round(latency_ms, 2),
                    "provider_error": True,
                },
            )
            return {
                "answer": "I'm currently unable to generate an answer. Please try again later.",
                "sources": [],
                "provider_error": True,
            }

        latency_ms = (time.perf_counter() - gen_start) * 1000
        logger.info(
            "Generation completed",
            extra={
                "provider": getattr(self.llm_provider, "provider_name", type(self.llm_provider).__name__),
                "model": getattr(self.llm_provider, "model_name", "unknown"),
                "latency_ms": round(latency_ms, 2),
                "provider_error": False,
            },
        )
        return {
            "answer": answer or ANSWER_UNAVAILABLE,
            "sources": [],
            "provider_error": False,
        }

    async def generate_general_answer(
        self,
        question: str,
        conversation_history: str = "",
    ) -> Dict[str, Any]:
        if conversation_history and conversation_history.strip():
            user_prompt = f"{conversation_history}\n\nQuestion: {question}"
        else:
            user_prompt = f"Question: {question}"

        gen_start = time.perf_counter()
        try:
            answer = await self.llm_provider.generate(
                system_prompt=GENERAL_CHAT_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                context="",
            )
        except Exception as exc:
            latency_ms = (time.perf_counter() - gen_start) * 1000
            logger.error(
                "General chat generation error: %s",
                exc,
                extra={
                    "provider": getattr(self.llm_provider, "provider_name", type(self.llm_provider).__name__),
                    "model": getattr(self.llm_provider, "model_name", "unknown"),
                    "latency_ms": round(latency_ms, 2),
                    "provider_error": True,
                },
            )
            return {
                "answer": "I'm currently unable to generate an answer. Please try again later.",
                "sources": [],
                "provider_error": True,
            }

        latency_ms = (time.perf_counter() - gen_start) * 1000
        logger.info(
            "General chat generation completed",
            extra={
                "provider": getattr(self.llm_provider, "provider_name", type(self.llm_provider).__name__),
                "model": getattr(self.llm_provider, "model_name", "unknown"),
                "latency_ms": round(latency_ms, 2),
                "provider_error": False,
            },
        )
        return {
            "answer": answer or "",
            "sources": [],
            "provider_error": False,
        }
