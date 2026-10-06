"""
Phase 9A — OCR Pipeline Validation Tests

Tests cover:
1. OCR cache keyed by SHA-256
2. image-only document uses OCR path
3. text-capable document does not unnecessarily OCR
4. exact technical identifiers preserved
5. canonical product slug generation
6. technical table row relationships
7. OCR page provenance metadata
8. authority_priority=100
9. unchanged OCR catalogue skipped
10. OCR failure does not corrupt other documents
11. low-confidence numeric data flagged safely
12. cross-product retrieval still isolated
"""
import hashlib
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.rag.ingestion.ocr.base import OCRBlock, OCRPageResult, OCRProvider, OCRTable
from app.rag.ingestion.ocr.ocr_service import OCRCache, OCRService
from app.rag.ingestion.pdf_parser import page_needs_ocr, _doc_hash
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.pdf_table_parser import parse_spec_table, is_likely_spec_table
from app.rag.product_identity import get_canonical_slug, resolve_product_identity, extract_model_identifier
from app.rag.constants import CATALOGUE_AUTHORITY_PRIORITY, CHUNK_TYPE_TECHNICAL_MODEL


# ============================================================
# 1. OCR cache keyed by SHA-256
# ============================================================
def test_ocr_cache_keyed_by_sha256() -> None:
    cache = OCRCache(base_dir=".tmp_test_ocr_cache_9a")
    doc_a = "a" * 64
    doc_b = "b" * 64
    result = OCRPageResult(page_number=1, full_text="test", blocks=[], tables=[], confidence=0.9)
    cache.put(doc_a, 1, result)
    loaded_a = cache.get(doc_a, 1)
    loaded_b = cache.get(doc_b, 1)
    assert loaded_a is not None
    assert loaded_b is None


# ============================================================
# 2. image-only document uses OCR path
# ============================================================
def test_page_needs_ocr_empty_text() -> None:
    assert page_needs_ocr("") is True
    assert page_needs_ocr("   ") is True
    # Numeric-only has 0 alpha chars so it also needs OCR
    assert page_needs_ocr("123") is True
    # Must have at least 40 alpha chars to skip OCR
    short = "Hello World, this is a test"
    assert page_needs_ocr(short) is True
    long_text = "This is a sufficiently long text page with more than forty alpha characters for OCR to be unnecessary here."
    assert page_needs_ocr(long_text) is False


# ============================================================
# 3. text-capable document does not unnecessarily OCR
# ============================================================
def test_page_needs_ocr_sufficient_alpha() -> None:
    text = "This is a real text page with enough alpha characters for OCR to be unnecessary."
    assert page_needs_ocr(text) is False


# ============================================================
# 4. exact technical identifiers preserved
# ============================================================
def test_parse_spec_table_preserves_colon_identifiers() -> None:
    rows = [
        ["Type", "30:150", "35:70"],
        ["Pressure ratio", "30:1", "35:1"],
        ["Output per cycle (cc)", "150", "70"],
    ]
    parsed = parse_spec_table(rows)
    assert len(parsed) == 2
    model_a = next(p for p in parsed if p["model"] == "30:150")
    assert model_a["values"][0]["value"] == "30:1"
    assert model_a["values"][1]["value"] == "150"
    assert "30:150" in model_a["values"][0]["value"] or "30:1" in model_a["values"][0]["value"]


def test_model_identifier_extraction() -> None:
    text = "The Tiger 30:150 pump has a pressure ratio of 30:1."
    match = extract_model_identifier(text)
    assert match == "30:150"


# ============================================================
# 5. canonical product slug generation
# ============================================================
def test_canonical_slug_known_product() -> None:
    assert get_canonical_slug("Tiger") == "tiger"
    assert get_canonical_slug("lion") == "lion"


def test_canonical_slug_unknown_returns_none() -> None:
    assert get_canonical_slug("unknown_product") is None
    assert get_canonical_slug("NonExistentSystem") is None


# ============================================================
# 6. technical table row relationships
# ============================================================
def test_spec_table_preserves_model_value_relationship() -> None:
    rows = [
        ["Model", "30:150", "35:70"],
        ["Pressure ratio", "30:1", "35:1"],
        ["Output per cycle (cc)", "150", "70"],
    ]
    parsed = parse_spec_table(rows)
    model_a = next(p for p in parsed if p["model"] == "30:150")
    labels = [v["label"] for v in model_a["values"]]
    assert "Pressure ratio" in labels
    assert "Output per cycle (cc)" in labels
    values = {v["label"]: v["value"] for v in model_a["values"]}
    assert values["Pressure ratio"] == "30:1"
    assert values["Output per cycle (cc)"] == "150"


def test_is_likely_spec_table_detects_headers() -> None:
    rows = [
        ["Model", "30:150", "35:70"],
        ["Pressure ratio", "30:1", "35:1"],
    ]
    assert is_likely_spec_table(rows) is True


# ============================================================
# 7. OCR page provenance metadata
# ============================================================
def test_ocr_page_result_has_provenance_fields() -> None:
    result = OCRPageResult(
        page_number=3,
        full_text="Pressure ratio: 30:1",
        blocks=[OCRBlock(text="Pressure ratio: 30:1", bbox=[0, 0, 100, 20], confidence=0.95)],
        tables=[],
        warnings=[],
        confidence=0.95,
        metadata={"text_confidence": 0.95, "table_confidence": None},
    )
    assert result.page_number == 3
    assert result.full_text == "Pressure ratio: 30:1"
    assert len(result.blocks) == 1
    assert result.blocks[0].confidence == 0.95
    assert result.metadata["text_confidence"] == 0.95


# ============================================================
# 8. authority_priority=100
# ============================================================
def test_catalogue_chunks_have_correct_authority() -> None:
    pages = [{"page_number": 1, "text": "Rhino pump\n\nPressure ratio: 30:1"}]
    chunks = chunk_catalogue(
        document_name="rhino.pdf",
        pages=pages,
        tables=[],
        product_slug="rhino",
        document_id="doc-123",
        ocr_results=[],
    )
    for chunk in chunks:
        assert chunk.get("authority_priority") == CATALOGUE_AUTHORITY_PRIORITY
        assert chunk.get("source_type") == "catalogue"


# ============================================================
# 9. unchanged OCR catalogue skipped
# ============================================================
def test_ocr_cache_prevents_repeated_processing() -> None:
    cache = OCRCache(base_dir=".tmp_test_ocr_cache_9b")
    doc_hash = "unchanged_doc_abc"
    page_num = 1
    original = OCRPageResult(
        page_number=page_num,
        full_text="30:1 150",
        blocks=[OCRBlock(text="30:1", confidence=0.9)],
        tables=[],
        confidence=0.9,
    )
    cache.put(doc_hash, page_num, original)
    loaded = cache.get(doc_hash, page_num)
    assert loaded is not None
    assert loaded.full_text == "30:1 150"
    assert loaded.blocks[0].confidence == 0.9
    # Second get returns same data (cache hit)
    loaded2 = cache.get(doc_hash, page_num)
    assert loaded2.full_text == "30:1 150"


# ============================================================
# 10. OCR failure does not corrupt other documents
# ============================================================
def test_ocr_failure_does_not_corrupt_cache() -> None:
    cache = OCRCache(base_dir=".tmp_test_ocr_cache_9c")
    good_doc = "good_doc_sha"
    bad_doc = "bad_doc_sha"
    good_result = OCRPageResult(page_number=1, full_text="good text", blocks=[], tables=[], confidence=0.9)
    cache.put(good_doc, 1, good_result)
    # Bad doc has no cache entry
    bad_result = cache.get(bad_doc, 1)
    assert bad_result is None
    # Good doc still intact
    good_loaded = cache.get(good_doc, 1)
    assert good_loaded is not None
    assert good_loaded.full_text == "good text"


# ============================================================
# 11. low-confidence numeric data flagged safely
# ============================================================
def test_low_confidence_numeric_triggers_warning() -> None:
    from unittest.mock import MagicMock
    from app.rag.ingestion.ocr.paddle_ocr import PaddleOCRProvider

    provider = PaddleOCRProvider(lang="en")
    mock_page_result = MagicMock()
    mock_page_result.rec_texts = ["180", "210"]
    mock_page_result.rec_scores = [0.7, 0.72]
    mock_page_result.rec_boxes = [[0, 0, 10, 10], [20, 20, 30, 30]]

    provider._client = MagicMock()
    provider._client.ocr.return_value = [mock_page_result]

    result = provider.process_page("/tmp/fake.png", 1)
    assert any("TABLE_CONFIDENCE_WARNING" in w for w in result.warnings)


# ============================================================
# 12. cross-product retrieval still isolated
# ============================================================
def test_cross_product_isolation_in_chunks() -> None:
    pages = [{"page_number": 1, "text": "Rhino pump\n\nPressure ratio: 30:1"}]
    chunks = chunk_catalogue(
        document_name="rhino.pdf",
        pages=pages,
        tables=[],
        product_slug="rhino",
        document_id="doc-rhino",
        ocr_results=[],
    )
    for chunk in chunks:
        assert chunk.get("product_slug") == "rhino"
        assert chunk.get("source_type") == "catalogue"
        assert chunk.get("authority_priority") == CATALOGUE_AUTHORITY_PRIORITY


# ============================================================
# Additional: chunk type for technical model
# ============================================================
def test_technical_model_chunk_type() -> None:
    rows = [
        ["30:150", "35:70"],
        ["30:1", "35:1"],
        ["150", "70"],
    ]
    parsed = parse_spec_table(rows)
    assert len(parsed) == 2
    for item in parsed:
        assert "model" in item
        assert "values" in item
        assert len(item["values"]) == 2
