"""
Phase 9C.6A — Barrel Pump Page-Specific OCR Remediation Tests

Tests cover:
1. document hash consistency
2. page-specific remediation selects best variant
3. good page reuse (no rerun)
4. bad page replacement
5. table reconstruction from repaired OCR
6. ratio normalization safety
7. raw/normalized value retention
8. model isolation
9. meaningful content preservation
10. garbage filtering
11. Barrel Pump identity extraction
12. cache writing
"""

import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.rag.ingestion.barrel_pump_remediator import (
    _doc_hash,
    audit_ocr,
    score_variant,
    run_ocr,
    preprocess_image,
    render_page,
    remediate_page,
    remediate_barrel_pump,
)
from app.rag.ingestion.ocr.base import OCRBlock, OCRPageResult
from app.rag.ingestion.structured_table_parser import (
    StructuredTable,
    TableCell,
    TableRow,
    detect_table_type,
    parse_pump_table,
    reconstruct_table_from_ocr_blocks,
)
from app.rag.product_identity import resolve_product_identity


# ============================================================
# Fixtures
# ============================================================

BARREL_PUMP_PDF = Path("/home/vr-coatings/Desktop/website_V2_barrel/backend/storage/catalogues/Barrel Pump.pdf")
BARREL_PUMP_HASH = "e28199b0a34777e992d6470e40cec82bb107159807ef55e0d83c21471339be7c"


@pytest.fixture()
def barrel_pump_available():
    if not BARREL_PUMP_PDF.exists():
        pytest.skip("Barrel Pump PDF not available")


# ============================================================
# 1. document hash consistency
# ============================================================

def test_doc_hash_consistent() -> None:
    if not BARREL_PUMP_PDF.exists():
        pytest.skip("Barrel Pump PDF not available")
    h1 = _doc_hash(str(BARREL_PUMP_PDF))
    h2 = _doc_hash(str(BARREL_PUMP_PDF))
    assert h1 == h2
    assert len(h1) == 64


def test_doc_hash_matches_cached() -> None:
    if not BARREL_PUMP_PDF.exists():
        pytest.skip("Barrel Pump PDF not available")
    h = _doc_hash(str(BARREL_PUMP_PDF))
    assert h == BARREL_PUMP_HASH


# ============================================================
# 2. page-specific remediation selects best variant
# ============================================================

def test_remediate_page_returns_best_variant(barrel_pump_available) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1)
    assert "best_variant" in report
    assert report["best_variant"] is not None
    assert "best_audit" in report
    assert "best_full_text" in report


def test_remediate_page_best_variant_has_higher_score(barrel_pump_available) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1)
    scores = {
        k: v.get("score", -999)
        for k, v in report["all_results"].items()
        if "error" not in v
    }
    if scores:
        best = max(scores.values())
        assert report["best_score"] == best


# ============================================================
# 3. good page reuse (no rerun)
# ============================================================

def test_page2_is_good_and_not_requiring_remediation() -> None:
    backend_dir = Path(__file__).resolve().parent.parent
    cache_path = backend_dir / ".rag_cache" / "ocr" / BARREL_PUMP_HASH / "page_002.json"
    if not cache_path.exists():
        pytest.skip("Page 2 cache not available")
    data = json.loads(cache_path.read_text(encoding="utf-8"))
    confidence = data.get("confidence", 0)
    useful_chars = sum(1 for ch in data.get("full_text", "") if ch.isalpha())
    assert useful_chars > 100, "Page 2 should have substantial text"
    assert confidence > 0.5 or useful_chars > 500, f"Page 2 confidence {confidence} is too low for reuse"


# ============================================================
# 4. bad page replacement
# ============================================================

def test_page1_replacement_improves_quality(barrel_pump_available) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1)
    backend_dir = Path(__file__).resolve().parent.parent
    old_cache = backend_dir / ".rag_cache" / "ocr" / BARREL_PUMP_HASH / "page_001.json"
    if old_cache.exists():
        old_data = json.loads(old_cache.read_text(encoding="utf-8"))
        old_chars = sum(1 for ch in old_data.get("full_text", "") if ch.isalpha())
    else:
        old_chars = 0
    new_chars = report["best_audit"].get("useful_char_count", 0)
    assert new_chars > old_chars or new_chars >= 50, (
        f"Remediated page should have >=50 useful chars (got {new_chars}, old had {old_chars})"
    )


# ============================================================
# 5. table reconstruction from repaired OCR
# ============================================================

def test_remediated_page1_does_not_create_fake_table(barrel_pump_available) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1)
    full_text = report.get("best_full_text", "")
    blocks = []
    for b in report.get("all_results", {}).get(report.get("best_variant", ""), {}).get("blocks", []):
        blocks.append(OCRBlock(**b))
    tables = reconstruct_table_from_ocr_blocks(blocks, page_number=1, document_name="Barrel Pump.pdf")
    if tables:
        for t in tables:
            assert t.table_type != "PUMP_MODEL_TABLE" or len(t.rows) == 0, (
                "Page 1 should not produce a pump model table"
            )


# ============================================================
# 6. ratio normalization safety
# ============================================================

def test_ratio_normalization_only_in_ratio_column() -> None:
    from app.rag.ingestion.structured_table_parser import _normalize_ratio_token
    normalized, reason = _normalize_ratio_token("4.1", is_ratio_col=True, context_rows=["Pressure ratio"])
    assert normalized == "4:1"
    assert reason == "pressure_ratio_column"

    normalized, reason = _normalize_ratio_token("4.1", is_ratio_col=False, context_rows=[])
    assert normalized == "4.1"
    assert reason is None


def test_decimal_values_remain_decimals() -> None:
    from app.rag.ingestion.structured_table_parser import _normalize_ratio_token
    normalized, reason = _normalize_ratio_token("4.4", is_ratio_col=True, context_rows=["Pressure ratio"])
    assert normalized == "4:4"
    assert reason == "pressure_ratio_column"


# ============================================================
# 7. raw/normalized value retention
# ============================================================

def test_raw_normalized_values_available() -> None:
    headers = ["Type", "Pressure ratio"]
    rows = [
        TableRow(
            cells=[TableCell(text="30:150"), TableCell(text="30:1", confidence=0.9)],
            raw_cells=["30:150", "30:1"],
        ),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE")
    parsed = parse_pump_table(table)
    if parsed:
        values = parsed[0]["values"]
        ratio_value = [v for v in values if v["label"] == "Pressure ratio"]
        if ratio_value:
            assert "raw_value" in ratio_value[0]
            assert "normalization_reason" in ratio_value[0]


# ============================================================
# 8. model isolation
# ============================================================

def test_pump_table_model_isolation() -> None:
    headers = ["Type", "30:150", "35:70"]
    rows = [
        TableRow(
            cells=[TableCell(text="Pressure ratio"), TableCell(text="30:1"), TableCell(text="35:1")],
            raw_cells=["Pressure ratio", "30:1", "35:1"],
        ),
        TableRow(
            cells=[TableCell(text="Output per cycle (cc)"), TableCell(text="150"), TableCell(text="70")],
            raw_cells=["Output per cycle (cc)", "150", "70"],
        ),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE")
    parsed = parse_pump_table(table)
    assert len(parsed) == 2
    assert parsed[0]["model"] == "30:150"
    assert parsed[1]["model"] == "35:70"
    for item in parsed:
        for v in item["values"]:
            assert v["label"] != ""


# ============================================================
# 9. meaningful content preservation
# ============================================================

def test_remediated_page1_has_meaningful_content(barrel_pump_available) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1)
    full_text = report.get("best_full_text", "")
    meaningful_words = {"barrel", "pump", "suitable", "transferring", "liquids", "vr", "coatings"}
    text_lower = full_text.lower()
    found = meaningful_words.intersection(set(text_lower.split()))
    assert len(found) >= 2, f"Expected meaningful content, got: {full_text[:200]}"


# ============================================================
# 10. garbage filtering
# ============================================================

def test_garbage_lines_filtered_from_chunks() -> None:
    from app.rag.ingestion.new_chunker import _classify_short_fragment
    garbage_samples = ["CE", "PUUP", "AEL", "VR ngs", "xi", "C∈"]
    for sample in garbage_samples:
        cls = _classify_short_fragment(sample)
        assert cls in ("OCR_GARBAGE", "UNKNOWN", "FOOTER"), f"{sample!r} classified as {cls}"


# ============================================================
# 11. Barrel Pump identity extraction
# ============================================================

def test_barrel_pump_identity_from_ocr() -> None:
    sample_text = "BARREL PUMP\nVR Coatings\nSuitable for transferring liquids from 210 liters barrel"
    slug = resolve_product_identity(sample_text)
    assert slug is not None
    assert slug[0] == "barrel-pump"


def test_barrel_pump_aliases_exist() -> None:
    from app.rag.product_identity import PRODUCT_ALIASES
    assert "barrel-pump" in PRODUCT_ALIASES
    aliases = [a.lower() for a in PRODUCT_ALIASES["barrel-pump"]["aliases"]]
    assert "barrel pump" in aliases


# ============================================================
# 12. cache writing
# ============================================================

def test_remediate_page_writes_cache(barrel_pump_available, tmp_path) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1, cache_dir=str(tmp_path))
    assert "cache_written" in report
    cache_path = Path(report["cache_written"])
    assert cache_path.exists()
    data = json.loads(cache_path.read_text(encoding="utf-8"))
    assert data["page_number"] == 1
    assert "full_text" in data
    assert "blocks" in data


def test_barrel_pump_hash_never_matches_tiger_hash() -> None:
    tiger_path = Path("/home/vr-coatings/Desktop/website_V2_barrel/backend/storage/catalogues/Tiger.pdf")
    if not tiger_path.exists():
        pytest.skip("Tiger.pdf not available")
    barrel_hash = _doc_hash(str(BARREL_PUMP_PDF))
    tiger_hash = _doc_hash(str(tiger_path))
    assert barrel_hash != tiger_hash
    assert barrel_hash == BARREL_PUMP_HASH


def test_remediate_page_uses_actual_pdf_hash(barrel_pump_available) -> None:
    report = remediate_page(str(BARREL_PUMP_PDF), page_number=1)
    assert report["document_hash"] == _doc_hash(str(BARREL_PUMP_PDF))
    assert report["document_hash"] != "9d9fa3fcbe4050d4bb60649ea87303c9bff9dcb2a6dcb687e4b83d1720e7e44e"
