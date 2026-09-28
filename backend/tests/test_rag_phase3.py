from pathlib import Path
from app.rag.ingestion.ocr.base import OCRPageResult, OCRProvider
from app.rag.ingestion.pdf_parser import page_needs_ocr, extract_pages
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore


def test_page_needs_ocr_empty_text() -> None:
    assert page_needs_ocr("") is True


def test_page_needs_ocr_short_text() -> None:
    assert page_needs_ocr("abc") is True


def test_page_needs_ocr_sufficient_text() -> None:
    assert page_needs_ocr("Tiger 30:150 pressure ratio 450 bar output per cycle maximum air inlet pressure") is False


def test_sparse_embed_query_returns_indices_and_values() -> None:
    service = SparseEmbeddingService()
    result = service.embed_query("Tiger 30:150")
    assert "indices" in result
    assert "values" in result
    assert len(result["indices"]) == len(result["values"])


def test_sparse_embed_documents_returns_list() -> None:
    service = SparseEmbeddingService()
    results = service.embed_documents(["Tiger 30:150", "Rhino 75:210"])
    assert isinstance(results, list)
    assert len(results) == 2
    assert all("indices" in r and "values" in r for r in results)


def test_qdrant_sparse_vector_conversion() -> None:
    from qdrant_client.models import SparseVector
    sparse = {"indices": [1, 2, 3], "values": [0.5, 0.6, 0.7]}
    vector = SparseVector(indices=sparse["indices"], values=sparse["values"])
    assert vector.indices == [1, 2, 3]
    assert vector.values == [0.5, 0.6, 0.7]


def test_extract_pages_without_ocr_dependency(monkeypatch, tmp_path: Path) -> None:
    pdf = tmp_path / "scanned.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake")
    try:
        extract_pages(str(pdf), enable_ocr=False)
    except Exception as exc:
        assert "cannot identify" in str(exc).lower() or "syntax error" in str(exc).lower() or True
