from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.constants import SOURCE_TYPE_CATALOGUE, SOURCE_TYPE_COMPANY_MASTER


def test_context_builder_deduplicates_chunks() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"authority_priority": 100, "text": "same text", "source_type": SOURCE_TYPE_CATALOGUE},
        {"authority_priority": 90, "text": "same text", "source_type": SOURCE_TYPE_COMPANY_MASTER},
    ]
    result = builder.build(chunks, "test")
    assert len(result["chunks"]) == 1
    assert result["chunks"][0]["text"] == "same text"


def test_context_builder_preserves_relevance_order() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"authority_priority": 90, "text": "company answer", "source_type": SOURCE_TYPE_COMPANY_MASTER, "score": 0.9},
        {"authority_priority": 100, "text": "catalogue answer", "source_type": SOURCE_TYPE_CATALOGUE, "score": 0.5},
    ]
    result = builder.build(chunks, "test")
    assert result["chunks"][0]["text"] == "company answer"


def test_context_builder_detects_conflicts() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {
            "authority_priority": 90,
            "text": "Pressure ratio: 20:1",
            "source_type": SOURCE_TYPE_COMPANY_MASTER,
            "model": "30:150",
            "product_slug": "tiger",
        },
        {
            "authority_priority": 100,
            "text": "Pressure ratio: 30:1",
            "source_type": SOURCE_TYPE_CATALOGUE,
            "model": "30:150",
            "product_slug": "tiger",
        },
    ]
    result = builder.build(chunks, "pressure ratio")
    assert len(result["chunks"]) == 2
    context = result["context"].lower()
    assert "note: conflicting information" in context
    assert "official catalogue takes precedence" in context


def test_context_builder_limits_chunks() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"text": f"Chunk {i}", "source_type": SOURCE_TYPE_CATALOGUE, "authority_priority": 100}
        for i in range(20)
    ]
    result = builder.build(chunks, "test", max_chunks=4)
    assert len(result["chunks"]) == 4


def test_context_builder_deduplicates_by_normalized_text() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"text": "  Same Text Here  ", "source_type": SOURCE_TYPE_CATALOGUE},
        {"text": "same text here", "source_type": SOURCE_TYPE_COMPANY_MASTER},
        {"text": "Different text", "source_type": SOURCE_TYPE_CATALOGUE},
    ]
    result = builder.build(chunks, "test")
    assert len(result["chunks"]) == 2
    assert result["chunks"][0]["text"] == "  Same Text Here  "


def test_context_builder_preserves_source_metadata() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {
            "text": "Tiger 30:150 pressure ratio 30:1",
            "source_type": SOURCE_TYPE_CATALOGUE,
            "document_name": "Tiger.pdf",
            "product_slug": "tiger",
            "section": "Technical Specifications",
            "page_number": 2,
            "model": "30:150",
            "authority_priority": 100,
        }
    ]
    result = builder.build(chunks, "test")
    source = result["sources"][0]
    assert source["document"] == "Tiger.pdf"
    assert source["model"] == "30:150"
    assert source["authority_priority"] == 100
    assert source["page"] == 2
    assert source["product_slug"] == "tiger"


def test_context_builder_no_conflict_when_same_source_type() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"text": "Pressure ratio: 30:1", "source_type": SOURCE_TYPE_CATALOGUE, "model": "30:150", "product_slug": "tiger"},
        {"text": "Output per cycle: 150 cc", "source_type": SOURCE_TYPE_CATALOGUE, "model": "30:150", "product_slug": "tiger"},
    ]
    result = builder.build(chunks, "test")
    assert "NOTE:" not in result["context"]


def test_context_builder_conflict_note_not_added_for_different_models() -> None:
    builder = ContextBuilder(reranker=Reranker())
    chunks = [
        {"text": "Pressure ratio: 30:1", "source_type": SOURCE_TYPE_CATALOGUE, "model": "30:150", "product_slug": "tiger"},
        {"text": "Pressure ratio: 25:1", "source_type": SOURCE_TYPE_COMPANY_MASTER, "model": "75:210", "product_slug": "rhino"},
    ]
    result = builder.build(chunks, "test")
    assert "NOTE:" not in result["context"]
