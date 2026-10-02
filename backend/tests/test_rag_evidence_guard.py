import pytest
from unittest.mock import AsyncMock, patch
from app.rag.retrieval.query_classifier import (
    classify_query,
    is_negative_existential,
    is_affirmative_yes_no,
    evaluate_evidence_guard,
    QueryIntent,
)
from app.rag.services.rag_service import RAGService
from app.rag.generation.prompts import ANSWER_UNAVAILABLE


def test_negative_existential_electric_cars_returns_unavailable() -> None:
    question = "Does VR Coatings make electric cars?"
    context = "VR Coatings manufactures pumps, spray equipment and dispensing systems."
    assert is_negative_existential(question) is True
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is True
    assert answer == ANSWER_UNAVAILABLE


def test_negative_existential_aircraft_returns_unavailable() -> None:
    question = "Does VR Coatings manufacture aircraft?"
    context = "VR Coatings manufactures pumps and dispensing systems."
    assert is_negative_existential(question) is True
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is True
    assert answer == ANSWER_UNAVAILABLE


def test_negative_existential_laptops_returns_unavailable() -> None:
    question = "Does VR Coatings sell laptops?"
    context = "VR Coatings sells pumps and spray equipment."
    assert is_negative_existential(question) is True
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is True
    assert answer == ANSWER_UNAVAILABLE


def test_negative_existential_tiger_water_based_returns_unavailable() -> None:
    question = "Does Tiger support water-based coatings?"
    context = "Tiger pumps are used for solvent-based coatings."
    assert is_negative_existential(question) is True
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is True
    assert answer == ANSWER_UNAVAILABLE


def test_affirmative_yes_no_tiger_pressure_ratio_passes_guard() -> None:
    question = "Does Tiger 30:150 have a pressure ratio of 30:1?"
    context = "Tiger 30:150\nPressure Ratio: 30:1"
    assert is_affirmative_yes_no(question) is True
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is False


def test_affirmative_yes_no_tiger_90_to_1_passes_guard() -> None:
    question = "Does Tiger 30:150 have a pressure ratio of 90:1?"
    context = "Tiger 30:150\nPressure Ratio: 30:1"
    assert is_affirmative_yes_no(question) is True
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is False


def test_positive_supported_claim_tiger_pumps_passes_guard() -> None:
    question = "Does VR Coatings manufacture Tiger pumps?"
    context = "VR Coatings manufactures Tiger pumps, spray equipment and dispensing systems."
    triggered, answer = evaluate_evidence_guard(question, context)
    assert triggered is False


def test_general_company_query_classification() -> None:
    assert classify_query("What is VR Coatings?") == QueryIntent.GENERAL_COMPANY
    assert classify_query("Tell me about VR Coatings.") == QueryIntent.GENERAL_COMPANY
    assert classify_query("What does VR Coatings do?") == QueryIntent.GENERAL_COMPANY


def test_governance_query_classification() -> None:
    assert classify_query("What does UNKNOWN / TBC mean?") == QueryIntent.GOVERNANCE


def test_model_identifier_query_classification() -> None:
    assert classify_query("30:150") == QueryIntent.MODEL_IDENTIFIER
    assert classify_query("Tiger 30:150 pressure ratio") == QueryIntent.PRODUCT_TECHNICAL


def test_contact_location_query_classification() -> None:
    assert classify_query("South India contact number") == QueryIntent.CONTACT_LOCATION


def test_rag_service_evidence_guard_returns_unavailable_for_negative_existential() -> None:
    import asyncio

    mock_dense = AsyncMock()
    mock_dense.embed_query.return_value = [0.1] * 384
    mock_sparse = AsyncMock()
    mock_sparse.embed_query.return_value = {"indices": [0], "values": [0.1]}
    mock_retriever = AsyncMock()
    mock_retriever.retrieve.return_value = [
        {
            "text": "VR Coatings manufactures pumps, spray equipment and dispensing systems.",
            "source_type": "company_master",
            "document_name": "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt",
            "section": "company_overview",
        }
    ]

    class SyncContextBuilder:
        def build(self, chunks, query):
            return {
                "context": "VR Coatings manufactures pumps, spray equipment and dispensing systems.",
                "sources": [],
                "chunks": [],
            }

    mock_context_builder = SyncContextBuilder()
    mock_generator = AsyncMock()
    mock_generator.generate_answer.return_value = {"answer": "No", "provider_error": False}

    service = RAGService(
        dense=mock_dense,
        sparse=mock_sparse,
        retriever=mock_retriever,
        generator=mock_generator,
        context_builder=mock_context_builder,
    )
    result = asyncio.run(service.answer("Does VR Coatings make electric cars?"))
    assert result["answer"] == ANSWER_UNAVAILABLE
