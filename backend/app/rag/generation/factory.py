from app.rag.generation.groq_provider import GroqProvider
from app.rag.config import rag_settings


class LLMFactory:
    @staticmethod
    def create():
        provider = (rag_settings.LLM_PROVIDER or "groq").lower().strip()
        if provider == "groq":
            return GroqProvider()
        raise ValueError(f"Unsupported LLM provider: {provider}")
