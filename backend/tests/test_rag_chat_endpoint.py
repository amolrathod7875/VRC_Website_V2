from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.main import app
from app.core.database import Base
from app.models import rag_document

client = TestClient(app)


def test_chat_endpoint_validates_empty_message() -> None:
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422
