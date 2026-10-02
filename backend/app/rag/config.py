import pydantic_settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path


class SettingsProxy:
    def __getattr__(self, name: str) -> str:
        try:
            from app.core.config import settings as main_settings
            return getattr(main_settings, name)
        except Exception:
            return ""


class RagSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent.parent.parent.parent / ".env"), extra="ignore")

    DATABASE_URL: str = ""
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "vr_coatings_knowledge"

    RAG_DENSE_MODEL: str = "BAAI/bge-small-en-v1.5"
    RAG_SPARSE_MODEL: str = "Qdrant/bm25"

    RAG_DENSE_TOP_K: int = 20
    RAG_SPARSE_TOP_K: int = 20
    RAG_FINAL_TOP_K: int = 8
    RAG_RERANK_ENABLED: bool = False

    RAG_EMBED_BATCH_SIZE: int = 64
    RAG_QDRANT_UPSERT_BATCH_SIZE: int = 64

    RAG_CATALOGUE_ROOT: str = "/app/storage/catalogues"
    RAG_COMPANY_KB_PATH: str = "/app/storage/knowledge/VR_Coatings_RAG_Monolithic_Knowledge_Base.txt"

    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "qwen/qwen3.8-27b"

    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        try:
            from app.core.config import settings as main_settings
            return getattr(main_settings, "DATABASE_URL", "")
        except Exception:
            return ""


rag_settings = RagSettings()
