from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.rag.retrieval.query_classifier import QueryIntent

client = TestClient(app)


def test_chat_endpoint_general_chat_bypasses_rag() -> None:
    mock_generator = AsyncMock()
    mock_generator.generate_general_answer.return_value = {
        "answer": "Artificial intelligence is a field of computer science.",
        "sources": [],
        "retrieval": None,
        "intent": "general_chat",
    }

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_generator):
        with patch("app.api.v1.endpoints.chat.is_vr_coatings_domain_query", return_value=False):
            response = client.post("/api/v1/chat", json={"message": "What is artificial intelligence?"})

    assert response.status_code == 200
    data = response.json()
    assert "artificial intelligence" in data["answer"].lower()
    assert data["sources"] == []
    assert data["show_sources"] is False
    assert data["intent"] == "general_chat"
    mock_generator.generate_general_answer.assert_called_once()


def test_chat_endpoint_identity_returns_deterministic() -> None:
    response = client.post("/api/v1/chat", json={"message": "what's your name"})

    assert response.status_code == 200
    data = response.json()
    assert "VR Coatings Assistant" in data["answer"]
    assert data["show_sources"] is False
    assert data["intent"] == "assistant_identity"


def test_chat_endpoint_general_side_turn_preserves_product_context() -> None:
    mock_generator = AsyncMock()
    mock_generator.generate_general_answer.return_value = {
        "answer": "Machine learning is a subset of AI.",
        "sources": [],
        "retrieval": None,
        "intent": "general_chat",
    }

    existing_id = uuid4()
    history = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
    ]

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_generator):
        with patch("app.api.v1.endpoints.chat.is_vr_coatings_domain_query", return_value=False):
            response = client.post("/api/v1/chat", json={"message": "What is machine learning?", "conversation_id": str(existing_id), "history": history})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "general_chat"
    assert data["show_sources"] is False
    mock_generator.generate_general_answer.assert_called_once()


def test_chat_endpoint_general_chat_general_failure() -> None:
    mock_generator = AsyncMock()
    mock_generator.generate_general_answer.side_effect = RuntimeError("Groq unavailable")

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_generator):
        with patch("app.api.v1.endpoints.chat.is_vr_coatings_domain_query", return_value=False):
            response = client.post("/api/v1/chat", json={"message": "Explain machine learning."})

    assert response.status_code == 500