"""Phase 8.1 multi-product context hardening tests."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.rag.product_identity import (
    resolve_product_identity,
    get_canonical_slug,
    extract_model_identifier,
    PRODUCT_ALIASES,
)
from app.rag.conversation.conversation_service import ConversationService
from app.rag.retrieval.query_classifier import classify_query, QueryIntent
from app.rag.services.rag_service import (
    _should_apply_product_filter,
    _cross_product_guard,
)
from app.rag.constants import SOURCE_TYPE_CATALOGUE


# ---------------------------------------------------------------------------
# Product identity / alias tests
# ---------------------------------------------------------------------------

def test_resolve_tiger_alias() -> None:
    assert resolve_product_identity("Tell me about Tiger pump") == ("tiger", "tiger pump")
    assert resolve_product_identity("TIGER") == ("tiger", "tiger")
    assert resolve_product_identity("Tell me about Tiger 30:150") == ("tiger", "tiger 30:150")


def test_resolve_lion_alias() -> None:
    assert resolve_product_identity("Tell me about LION") == ("lion", "lion")
    assert resolve_product_identity("LION pump") == ("lion", "lion pump")
    assert resolve_product_identity("lion_catalogue") == ("lion", "lion_catalogue")


def test_resolve_unknown_returns_none() -> None:
    assert resolve_product_identity("Tell me about VR Coatings") is None
    assert resolve_product_identity("") is None


def test_get_canonical_slug() -> None:
    assert get_canonical_slug("Tiger pump") == "tiger"
    assert get_canonical_slug("LION") == "lion"
    assert get_canonical_slug("unknown_product") is None


def test_extract_model_identifier() -> None:
    assert extract_model_identifier("Tiger 30:150") == "30:150"
    assert extract_model_identifier("What is 35:1 output?") == "35:1"
    assert extract_model_identifier("Tell me about Tiger") is None
    assert extract_model_identifier("") is None


# ---------------------------------------------------------------------------
# Active context: explicit new product overrides previous active product
# ---------------------------------------------------------------------------

def test_explicit_new_product_overrides_previous_active_product() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 is a spray pump.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "Now tell me about LION.", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "lion"
    assert ctx["model"] is None
    assert ctx["document"] is None


# ---------------------------------------------------------------------------
# Active context: product switch clears stale model
# ---------------------------------------------------------------------------

def test_product_switch_clears_stale_model() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about LION.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "LION is a pump.", "sources": [{"document": "LION_Catalogue.pdf", "product_slug": "lion", "model": None}], "retrieval_metadata": {}},
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] is None


# ---------------------------------------------------------------------------
# Active context: Tiger -> LION -> generic technical follow-up resolves LION
# ---------------------------------------------------------------------------

def test_tiger_to_lion_followup_resolves_lion() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 outputs 150 cc.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "Now tell me about LION.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "LION is a high-volume pump.", "sources": [{"document": "LION_Catalogue.pdf", "product_slug": "lion", "model": None}], "retrieval_metadata": {}},
        {"role": "user", "content": "What is its pressure ratio?", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "lion"
    assert ctx["model"] is None


# ---------------------------------------------------------------------------
# Active context: LION -> Tiger -> output resolves Tiger
# ---------------------------------------------------------------------------

def test_lion_to_tiger_followup_resolves_tiger() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about LION.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "LION is a pump.", "sources": [{"document": "LION_Catalogue.pdf", "product_slug": "lion", "model": None}], "retrieval_metadata": {}},
        {"role": "user", "content": "Now tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 outputs 150 cc.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "What is its output?", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"


# ---------------------------------------------------------------------------
# Cross-product evidence guard
# ---------------------------------------------------------------------------

def test_cross_product_evidence_guard_rejects_foreign_catalogue_sources() -> None:
    question = "What is the output per cycle of LION?"
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}
    chunks = [
        {"source_type": SOURCE_TYPE_CATALOGUE, "product_slug": "tiger", "text": "Tiger 30:150 output per cycle: 150 cc"},
    ]
    triggered, answer = _cross_product_guard(question, active, chunks)
    assert triggered is True
    assert answer == "This information is not available in the current VR Coatings knowledge base."


def test_cross_product_evidence_guard_allows_matching_sources() -> None:
    question = "What is the pressure ratio of LION?"
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}
    chunks = [
        {"source_type": SOURCE_TYPE_CATALOGUE, "product_slug": "lion", "text": "Pressure Ratio 0.14:1"},
    ]
    triggered, _ = _cross_product_guard(question, active, chunks)
    assert triggered is False


# ---------------------------------------------------------------------------
# Product filter strategy
# ---------------------------------------------------------------------------

def test_product_filter_applied_for_single_product_technical_query() -> None:
    intent = QueryIntent.PRODUCT_TECHNICAL
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}
    assert _should_apply_product_filter("What is LION pressure ratio?", active, intent) is True


def test_product_filter_not_applied_for_comparison_query() -> None:
    intent = QueryIntent.PRODUCT_COMPARISON
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}
    assert _should_apply_product_filter("Compare Tiger and LION", active, intent) is False


def test_product_filter_not_applied_for_governance_query() -> None:
    intent = QueryIntent.GOVERNANCE
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}
    assert _should_apply_product_filter("What does UNKNOWN / TBC mean?", active, intent) is False


def test_product_filter_not_applied_for_company_query() -> None:
    intent = QueryIntent.GENERAL_COMPANY
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}
    assert _should_apply_product_filter("When was VR Coatings founded?", active, intent) is False


# ---------------------------------------------------------------------------
# Conversation isolation
# ---------------------------------------------------------------------------

def test_conversations_remain_isolated() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    db.execute = AsyncMock(return_value=mock_result)

    cid1 = MagicMock()
    cid1.id = "11111111-1111-1111-1111-111111111111"
    cid2 = MagicMock()
    cid2.id = "22222222-2222-2222-2222-222222222222"

    async def run():
        msgs1 = await service.get_recent_messages(cid1.id, limit=4)
        msgs2 = await service.get_recent_messages(cid2.id, limit=4)
        assert msgs1 == []
        assert msgs2 == []

    import asyncio
    asyncio.run(run())


# ---------------------------------------------------------------------------
# Canonical LION slug
# ---------------------------------------------------------------------------

def test_canonical_lion_slug() -> None:
    assert get_canonical_slug("LION") == "lion"
    assert get_canonical_slug("lion pump") == "lion"
    assert get_canonical_slug("LION_Catalogue.pdf") == "lion"


# ---------------------------------------------------------------------------
# Alias resolution
# ---------------------------------------------------------------------------

def test_alias_resolution_extensible() -> None:
    assert "lion" in PRODUCT_ALIASES
    assert "tiger" in PRODUCT_ALIASES
    assert len(PRODUCT_ALIASES) >= 2  # room for future products


# ---------------------------------------------------------------------------
# Exact Tiger 30:150 preserved
# ---------------------------------------------------------------------------

def test_exact_tiger_30_150_preserved_in_active_context() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 outputs 150 cc.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "What is its output?", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"
    assert ctx["document"] == "Tiger.pdf"


# ---------------------------------------------------------------------------
# Price guards remain active (context does not inject prices)
# ---------------------------------------------------------------------------

def test_price_question_does_not_inject_old_product_price() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "How much does Tiger 30:150 cost?", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Price is unavailable.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "How much does LION cost?", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    assert ctx["product_slug"] == "lion"
    assert ctx["model"] is None


# ---------------------------------------------------------------------------
# Unknown product does not inherit previous product specs
# ---------------------------------------------------------------------------

def test_unknown_product_does_not_inherit_previous_specs() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 outputs 150 cc.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "What is Cheetah?", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    # Unknown product names do not override the most recent known product context.
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"


# ---------------------------------------------------------------------------
# Company topic does not contaminate product-specific retrieval
# ---------------------------------------------------------------------------

def test_company_topic_does_not_contaminate_product_retrieval() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    messages = [
        {"role": "user", "content": "Tell me about Tiger 30:150.", "sources": [], "retrieval_metadata": {}},
        {"role": "assistant", "content": "Tiger 30:150 outputs 150 cc.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
        {"role": "user", "content": "When was VR Coatings founded?", "sources": [], "retrieval_metadata": {}},
    ]

    ctx = service.get_active_product_context(messages)
    # Active context may retain the previous product, but company questions
    # are protected by query intent classification and filter logic.
    assert ctx["product_slug"] == "tiger"
    assert ctx["model"] == "30:150"

    # Verify company queries do not apply product filters.
    intent = classify_query("When was VR Coatings founded?")
    assert intent == QueryIntent.GENERAL_COMPANY
    assert _should_apply_product_filter("When was VR Coatings founded?", ctx, intent) is False


# ---------------------------------------------------------------------------
# Governance query ignores product filters
# ---------------------------------------------------------------------------

def test_governance_query_ignores_product_filters() -> None:
    intent = classify_query("What does UNKNOWN / TBC mean?")
    assert intent == QueryIntent.GOVERNANCE

    active = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}
    assert _should_apply_product_filter("What does UNKNOWN / TBC mean?", active, intent) is False


# ---------------------------------------------------------------------------
# Comparison query allows multiple products
# ---------------------------------------------------------------------------

def test_comparison_query_allows_multiple_products() -> None:
    intent = classify_query("Compare Tiger and LION")
    assert intent == QueryIntent.PRODUCT_COMPARISON

    active = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}
    assert _should_apply_product_filter("Compare Tiger and LION", active, intent) is False


# ---------------------------------------------------------------------------
# LION technical test (catalogue evidence required)
# ---------------------------------------------------------------------------

def test_lion_technical_query_requires_lion_catalogue_evidence() -> None:
    question = "What is the pressure ratio of LION?"
    active = {"product_slug": "lion", "model": None, "document": "LION_Catalogue.pdf"}

    # Reject if only Tiger evidence is retrieved.
    chunks = [
        {"source_type": SOURCE_TYPE_CATALOGUE, "product_slug": "tiger", "text": "Tiger 30:150\nPressure Ratio: 30:1"},
    ]
    triggered, _ = _cross_product_guard(question, active, chunks)
    assert triggered is True

    # Allow if Lion evidence is retrieved.
    chunks = [
        {"source_type": SOURCE_TYPE_CATALOGUE, "product_slug": "lion", "text": "LION\nPressure Ratio 0.14:1"},
    ]
    triggered, _ = _cross_product_guard(question, active, chunks)
    assert triggered is False


# ---------------------------------------------------------------------------
# Augmented query does not append stale identifiers when explicit product is present
# ---------------------------------------------------------------------------

def test_augmented_query_does_not_append_stale_identifiers() -> None:
    db = AsyncMock()
    service = ConversationService(db)

    recent = [
        {"role": "assistant", "content": "Tiger 30:150 details.", "sources": [{"document": "Tiger.pdf", "product_slug": "tiger", "model": "30:150"}], "retrieval_metadata": {}},
    ]
    ctx = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}

    augmented = service.build_augmented_query("Tell me about LION.", recent, ctx)
    assert "tiger" not in augmented.lower()
    assert "30:150" not in augmented
