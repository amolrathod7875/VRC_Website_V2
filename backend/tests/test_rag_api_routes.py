from unittest.mock import AsyncMock, patch
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

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
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
