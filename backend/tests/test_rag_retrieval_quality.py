from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.query_classifier import classify_query, QueryIntent


def test_context_builder_general_company_query_prefers_overview_chunks() -> None:
    builder = ContextBuilder()
    chunks = [
        {"text": "VR Coatings manufactures pumps and spray equipment.", "source_type": "company_master", "section": "company_overview", "score": 0.5},
        {"text": "Change log: updated dataset goals.", "source_type": "company_master", "section": "change_log", "score": 0.9},
        {"text": "VR Coatings was founded in 1985.", "source_type": "company_master", "section": "company_history", "score": 0.8},
    ]
    result = builder.build(chunks, "What is VR Coatings?", max_chunks=3, max_chars=12000)
    selected = result["chunks"]
    assert any("company_overview" in c.get("section", "").lower() for c in selected)
    assert selected[0].get("section", "").lower() == "company_overview"


def test_context_builder_governance_query_retrieves_governance_chunks() -> None:
    builder = ContextBuilder()
    chunks = [
        {"text": "UNKNOWN means the value has not been verified.", "source_type": "company_master", "section": "governance", "score": 0.9},
        {"text": "VR Coatings manufactures pumps.", "source_type": "company_master", "section": "company_overview", "score": 0.5},
    ]
    result = builder.build(chunks, "What does UNKNOWN mean?", max_chunks=2, max_chars=12000)
    selected = result["chunks"]
    assert any("governance" in c.get("section", "").lower() for c in selected)


def test_context_builder_model_identifier_query_prefers_catalogue_technical() -> None:
    builder = ContextBuilder()
    chunks = [
        {"text": "Tiger 30:150 has a pressure ratio of 30:1.", "source_type": "catalogue", "section": "technical_specifications", "score": 0.5},
        {"text": "VR Coatings manufactures pumps.", "source_type": "company_master", "section": "company_overview", "score": 0.9},
    ]
    result = builder.build(chunks, "Tiger 30:150 pressure ratio", max_chunks=2, max_chars=12000)
    selected = result["chunks"]
    assert selected[0].get("source_type") == "catalogue"
    assert "pressure ratio" in selected[0].get("text", "").lower()


def test_classify_query_what_is_vr_coatings() -> None:
    assert classify_query("What is VR Coatings?") == QueryIntent.GENERAL_COMPANY


def test_classify_query_tiger_pressure_ratio() -> None:
    assert classify_query("Tiger 30:150 pressure ratio") == QueryIntent.PRODUCT_TECHNICAL


def test_classify_query_unknown_tbc() -> None:
    assert classify_query("What does UNKNOWN / TBC mean?") == QueryIntent.GOVERNANCE
