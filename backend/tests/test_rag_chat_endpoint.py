from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

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
    assert "conversation_id" in data


def test_chat_endpoint_returns_structured_response() -> None:
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


def test_chat_endpoint_no_context_returns_unavailable() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "This information is not available in the current VR Coatings knowledge base.",
        "sources": [],
        "retrieval": {"chunks_used": 0},
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
            mock_cs.build_augmented_query = MagicMock(return_value="What is the pressure ratio?")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio?"})

    assert response.status_code == 200
    data = response.json()
    assert "not available" in data["answer"]
    assert data["retrieval"]["chunks_used"] == 0


def test_chat_endpoint_provider_failure_returns_error() -> None:
    mock_service = AsyncMock()
    mock_service.answer.side_effect = RuntimeError("Groq unavailable")

    mock_conversation = MagicMock()
    mock_conversation.id = uuid4()

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[])
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is the pressure ratio?"})

    assert response.status_code == 500


def test_chat_endpoint_missing_retrieval_metadata() -> None:
    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "30:1",
        "sources": [],
        "retrieval": None,
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
            mock_cs.build_augmented_query = MagicMock(return_value="test")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "test"})

    assert response.status_code == 200
    data = response.json()
    assert data["retrieval"] is None


def test_chat_endpoint_invalid_conversation_id_returns_404() -> None:
    with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
        mock_cs = MagicMock()
        mock_cs.get_or_create_conversation = AsyncMock(side_effect=ValueError("Conversation not found"))
        MockConvService.return_value = mock_cs

        response = client.post("/api/v1/chat", json={"message": "test", "conversation_id": str(uuid4())})

    assert response.status_code == 404


def test_chat_endpoint_existing_conversation_continues() -> None:
    existing_id = uuid4()
    mock_conversation = MagicMock()
    mock_conversation.id = existing_id

    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "1985",
        "sources": [],
        "retrieval": {"chunks_used": 1},
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[
                {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
                {"role": "assistant", "content": "Tiger 30:150 is a spray pump.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
            ])
            mock_cs.get_active_product_context = MagicMock(return_value={"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"})
            mock_cs.build_augmented_query = MagicMock(return_value="What is its output?")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is its output?", "conversation_id": str(existing_id)})

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == str(existing_id)


def test_chat_endpoint_augments_followup_query() -> None:
    existing_id = uuid4()
    mock_conversation = MagicMock()
    mock_conversation.id = existing_id

    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "150 cc",
        "sources": [{"document": "Tiger.pdf", "source_type": "catalogue", "model": "30:150"}],
        "retrieval": {"chunks_used": 2},
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[
                {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
            ])
            mock_cs.get_active_product_context = MagicMock(return_value={"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"})
            mock_cs.build_augmented_query = MagicMock(return_value="What is its output? tiger 30:150")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "What is its output?", "conversation_id": str(existing_id)})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "150 cc"


def test_chat_endpoint_topic_switch_resets_active_context() -> None:
    existing_id = uuid4()
    mock_conversation = MagicMock()
    mock_conversation.id = existing_id

    mock_service = AsyncMock()
    mock_service.answer.return_value = {
        "answer": "1985",
        "sources": [{"document": "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt", "source_type": "company_master"}],
        "retrieval": {"chunks_used": 1},
    }

    with patch("app.api.v1.endpoints.chat._build_rag_service", return_value=mock_service):
        with patch("app.api.v1.endpoints.chat.ConversationService") as MockConvService:
            mock_cs = MagicMock()
            mock_cs.get_or_create_conversation = AsyncMock(return_value=mock_conversation)
            mock_cs.append_user_message = AsyncMock()
            mock_cs.append_assistant_message = AsyncMock()
            mock_cs.get_recent_messages = AsyncMock(return_value=[
                {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
                {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
                {"role": "user", "content": "When was VR Coatings founded?", "sources": [], "retrieval_metadata": {}},
            ])
            mock_cs.get_active_product_context = MagicMock(return_value={"product_slug": None, "model": None, "document": "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt"})
            mock_cs.build_augmented_query = MagicMock(return_value="When was VR Coatings founded?")
            MockConvService.return_value = mock_cs

            response = client.post("/api/v1/chat", json={"message": "When was VR Coatings founded?", "conversation_id": str(existing_id)})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "1985"
