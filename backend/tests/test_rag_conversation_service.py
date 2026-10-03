import asyncio
import json
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.rag.conversation.conversation_service import ConversationService


def make_message(role: str, content: str, sources=None, retrieval_metadata=None):
    return {
        "role": role,
        "content": content,
        "sources": sources or [],
        "retrieval_metadata": retrieval_metadata or {},
    }


def test_get_or_create_conversation_creates_new() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    db.add = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()

    mock_conversation = MagicMock()
    mock_conversation.id = uuid.uuid4()

    db.add.side_effect = lambda obj: setattr(obj, "id", mock_conversation.id)

    async def run():
        result = await service.get_or_create_conversation(None)
        assert result is not None

    asyncio.run(run())
    db.add.assert_called_once()


def test_append_user_message() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    db.add = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()

    cid = uuid.uuid4()

    async def run():
        await service.append_user_message(cid, "Test question")

    asyncio.run(run())
    db.add.assert_called_once()
    added = db.add.call_args[0][0]
    assert added.role == "user"
    assert added.content == "Test question"
    assert added.conversation_id == cid


def test_append_assistant_message() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    db.add = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()

    cid = uuid.uuid4()
    sources = [{"document": "Tiger.pdf", "model": "30:150"}]
    retrieval = {"chunks_used": 2}

    async def run():
        await service.append_assistant_message(cid, "30:1", sources, retrieval)

    asyncio.run(run())
    db.add.assert_called_once()
    added = db.add.call_args[0][0]
    assert added.role == "assistant"
    assert added.content == "30:1"
    assert json.loads(added.sources) == sources
    assert json.loads(added.retrieval_metadata) == retrieval


def test_get_recent_messages_returns_bounded() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    rows = []
    for i in range(6):
        row = MagicMock()
        row.role = "user" if i % 2 == 0 else "assistant"
        row.content = f"Message {i}"
        row.sources = json.dumps([]) if i % 2 == 1 else None
        row.retrieval_metadata = json.dumps({}) if i % 2 == 1 else None
        rows.append(row)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = rows
    db.execute = AsyncMock(return_value=mock_result)

    cid = uuid.uuid4()

    async def run():
        messages = await service.get_recent_messages(cid, limit=6)
        assert len(messages) == 6
        assert messages[0]["content"] == "Message 5"
        assert messages[-1]["content"] == "Message 0"

    asyncio.run(run())


def test_get_active_product_context_tracks_from_sources() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Here it is.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"


def test_build_augmented_query_adds_context_for_ambiguous_followup() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Here it is.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = service.build_augmented_query("What is its output?", recent, ctx)
    assert "tiger" in augmented
    assert "30:150" in augmented
    assert "output" in augmented


def test_build_augmented_query_does_not_augment_clear_questions() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Here it is.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = service.build_augmented_query("When was VR Coatings founded?", recent, ctx)
    assert augmented == "When was VR Coatings founded?"


def test_build_generation_context_separates_history_from_evidence() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Tiger 30:150 outputs 150 cc.", sources=[{"document": "Tiger.pdf", "model": "30:150"}]),
    ]
    retrieval = "Tiger 30:150 output per cycle: 150 cc."

    context = service.build_generation_context(recent, retrieval)
    assert "CONVERSATION HISTORY" in context
    assert "RETRIEVED KNOWLEDGE" in context
    assert "authoritative" in context.lower()


def test_get_active_product_context_preserves_model_across_same_product_followup() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message(
            "assistant",
            "Tiger 30:150 outputs 150 cc.",
            sources=[
                {"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"},
            ],
        ),
        make_message(
            "user",
            "What is its output?",
        ),
        make_message(
            "assistant",
            "150 cc",
            sources=[
                {"document": "Tiger.pdf", "product_slug": "tiger", "model": None},
                {"document": "rhino.pdf", "product_slug": "rhino", "model": "75:210"},
            ],
        ),
        make_message("user", "And pressure ratio?"),
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"


def test_get_active_product_context_clears_model_on_product_switch() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message(
            "assistant",
            "Tiger 30:150 outputs 150 cc.",
            sources=[
                {"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"},
            ],
        ),
        make_message("user", "Now tell me about LION."),
        make_message(
            "assistant",
            "LION is a hydraulic pump.",
            sources=[
                {"document": "LION_Catalogue.pdf", "product_slug": "lion", "model": None},
            ],
        ),
        make_message("user", "What is its pressure ratio?"),
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "lion"
    assert ctx["model"] is None
    assert ctx["document"] == "LION_Catalogue.pdf"


def test_build_augmented_query_preserves_model_for_technical_followup() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message(
            "assistant",
            "Tiger 30:150 outputs 150 cc.",
            sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}],
        ),
        make_message("user", "What is its output?"),
        make_message(
            "assistant",
            "150 cc",
            sources=[
                {"document": "Tiger.pdf", "product_slug": "tiger", "model": None},
            ],
        ),
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = service.build_augmented_query("And pressure ratio?", recent, ctx)
    assert "tiger" in augmented
    assert "30:150" in augmented
    assert "pressure ratio" in augmented


def test_conversations_do_not_leak_between_sessions() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    db.execute = AsyncMock(return_value=mock_result)

    cid1 = uuid.uuid4()
    cid2 = uuid.uuid4()

    async def run():
        msgs1 = await service.get_recent_messages(cid1, limit=4)
        msgs2 = await service.get_recent_messages(cid2, limit=4)
        assert msgs1 == []
        assert msgs2 == []

    asyncio.run(run())
