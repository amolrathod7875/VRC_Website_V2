from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_validates_empty_message() -> None:
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_endpoint_returns_structured_response() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "30:1",
        "sources": [{"document": "Tiger.pdf", "source_type": "catalogue", "model": "30:150"}],
        "retrieval": {"chunks_used": 4},
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio of Tiger 30:150?"})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "30:1"
    assert len(data["sources"]) == 1
    assert data["retrieval"]["chunks_used"] == 4


def test_chat_endpoint_no_context_returns_unavailable() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "This information is not available in the current VR Coatings knowledge base.",
        "sources": [],
        "retrieval": {"chunks_used": 0},
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio?"})

    assert response.status_code == 200
    data = response.json()
    assert "not available" in data["answer"]
    assert data["retrieval"]["chunks_used"] == 0


def test_chat_endpoint_provider_failure_returns_error() -> None:
    mock_service = AsyncMock()
    mock_service.answer.side_effect = RuntimeError("Groq unavailable")

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio?"})

    assert response.status_code == 500


def test_chat_endpoint_missing_retrieval_metadata() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "30:1",
        "sources": [],
        "retrieval": None,
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "test"})

    assert response.status_code == 200
    data = response.json()
    assert data["retrieval"] is None
