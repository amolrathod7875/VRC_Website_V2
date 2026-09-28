from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker


def test_context_builder_prefers_higher_authority() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"authority_priority": 90, "text": "company answer", "source_type": "company_master"},
        {"authority_priority": 100, "text": "catalogue answer", "source_type": "catalogue"},
    ]
    result = builder.build(chunks, "test")
    assert result["chunks"][0]["text"] == "catalogue answer"
