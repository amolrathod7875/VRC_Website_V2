from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_post_works() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "30:1",
        "sources": [{"document": "Tiger.pdf", "source_type": "catalogue", "model": "30:150"}],
        "retrieval": {"chunks_used": 4},
    }

    mock_conversation = MagicMock()
    mock_conversation.id = uuid4()

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[])
            mock_cs.get_active_product_context = MagicMock(return_value={})
            mock_cs.build_augmented_query = MagicMock(return_value="What is the pressure ratio of Tiger 30:150?")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio of Tiger 30:150?"})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "30:1"
    assert len(data["sources"]) == 1
    assert data["retrieval"]["chunks_used"] == 4


def test_chat_status_endpoint_works() -> None:
    response = client.get("/api/v1/chat/status")
    assert response.status_code == 200
    data = response.json()
    assert "rag_ready" in data
    assert "generation_ready" in data
