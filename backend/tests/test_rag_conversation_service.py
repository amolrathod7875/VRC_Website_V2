"""Tests for the stateless ConversationService."""
import uuid
from app.rag.conversation.conversation_service import ConversationService


def make_message(role: str, content: str, sources=None, retrieval_metadata=None):
    return {
        "role": role,
        "content": content,
        "sources": sources or [],
        "retrieval_metadata": retrieval_metadata or {},
    }


def test_generate_conversation_id_returns_string() -> None:
    id1 = ConversationService.generate_conversation_id()
    id2 = ConversationService.generate_conversation_id()
    assert isinstance(id1, str)
    assert isinstance(uuid.UUID(id1), uuid.UUID)  # valid UUID string
    assert id1 != id2  # unique


def test_validate_history_filters_invalid_messages() -> None:
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "invalid", "content": "Should be filtered"},
        {"role": "user", "content": ""},  # empty content
        {"role": "assistant", "content": "Valid response"},
        "not a dict",
        {"role": "user"},  # no content
    ]
    result = ConversationService.validate_history(messages)
    assert len(result) == 2
    assert result[0]["role"] == "user"
    assert result[0]["content"] == "Hello"
    assert result[1]["role"] == "assistant"


def test_validate_history_preserves_sources_for_assistant() -> None:
    sources = [{"document": "Tiger.pdf", "model": "30:150"}]
    messages = [
        {"role": "user", "content": "What is Tiger 30:150?"},
        {"role": "assistant", "content": "It's a pump.", "sources": sources, "retrieval_metadata": {"key": "val"}},
    ]
    result = ConversationService.validate_history(messages)
    assert result[1]["sources"] == sources
    assert result[1]["retrieval_metadata"] == {"key": "val"}


def test_validate_history_truncates_long_content() -> None:
    long_content = "x" * 5000
    messages = [{"role": "user", "content": long_content}]
    result = ConversationService.validate_history(messages)
    assert len(result[0]["content"]) == 4000


def test_validate_history_limits_to_max_messages() -> None:
    messages = [{"role": "user", "content": f"msg {i}"} for i in range(15)]
    result = ConversationService.validate_history(messages)
    assert len(result) == 8


def test_validate_history_empty_returns_empty() -> None:
    assert ConversationService.validate_history([]) == []
    assert ConversationService.validate_history(None) == []


def test_get_active_product_context_tracks_from_sources() -> None:
    messages = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Here it is.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"


def test_build_augmented_query_adds_context_for_ambiguous_followup() -> None:
    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Here it is.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = ConversationService.build_augmented_query("What is its output?", recent, ctx)
    assert "tiger" in augmented
    assert "30:150" in augmented
    assert "output" in augmented


def test_build_augmented_query_does_not_augment_clear_questions() -> None:
    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Here it is.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = ConversationService.build_augmented_query("When was VR Coatings founded?", recent, ctx)
    assert augmented == "When was VR Coatings founded?"


def test_build_generation_context_separates_history_from_evidence() -> None:
    recent = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Tiger 30:150 outputs 150 cc.", sources=[{"document": "Tiger.pdf", "model": "30:150"}]),
    ]
    retrieval = "Tiger 30:150 output per cycle: 150 cc."

    context = ConversationService.build_generation_context(recent, retrieval)
    assert "CONVERSATION HISTORY" in context
    assert "RETRIEVED KNOWLEDGE" in context
    assert "authoritative" in context.lower()


def test_get_active_product_context_preserves_model_across_same_product_followup() -> None:
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

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"


def test_get_active_product_context_clears_model_on_product_switch() -> None:
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

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "lion"
    assert ctx["model"] is None
    assert ctx["document"] == "LION_Catalogue.pdf"


def test_build_augmented_query_preserves_model_for_technical_followup() -> None:
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

    augmented = ConversationService.build_augmented_query("And pressure ratio?", recent, ctx)
    assert "tiger" in augmented
    assert "30:150" in augmented
    assert "pressure ratio" in augmented


def test_conversations_remain_isolated_via_stateless_design() -> None:
    """Stateless design: no session isolation issues since context comes from request."""
    assert ConversationService.get_active_product_context([]) == {
        "product_slug": None, "model": None, "document": None
    }


def test_exact_tiger_30_150_preserved_in_active_context() -> None:
    messages = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Tiger 30:150 outputs 150 cc.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
        make_message("user", "What is its output?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"


def test_price_question_does_not_inject_old_product_price() -> None:
    messages = [
        make_message("user", "How much does Tiger 30:150 cost?"),
        make_message("assistant", "Price is unavailable.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
        make_message("user", "How much does LION cost?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "lion"
    assert ctx["model"] is None


def test_unknown_product_does_not_inherit_previous_specs() -> None:
    messages = [
        make_message("user", "Tell me about Tiger 30:150."),
        make_message("assistant", "Tiger 30:150 outputs 150 cc.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
        make_message("user", "What is WidgetX?"),
    ]

    ctx = ConversationService.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"


def test_augmented_query_does_not_append_stale_identifiers() -> None:
    recent = [
        make_message("assistant", "Tiger 30:150 details.", sources=[{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}]),
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = ConversationService.build_augmented_query("Tell me about LION.", recent, ctx)
    assert "tiger" not in augmented.lower()
    assert "30:150" not in augmented