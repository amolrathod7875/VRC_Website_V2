import pytest
from app.rag.retrieval.query_classifier import is_vr_coatings_domain_query, QueryIntent


@pytest.mark.parametrize(
    "message",
    [
        "What is VR Coatings?",
        "When was VR Coatings founded?",
        "Where is VR Coatings located?",
        "Tell me about Tiger 30:150.",
        "What is Rhino used for?",
        "Hippo pump",
        "Leopard flow rate",
        "What is the pressure ratio of Tiger?",
        "Compare Rhino and Elephant",
        "What is the output per cycle of LION?",
        "What warranty does Tiger have?",
    ],
)
def test_vr_coatings_domain_queries_are_detected(message: str) -> None:
    assert is_vr_coatings_domain_query(message) is True


@pytest.mark.parametrize(
    "message",
    [
        "what's your name",
        "what is AI",
        "explain machine learning",
        "tell me a joke",
        "write python factorial",
        "capital of Japan",
        "difference between TCP and UDP",
        "What is an airless spray pump?",
        "how does a transformer model work",
    ],
)
def test_general_knowledge_queries_are_not_domain(message: str) -> None:
    assert is_vr_coatings_domain_query(message) is False


def test_domain_followup_with_active_product_context() -> None:
    active_context = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}
    assert is_vr_coatings_domain_query("What is its output?", active_context) is True
    assert is_vr_coatings_domain_query("And pressure ratio?", active_context) is True
    assert is_vr_coatings_domain_query("Tell me more", active_context) is True


def test_general_question_during_product_context_stays_general() -> None:
    active_context = {"product_slug": "tiger", "model": "30:150", "document": "Tiger.pdf"}
    assert is_vr_coatings_domain_query("What is machine learning?", active_context) is False
    assert is_vr_coatings_domain_query("Explain AI", active_context) is False
    assert is_vr_coatings_domain_query("Write a Python function", active_context) is False


def test_product_switch_detected() -> None:
    assert is_vr_coatings_domain_query("Now tell me about LION") is True
    assert is_vr_coatings_domain_query("What about Rhino?") is True
