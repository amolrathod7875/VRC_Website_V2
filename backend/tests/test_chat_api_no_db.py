"""Test that the chat API works without PostgreSQL configured.

In the PostgreSQL-free migration, the chat endpoint should function correctly
even when DATABASE_URL is not set, since ConversationService is stateless
and all document state lives in Qdrant.
"""
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


def test_chat_api_works_without_database_url():
    """Chat endpoint should work when DATABASE_URL is not set."""
    if os.environ.get("DATABASE_URL"):
        os.environ.pop("DATABASE_URL", None)

    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-no-db-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        mock_cs.build_augmented_query = MagicMock(return_value="hi")
        MockConvService.return_value = mock_cs

        from app.main import app
        client = TestClient(app)
        response = client.post("/api/v1/chat", json={"message": "hi"})

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == "test-no-db-id"
    assert "answer" in data
    assert data["show_sources"] is False


def test_chat_api_greeting_without_database_url():
    """Greeting responses work without PostgreSQL."""
    if os.environ.get("DATABASE_URL"):
        os.environ.pop("DATABASE_URL", None)

    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-greeting-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        mock_cs.build_augmented_query = MagicMock(return_value="hello")
        MockConvService.return_value = mock_cs

        from app.main import app
        client = TestClient(app)
        response = client.post("/api/v1/chat", json={"message": "hello"})

    assert response.status_code == 200
    data = response.json()
    assert "Hello" in data["answer"]
    assert data["intent"] == "greeting"
    assert data["sources"] == []


def test_chat_api_status_endpoint_without_database_url():
    """Status endpoint should work without PostgreSQL."""
    if os.environ.get("DATABASE_URL"):
        os.environ.pop("DATABASE_URL", None)

    from app.main import app
    client = TestClient(app)
    response = client.get("/api/v1/chat/status")

    assert response.status_code == 200
    data = response.json()
    assert "rag_ready" in data
    assert "generation_ready" in data
    assert "indexed_documents" in data
