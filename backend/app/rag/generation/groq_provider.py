import os
import logging
from typing import Any, Dict, Optional
from groq import AsyncGroq
from app.rag.config import rag_settings
from app.rag.generation.base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GroqProvider(BaseLLMProvider):
    def __init__(self) -> None:
        self.api_key = rag_settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        self.model = rag_settings.GROQ_MODEL or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client = AsyncGroq(api_key=self.api_key)

    async def generate(self, system_prompt: str, user_prompt: str, context: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n\nContext:\n{context}"},
            ],
        )
        return response.choices[0].message.content or ""
