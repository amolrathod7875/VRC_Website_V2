from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_general_chat_bypasses_rag() -> None:
    mock_generator = AsyncMock()
    mock_generator.answer_general.return_value = {
        "answer": "Artificial intelligence is a field of computer science.",
        "sources": [],
        "retrieval": {
            "chunks_used": 0,
            "retrieval_duration_ms": 0.0,
            "generation_duration_ms": 0.0,
            "total_duration_ms": 0.0,
            "provider_error": False,
        },
        "intent": "general_chat",
    }

    mock_conversation = MagicMock()
    mock_conversation.id = uuid4()

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_generator):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[])
            mock_cs.get_active_product_context = MagicMock(return_value={})
            mock_cs.build_augmented_query = MagicMock(return_value="What is AI?")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is artificial intelligence?"})

    assert response.status_code == 200
    data = response.json()
    assert "artificial intelligence" in data["answer"].lower()
    assert data["sources"] == []
    assert data["show_sources"] is False
    assert data["intent"] == "general_chat"
    mock_generator.answer_general.assert_called_once()


def test_chat_endpoint_identity_returns_deterministic() -> None:
    mock_conversation = MagicMock()
    mock_conversation.id = uuid4()

    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
        mock_cs.append_user_message = AsyncMock()
        mock_cs.append_assistant_message = AsyncMock()
        mock_cs.get_recent_messages = AsyncMock(return_value=[])
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "what's your name"})

    assert response.status_code == 200
    data = response.json()
    assert "VR Coatings Assistant" in data["answer"]
    assert data["show_sources"] is False
    assert data["intent"] == "assistant_identity"


def test_chat_endpoint_general_side_turn_preserves_product_context() -> None:
    mock_generator = AsyncMock()
    mock_generator.answer_general.return_value = {
        "answer": "Machine learning is a subset of AI.",
        "sources": [],
        "retrieval": {
            "chunks_used": 0,
            "retrieval_duration_ms": 0.0,
            "generation_duration_ms": 0.0,
            "total_duration_ms": 0.0,
            "provider_error": False,
        },
        "intent": "general_chat",
    }

    existing_id = uuid4()
    mock_conversation = MagicMock()
    mock_conversation.id = existing_id

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_generator):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[
                {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
                {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
            ])
            mock_cs.get_active_product_context = MagicMock(return_value={"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"})
            mock_cs.build_augmented_query = MagicMock(return_value="What is machine learning?")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is machine learning?", "conversation_id": str(existing_id)})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "general_chat"
    assert data["show_sources"] is False
    mock_generator.answer_general.assert_called_once()


def test_chat_endpoint_general_chat_general_failure() -> None:
    mock_generator = AsyncMock()
    mock_generator.answer_general.side_effect = RuntimeError("Groq unavailable")

    mock_conversation = MagicMock()
    mock_conversation.id = uuid4()

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_generator):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[])
            mock_cs.get_active_product_context = MagicMock(return_value={})
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "Explain machine learning."})

    assert response.status_code == 500
