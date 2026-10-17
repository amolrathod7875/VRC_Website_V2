from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.rag.retrieval.query_classifier import QueryIntent

client = TestClient(app)


def test_chat_endpoint_validates_empty_message() -> None:
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_endpoint_returns_conversation_id() -> None:
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
    assert "conversation_id" in data


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
        response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio of Tiger 30:150?"})

    assert response.status_code == 200
    data = response.json()
    assert data["retrieval"] is None


def test_chat_endpoint_existing_conversation_continues() -> None:
    existing_id = uuid4()
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "1985",
        "sources": [],
        "retrieval": {"chunks_used": 1},
    }

    # Provide history to simulate existing conversation
    history = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 is a spray pump.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
    ]

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "What is its output?", "conversation_id": str(existing_id), "history": history})

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == str(existing_id)


def test_chat_endpoint_augments_followup_query() -> None:
    existing_id = uuid4()
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "150 cc",
        "sources": [{"document": "Tiger.pdf", "source_type": "catalogue", "model": "30:150"}],
        "retrieval": {"chunks_used": 2},
    }

    history = [
        {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
    ]

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "What is its output?", "conversation_id": str(existing_id), "history": history})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "150 cc"


def test_chat_endpoint_topic_switch_resets_active_context() -> None:
    existing_id = uuid4()
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "1985",
        "sources": [{"document": "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt", "source_type": "company_master"}],
        "retrieval": {"chunks_used": 1},
    }

    history = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "When was VR Coatings founded?", "sources": [], "retrieval_metadata": {}},
    ]

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "When was VR Coatings founded?", "conversation_id": str(existing_id), "history": history})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "1985"


def test_chat_endpoint_catalogue_request_bypasses_rag() -> None:
    with patch("app.api.v1.endpoints.chat._build_rag_service") as mock_rag:
        with patch("app.api.v1.endpoints.chat.CatalogueResolver") as MockResolver:
            mock_resolver = AsyncMock()
            mock_resolver.resolve_from_message = AsyncMock(return_value=("rhino", [{"product_slug": "rhino", "product_name": "Rhino", "document_name": "rhino.pdf", "url": "/media/catalogues/rhino.pdf"}]))
            MockResolver.return_value = mock_resolver

            response = client.post("/api/v1/chat", json={"message": "give me catalogue of rhino"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "catalogue_request"
    assert "Rhino" in data["answer"]
    assert data["show_sources"] is False
    assert data["sources"] == []
    assert data["retrieval"] is None
    assert len(data["catalogues"]) == 1
    assert data["catalogues"][0]["document_name"] == "rhino.pdf"
    mock_rag.assert_not_called()


def test_chat_endpoint_catalogue_request_tiger() -> None:
    with patch("app.api.v1.endpoints.chat._build_rag_service") as mock_rag:
        with patch("app.api.v1.endpoints.chat.CatalogueResolver") as MockResolver:
            mock_resolver = AsyncMock()
            mock_resolver.resolve_from_message = AsyncMock(return_value=("tiger", [{"product_slug": "tiger", "product_name": "Tiger", "document_name": "Tiger.pdf", "url": "/media/catalogues/Tiger.pdf"}]))
            MockResolver.return_value = mock_resolver

            response = client.post("/api/v1/chat", json={"message": "give me catalogue of Tiger"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "catalogue_request"
    assert "Tiger" in data["answer"]
    assert data["show_sources"] is False
    assert data["sources"] == []
    assert data["retrieval"] is None
    assert len(data["catalogues"]) == 1
    assert data["catalogues"][0]["document_name"] == "Tiger.pdf"
    mock_rag.assert_not_called()


def test_chat_endpoint_unknown_catalogue_returns_error() -> None:
    with patch("app.api.v1.endpoints.chat._build_rag_service") as mock_rag:
        with patch("app.api.v1.endpoints.chat.CatalogueResolver") as MockResolver:
            mock_resolver = AsyncMock()
            mock_resolver.resolve_from_message = AsyncMock(return_value=(None, []))
            MockResolver.return_value = mock_resolver

            response = client.post("/api/v1/chat", json={"message": "give me catalogue of Ferrari"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "catalogue_request"
    assert "couldn" in data["answer"].lower() and "find a vr coatings catalogue" in data["answer"].lower()
    assert data["show_sources"] is False
    assert data["sources"] == []
    assert data["retrieval"] is None
    assert data["catalogues"] == []
    mock_rag.assert_not_called()


def test_chat_endpoint_unavailable_clears_sources() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "This information is not available in the current VR Coatings knowledge base.",
        "sources": [{"document": "Tiger.pdf", "source_type": "catalogue", "product_slug": "tiger"}],
        "retrieval": {"chunks_used": 0},
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        response = client.post("/api/v1/chat", json={"message": "How much does Tiger cost?"})

    assert response.status_code == 200
    data = response.json()
    assert "not available" in data["answer"]
    assert data["show_sources"] is False
    assert data["sources"] == []


def test_chat_endpoint_greeting() -> None:
    with patch("app.api.v1.endpoints.chat._build_rag_service") as mock_rag:
        response = client.post("/api/v1/chat", json={"message": "hello"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "greeting"
    assert data["show_sources"] is False
    mock_rag.assert_not_called()


def test_chat_endpoint_assistant_identity() -> None:
    with patch("app.api.v1.endpoints.chat._build_rag_service") as mock_rag:
        response = client.post("/api/v1/chat", json={"message": "who are you"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "assistant_identity"
    assert data["show_sources"] is False
    mock_rag.assert_not_called()


def test_chat_endpoint_general_chat() -> None:
    mock_service = AsyncMock()
    mock_service.generate_general_answer.return_value = {
        "answer": "I am a helpful assistant.",
        "sources": [],
        "retrieval": None,
        "intent": "general_chat",
    }

    with patch("app.api.v1.endpoints.chat._build_generation_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.is_vr_coatings_domain_query", return_value=False):
            response = client.post("/api/v1/chat", json={"message": "What is the meaning of life?"})

    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "general_chat"