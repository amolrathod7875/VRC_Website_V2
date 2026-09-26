from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg://vrcoatings:vrcoatings@postgres:5432/vrcoatings"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"
    MEDIA_ROOT: str = "/app/storage"
    API_V1_STR: str = "/api/v1"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]


settings = Settings()
