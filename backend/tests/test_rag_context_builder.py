from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker


def test_context_builder_deduplicates_chunks() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"authority_priority": 100, "text": "same text", "source_type": "catalogue"},
        {"authority_priority": 90, "text": "same text", "source_type": "company_master"},
    ]
    result = builder.build(chunks, "test")
    assert len(result["chunks"]) == 1
    assert result["chunks"][0]["text"] == "same text"


def test_context_builder_preserves_relevance_order() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"authority_priority": 90, "text": "company answer", "source_type": "company_master", "score": 0.9},
        {"authority_priority": 100, "text": "catalogue answer", "source_type": "catalogue", "score": 0.5},
    ]
    result = builder.build(chunks, "test")
    assert result["chunks"][0]["text"] == "company answer"
