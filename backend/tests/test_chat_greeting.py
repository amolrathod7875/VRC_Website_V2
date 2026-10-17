from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_greeting_bypasses_rag() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        mock_cs.build_augmented_query = MagicMock(return_value="hey")
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "hey"})

    assert response.status_code == 200
    data = response.json()
    assert "Hey!" in data["answer"]
    assert data["sources"] == []
    assert data["show_sources"] is False
    assert data["intent"] == "greeting"


def test_chat_endpoint_greeting_hello() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "hello"})

    assert response.status_code == 200
    data = response.json()
    assert "Hello!" in data["answer"]
    assert data["show_sources"] is False
    assert data["intent"] == "greeting"


def test_chat_endpoint_greeting_plus_product_query_runs_rag() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "Tiger 30:150 is a spray pump.",
        "sources": [{"document": "Tiger.pdf", "source_type": "catalogue", "model": "30:150", "product_slug": "tiger"}],
        "retrieval": {"chunks_used": 2},
        "intent": "product_technical",
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
            mock_cs.validate_history = MagicMock(return_value=[])
            mock_cs.get_active_product_context = MagicMock(return_value={})
            mock_cs.build_augmented_query = MagicMock(return_value="tell me about tiger 30:150")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "Hi, tell me about Tiger 30:150."})

    assert response.status_code == 200
    data = response.json()
    assert "Tiger" in data["answer"]
    mock_service.answer.assert_called_once()
    assert data["intent"] == "product_technical"


def test_chat_endpoint_greeting_how_are_you() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "how are you?"})

    assert response.status_code == 200
    data = response.json()
    assert "I'm doing well" in data["answer"]
    assert data["show_sources"] is False


def test_chat_endpoint_greeting_thanks() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "thanks"})

    assert response.status_code == 200
    data = response.json()
    assert "You're welcome" in data["answer"]
    assert data["show_sources"] is False


def test_chat_endpoint_greeting_bye() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
        mock_cs.validate_history = MagicMock(return_value=[])
        mock_cs.get_active_product_context = MagicMock(return_value={})
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "bye"})

    assert response.status_code == 200
    data = response.json()
    assert "Goodbye" in data["answer"]
    assert data["show_sources"] is False


def test_chat_endpoint_greeting_inside_product_conversation() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.generate_conversation_id = MagicMock(return_value="test-conv-id")
        mock_cs.validate_history = MagicMock(return_value=[
            {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
            {"role": "assistant", "content": "Tiger 30:150 is a spray pump.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        ])
        mock_cs.get_active_product_context = MagicMock(return_value={"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"})
        mock_cs.build_augmented_query = MagicMock(return_value="thanks")
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "thanks", "conversation_id": "test-conv-id"})

    assert response.status_code == 200
    data = response.json()
    assert "You're welcome" in data["answer"]
    assert data["show_sources"] is False
