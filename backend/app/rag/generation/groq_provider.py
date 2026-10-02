import os
import time
import logging
import asyncio
from typing import Any, Dict, Optional
from groq import AsyncGroq, APIConnectionError, APIStatusError
from app.rag.config import rag_settings
from app.rag.generation.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GroqProvider(BaseLLMProvider):
    MAX_RETRIES = 2
    RETRY_BASE_DELAY = 1.0
    RETRY_MAX_DELAY = 10.0

    def __init__(self) -> None:
        self.api_key = rag_settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        self.model = rag_settings.GROQ_MODEL or os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        self.client = AsyncGroq(api_key=self.api_key, timeout=60.0)
        self._provider_name = "groq"

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def model_name(self) -> str:
        return self.model

    async def _call_with_retry(self, payload: Dict[str, Any]) -> Any:
        attempt = 0
        last_exc: Optional[Exception] = None
        while attempt <= self.MAX_RETRIES:
            try:
                return await self.client.chat.completions.create(**payload)
            except APIStatusError as exc:
                status = exc.status_code
                last_exc = exc
                if status == 429 or status >= 500:
                    retry_after = 0.0
                    try:
                        headers = exc.response.headers if exc.response else {}
                        retry_after = float(headers.get("retry-after", 0))
                    except Exception:
                        retry_after = 0.0
                    delay = min(self.RETRY_BASE_DELAY * (2 ** attempt) + retry_after, self.RETRY_MAX_DELAY)
                    logger.warning(
                        "Groq transient error %s on attempt %s/%s; retrying in %ss",
                        status,
                        attempt + 1,
                        self.MAX_RETRIES + 1,
                        round(delay, 2),
                        extra={
                            "provider": self._provider_name,
                            "model": self.model,
                            "provider_error": True,
                            "retry_attempt": attempt + 1,
                            "http_status": status,
                        },
                    )
                    await asyncio.sleep(delay)
                    attempt += 1
                    continue
                raise
            except (APIConnectionError, TimeoutError) as exc:
                last_exc = exc
                delay = min(self.RETRY_BASE_DELAY * (2 ** attempt), self.RETRY_MAX_DELAY)
                logger.warning(
                    "Groq connection error on attempt %s/%s; retrying in %ss: %s",
                    attempt + 1,
                    self.MAX_RETRIES + 1,
                    round(delay, 2),
                    exc,
                    extra={
                        "provider": self._provider_name,
                        "model": self.model,
                        "provider_error": True,
                        "retry_attempt": attempt + 1,
                    },
                )
                await asyncio.sleep(delay)
                attempt += 1
                continue
            except Exception as exc:
                raise RuntimeError(f"Groq generation unexpected error: {exc}") from exc
        raise RuntimeError(f"Groq generation failed after retries: {last_exc}") from last_exc

    async def generate(self, system_prompt: str, user_prompt: str, context: str) -> str:
        if not context or not context.strip():
            raise ValueError("Context is empty")
        start = time.perf_counter()
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{user_prompt}\n\nContext:\n{context}"},
                ],
                "temperature": 0.0,
                "max_tokens": 1024,
            }
            response = await self._call_with_retry(payload)
            latency_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "Groq generation completed",
                extra={
                    "provider": self._provider_name,
                    "model": self.model,
                    "latency_ms": round(latency_ms, 2),
                    "provider_error": False,
                    "retry_attempt": 0,
                },
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            logger.error(
                "Groq generation failed: %s",
                exc,
                extra={
                    "provider": self._provider_name,
                    "model": self.model,
                    "latency_ms": round(latency_ms, 2),
                    "provider_error": True,
                },
            )
            raise RuntimeError(f"Groq generation failed: {exc}") from exc
