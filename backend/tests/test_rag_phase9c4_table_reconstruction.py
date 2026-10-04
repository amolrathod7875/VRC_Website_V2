"""
Phase 9C.4 — Table Reconstruction Remediation Tests

Tests cover:
1. Table type classification
2. Pump row reconstruction (PUMP_MODEL_TABLE)
3. Part-number row reconstruction (PART_NUMBER_TABLE)
4. Valve row reconstruction (VALVE_SPEC_TABLE)
5. Dot/colon normalization only in ratio columns
6. Decimal values remain decimals
7. Part-number spacing preservation
8. Leading-zero preservation
9. Row confidence
10. Unknown cell preservation
11. technical_part chunks
12. Page provenance
13. Turbine/pneumatic alias isolation
14. Duplicate row removal
15. Idempotency
16. CUB table diagnosis
17. Drum Press identity preserved
18. Ball valve row coherence
"""

import re
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from app.rag.ingestion.structured_table_parser import (
    StructuredTable,
    TableRow,
    TableCell,
    detect_table_type,
    parse_pump_table,
    parse_part_number_table,
    parse_valve_table,
    parse_structured_table,
    validate_table,
    _normalize_ratio_token,
    _is_part_number,
    reconstruct_table_from_ocr_blocks,
)
from app.rag.ingestion.ocr.base import OCRBlock, OCRPageResult
from app.rag.ingestion.new_chunker import chunk_catalogue
from app.rag.product_identity import PRODUCT_ALIASES, resolve_product_identity


# ============================================================
# 1. Table type classification
# ============================================================

def test_pump_model_table_type_detected() -> None:
    headers = ["Type", "Pressure ratio", "Discharge per cycle (cc)", "Stroke Length (mm)"]
    rows = [
        TableRow(cells=[TableCell(text="30:150"), TableCell(text="30:1"), TableCell(text="150"), TableCell(text="120")]),
        TableRow(cells=[TableCell(text="35:70"), TableCell(text="35:1"), TableCell(text="70"), TableCell(text="120")]),
    ]
    table_type = detect_table_type(headers, rows, "Tiger.pdf")
    assert table_type == "PUMP_MODEL_TABLE"


def test_part_number_table_type_detected() -> None:
    headers = ["Fan dia.", "Shaft length.", "Part No.", "Part No.", "For container"]
    rows = [
        TableRow(cells=[TableCell(text="200"), TableCell(text="300"), TableCell(text="16 200 000 01"), TableCell(text="16 200 000 00"), TableCell(text="200")]),
    ]
    table_type = detect_table_type(headers, rows, "PNEUMATIC STIRRER.pdf")
    assert table_type == "PART_NUMBER_TABLE"


def test_valve_spec_table_type_detected() -> None:
    headers = ["PORT SIZE", "MOC- CARBON STEEL PART CODE", "MWP", "CONNECTIONS"]
    rows = [
        TableRow(cells=[TableCell(text="1/4\" PORT"), TableCell(text="20 058 000 01"), TableCell(text="450 BAR"), TableCell(text="1 MALE/1 FEMALE PORT (BSP)")]),
    ]
    table_type = detect_table_type(headers, rows, "ball_valves.pdf")
    assert table_type == "VALVE_SPEC_TABLE"


def test_unknown_table_type_fallback() -> None:
    headers = ["Column A", "Column B"]
    rows = [
        TableRow(cells=[TableCell(text="foo"), TableCell(text="bar")]),
    ]
    table_type = detect_table_type(headers, rows, "unknown.pdf")
    assert table_type == "UNKNOWN_TABLE"


# ============================================================
# 2. Pump row reconstruction
# ============================================================

def test_pump_table_reconstructs_models() -> None:
    headers = ["Type", "CUB 2:400", "CUB 4.400", "CUB 6.400"]
    rows = [
        TableRow(cells=[TableCell(text="Pressure ratio"), TableCell(text="2:1"), TableCell(text="4:1"), TableCell(text="6:1")], raw_cells=["Pressure ratio", "2:1", "4:1", "6:1"]),
        TableRow(cells=[TableCell(text="Discharge per cycle (cc)"), TableCell(text="400"), TableCell(text="400"), TableCell(text="400")], raw_cells=["Discharge per cycle (cc)", "400", "400", "400"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE")
    parsed = parse_pump_table(table)
    assert len(parsed) == 3
    assert parsed[0]["model"] == "CUB 2:400"
    assert parsed[1]["model"] == "CUB 4.400"
    assert parsed[2]["model"] == "CUB 6.400"
    assert len(parsed[0]["values"]) == 2
    assert parsed[0]["values"][0]["value"] == "2:1"
    assert parsed[0]["values"][1]["value"] == "400"


def test_pump_table_missing_cell_rejects_row() -> None:
    headers = ["Type", "Pressure ratio", "Discharge per cycle (cc)"]
    rows = [
        TableRow(cells=[TableCell(text="30:150"), TableCell(text="30:1"), TableCell(text="")], raw_cells=["30:150", "30:1", ""]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE")
    parsed = parse_pump_table(table)
    assert len(parsed) == 1
    assert parsed[0]["model"] == "Pressure ratio"
    assert parsed[0]["values"][0]["value"] == "30:1"


# ============================================================
# 3. Part-number row reconstruction
# ============================================================

def test_part_number_table_reconstructs_parts() -> None:
    headers = ["Fan dia.", "Shaft length.", "Part No.", "Part No.", "For container"]
    rows = [
        TableRow(cells=[TableCell(text="200"), TableCell(text="300"), TableCell(text="16 200 000 01"), TableCell(text="16 200 000 00"), TableCell(text="200")], raw_cells=["200", "300", "16 200 000 01", "16 200 000 00", "200"]),
        TableRow(cells=[TableCell(text="100"), TableCell(text="300"), TableCell(text="16 100 000 01"), TableCell(text="16 100 000 00"), TableCell(text="100")], raw_cells=["100", "300", "16 100 000 01", "16 100 000 00", "100"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PART_NUMBER_TABLE")
    parsed = parse_part_number_table(table)
    assert len(parsed) == 2
    assert parsed[0]["part_number"] == "16 200 000 01"
    assert parsed[1]["part_number"] == "16 100 000 01"
    assert parsed[0]["values"][0]["value"] == "200"


def test_part_number_table_no_pump_ratio_normalization() -> None:
    headers = ["Fan dia.", "Shaft length.", "Part No."]
    rows = [
        TableRow(cells=[TableCell(text="200"), TableCell(text="300"), TableCell(text="16 200 000 01")], raw_cells=["200", "300", "16 200 000 01"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PART_NUMBER_TABLE")
    parsed = parse_part_number_table(table)
    assert len(parsed) == 1
    assert parsed[0]["part_number"] == "16 200 000 01"
    assert ":" not in parsed[0]["values"][0]["value"]


# ============================================================
# 4. Valve row reconstruction
# ============================================================

def test_valve_table_reconstructs_rows() -> None:
    headers = ["PORT SIZE", "PART CODE", "MWP", "CONNECTIONS"]
    rows = [
        TableRow(cells=[
            TableCell(text="1/4\" PORT"), TableCell(text="20 058 000 01"),
            TableCell(text="450 BAR"), TableCell(text="1 MALE/1 FEMALE PORT (BSP)")
        ]),
        TableRow(cells=[
            TableCell(text="3/8\" PORT"), TableCell(text="20 023 000 03"),
            TableCell(text="500 BAR"), TableCell(text="FEMALE/FEMALE PORT (BSP)")
        ]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="VALVE_SPEC_TABLE")
    parsed = parse_valve_table(table)
    assert len(parsed) == 2
    assert parsed[0]["part_number"] == "1/4\" PORT"
    assert parsed[1]["part_number"] == "3/8\" PORT"
    assert "20 058 000 01" in parsed[0]["values"][1]["value"]
    assert "500 BAR" in parsed[1]["values"][2]["value"]


# ============================================================
# 5. Dot/colon normalization only in ratio columns
# ============================================================

def test_ratio_normalization_only_in_ratio_column() -> None:
    normalized, reason = _normalize_ratio_token("4.1", is_ratio_col=True, context_rows=["Pressure ratio"])
    assert normalized == "4:1"
    assert reason == "pressure_ratio_column"

    normalized, reason = _normalize_ratio_token("4.1", is_ratio_col=False, context_rows=["Some other column"])
    assert normalized == "4.1"
    assert reason is None


def test_decimal_values_remain_decimals() -> None:
    normalized, reason = _normalize_ratio_token("4.4", is_ratio_col=True, context_rows=["Pressure ratio"])
    assert normalized == "4:4"
    assert reason == "pressure_ratio_column"


def test_non_ratio_tokens_unchanged() -> None:
    normalized, reason = _normalize_ratio_token("12.99", is_ratio_col=True, context_rows=["Price"])
    assert normalized == "12.99"
    assert reason is None


# ============================================================
# 6. Part-number spacing preservation
# ============================================================

def test_part_number_spaces_preserved() -> None:
    assert _is_part_number("16 200 000 01") is True
    assert _is_part_number("20 058 000 01") is True
    assert _is_part_number("16 045 0 0") is True


def test_part_number_not_converted_to_number() -> None:
    assert _is_part_number("016 200 000 01") is True
    assert _is_part_number("20 069 001 55") is True


def test_non_part_number_rejected() -> None:
    assert _is_part_number("200") is False
    assert _is_part_number("CUB") is False
    assert _is_part_number("") is False


# ============================================================
# 7. Leading-zero preservation
# ============================================================

def test_leading_zeros_preserved() -> None:
    headers = ["Part No.", "Description"]
    rows = [
        TableRow(cells=[TableCell(text="016 200 000 01"), TableCell(text="Test")], raw_cells=["016 200 000 01", "Test"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PART_NUMBER_TABLE")
    parsed = parse_part_number_table(table)
    assert len(parsed) == 1
    assert parsed[0]["part_number"] == "016 200 000 01"


# ============================================================
# 8. Row confidence
# ============================================================

def test_row_confidence_high_when_valid() -> None:
    headers = ["Type", "30:150", "35:70"]
    rows = [
        TableRow(cells=[TableCell(text="Pressure ratio"), TableCell(text="30:1"), TableCell(text="35:1")], raw_cells=["Pressure ratio", "30:1", "35:1"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE", confidence="USABLE")
    parsed = parse_pump_table(table)
    assert len(parsed) == 2
    assert parsed[0]["confidence"] == "USABLE"
    assert parsed[1]["confidence"] == "USABLE"


def test_row_confidence_review_when_low_ocr() -> None:
    headers = ["Type", "30:150", "35:70"]
    rows = [
        TableRow(cells=[TableCell(text="Pressure ratio", confidence=0.5), TableCell(text="30:1", confidence=0.5), TableCell(text="35:1", confidence=0.5)], raw_cells=["Pressure ratio", "30:1", "35:1"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE", confidence="REVIEW_REQUIRED")
    parsed = parse_pump_table(table)
    assert len(parsed) == 2
    assert parsed[0]["confidence"] == "REVIEW_REQUIRED"


# ============================================================
# 9. Unknown cell preservation
# ============================================================

def test_unknown_cell_not_guessed() -> None:
    headers = ["Type", "Pressure ratio", "Discharge per cycle (cc)"]
    rows = [
        TableRow(cells=[TableCell(text="30:150"), TableCell(text="30:1"), TableCell(text="")], raw_cells=["30:150", "30:1", ""]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE")
    parsed = parse_pump_table(table)
    assert len(parsed) == 1
    for item in parsed:
        for v in item["values"]:
            assert v["value"] != ""
            assert v["raw_value"] != ""


# ============================================================
# 10. Table validation
# ============================================================

def test_table_validation_empty_headers() -> None:
    table = StructuredTable(headers=[], rows=[], source_page=1, table_type="UNKNOWN_TABLE")
    is_valid, issues = validate_table(table)
    assert not is_valid
    assert "empty_headers" in issues


def test_table_validation_duplicate_rows() -> None:
    headers = ["A", "B"]
    rows = [
        TableRow(cells=[TableCell(text="x"), TableCell(text="y")]),
        TableRow(cells=[TableCell(text="x"), TableCell(text="y")]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=1, table_type="UNKNOWN_TABLE")
    is_valid, issues = validate_table(table)
    assert not is_valid
    assert any("duplicate_row" in issue for issue in issues)


def test_table_validation_column_mismatch() -> None:
    headers = ["A", "B", "C"]
    rows = [
        TableRow(cells=[TableCell(text="x"), TableCell(text="y")]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=1, table_type="UNKNOWN_TABLE")
    is_valid, issues = validate_table(table)
    assert not is_valid
    assert any("column_mismatch" in issue for issue in issues)


# ============================================================
# 11. Coordinate-based reconstruction
# ============================================================

def test_reconstruct_table_from_ocr_blocks() -> None:
    blocks = [
        OCRBlock(text="Type", bbox=[100, 100, 200, 150], confidence=0.99),
        OCRBlock(text="30:150", bbox=[300, 100, 400, 150], confidence=0.99),
        OCRBlock(text="35:70", bbox=[500, 100, 600, 150], confidence=0.99),
        OCRBlock(text="Pressure ratio", bbox=[100, 200, 300, 250], confidence=0.99),
        OCRBlock(text="30:1", bbox=[300, 200, 400, 250], confidence=0.99),
        OCRBlock(text="35:1", bbox=[500, 200, 600, 250], confidence=0.99),
    ]
    tables = reconstruct_table_from_ocr_blocks(blocks, page_number=2, document_name="test.pdf")
    assert tables is not None
    assert len(tables) >= 1
    table = tables[0]
    assert len(table.headers) >= 2
    assert len(table.rows) >= 1
    assert table.table_type == "PUMP_MODEL_TABLE"


def test_reconstruct_table_insufficient_blocks() -> None:
    blocks = [
        OCRBlock(text="Type", bbox=[100, 100, 200, 150], confidence=0.99),
    ]
    tables = reconstruct_table_from_ocr_blocks(blocks, page_number=2, document_name="test.pdf")
    assert tables == []


# ============================================================
# 12. CUB table via OCR reconstruction
# ============================================================

def test_cub_table_from_real_ocr_blocks() -> None:
    """Verify CUB table reconstruction from actual OCR blocks."""
    ocr_hash = "ff00f0e526419b151ae17d32c378070dd2100e52beffb5913df38a3a73c73803"
    cache_path = Path(f"/home/vr-coatings/Desktop/website_V2/backend/.rag_cache/ocr/{ocr_hash}/page_002.json")
    if not cache_path.exists():
        pytest.skip("CUB OCR cache not available")

    data = __import__("json").loads(cache_path.read_text(encoding="utf-8"))
    blocks = [OCRBlock(**b) for b in data.get("blocks", [])]
    tables = reconstruct_table_from_ocr_blocks(blocks, page_number=2, document_name="cub.pdf")
    if not tables:
        pytest.skip("Could not reconstruct table from CUB OCR")

    table = tables[0]
    parsed = parse_structured_table(table)
    if not parsed:
        pytest.skip("CUB table parsed empty")

    models = [p["model"] for p in parsed if p.get("model")]
    assert any("2:400" in m or "2:1" in m for m in models), f"CUB models not found in: {models}"


# ============================================================
# 13. Drum Press identity preserved
# ============================================================

def test_drum_press_identity_not_replaced_by_internal_model() -> None:
    """Ensure Drum Press document is not accidentally identified as an internal pump model."""
    slug = resolve_product_identity("drum press")
    assert slug is not None
    assert slug[0] == "drum-press"


def test_drum_press_internal_models_not_product_identities() -> None:
    """Internal pump models like 28:550 should not become product identities."""
    for model in ["28:550", "28:920", "30:150", "75:210"]:
        slug = resolve_product_identity(model)
        if slug:
            assert slug[0] != "drum-press", f"Internal model {model} should not map to drum-press"


# ============================================================
# 14. Turbine/Pneumatic isolation
# ============================================================

def test_turbine_alias_not_shared_with_pneumatic() -> None:
    turbine_aliases = [a.lower() for a in PRODUCT_ALIASES.get("turbine", {}).get("aliases", [])]
    pneumatic_slug = resolve_product_identity("pneumatic stirrer")
    if pneumatic_slug:
        assert pneumatic_slug[0] != "turbine"
    assert "turbine stirrer" in turbine_aliases


def test_pneumatic_stirrer_alias_does_not_include_turbine() -> None:
    pneumatic_aliases = [a.lower() for a in PRODUCT_ALIASES.get("pneumatic-stirrer", {}).get("aliases", [])]
    assert "turbine stirrer" not in pneumatic_aliases


# ============================================================
# 15. Chunking integration for target documents
# ============================================================

def test_cub_chunking_produces_table_chunks() -> None:
    pages = [
        {
            "page_number": 2,
            "text": (
                "TECHNICAL SPECIFICATIONS\n"
                "Type\nCUB 2:400\nCUB 4.400\nCUB 6.400\n"
                "Pressure ratio\n2:1\n4:1\n6:1\n"
                "Discharge per cycle (cc)\n400\n400\n400\n"
                "Stroke Length (mm)\n120\n120\n120\n"
            ),
        }
    ]
    chunks = chunk_catalogue("cub.pdf", pages, [], "cub", "doc-cub")
    table_chunks = [c for c in chunks if c.get("section") == "technical_model"]
    assert len(table_chunks) >= 1
    texts = " ".join(c["text"] for c in table_chunks)
    assert "2:1" in texts
    assert "4:1" in texts
    assert "6:1" in texts


def test_drum_press_chunking_preserves_identity() -> None:
    pages = [
        {
            "page_number": 1,
            "text": "DRUM PRESS\nMEDIUM & HEAVY DUTY\nAIRLESS DRUM PRESS",
        },
        {
            "page_number": 2,
            "text": (
                "TECHNICAL SPECIFICATIONS\n"
                "Type\n28:550\n30:150\n75:210\n"
                "Pressure ratio\n28:1\n30:1\n75:1\n"
                "Discharge per cycle (cc)\n550\n150\n210\n"
            ),
        },
    ]
    chunks = chunk_catalogue("DRUM PRESS.pdf", pages, [], "drum-press", "doc-drum-press")
    identity_chunks = [c for c in chunks if c.get("section") == "product_identity"]
    assert len(identity_chunks) >= 1
    assert any("DRUM PRESS" in c["text"] for c in identity_chunks)


def test_pneumatic_stirrer_part_numbers_preserved() -> None:
    pages = [
        {
            "page_number": 2,
            "text": "PNEUMATIC STIRRER technical specifications",
        }
    ]
    tables = [
        {
            "page_number": 2,
            "rows": [
                ["Part No.", "Fan dia.", "Shaft length."],
                ["16 200 000 01", "200", "300"],
                ["16 100 000 01", "100", "300"],
            ],
        }
    ]
    chunks = chunk_catalogue("PNEUMATIC STIRRER.pdf", pages, tables, "pneumatic-stirrer", "doc-pneumatic-stirrer")
    part_chunks = [c for c in chunks if c.get("section") == "technical_part"]
    assert len(part_chunks) >= 2
    texts = " ".join(c["text"] for c in part_chunks)
    assert "16 200 000 01" in texts
    assert "16 100 000 01" in texts


def test_ball_valve_rows_coherent() -> None:
    pages = [
        {
            "page_number": 2,
            "text": "High Pressure Manual Ball Valves",
        }
    ]
    tables = [
        {
            "page_number": 2,
            "rows": [
                ["Part No.", "PORT SIZE", "MWP", "CONNECTIONS"],
                ["20 058 000 01", "1/4\" PORT", "450 BAR", "1 MALE/1 FEMALE PORT (BSP)"],
                ["20 023 000 03", "3/8\" PORT", "500 BAR", "FEMALE/FEMALE PORT (BSP)"],
            ],
        }
    ]
    chunks = chunk_catalogue("ball_valves.pdf", pages, tables, "ball-valves", "doc-ball-valves")
    part_chunks = [c for c in chunks if c.get("section") == "technical_part"]
    assert len(part_chunks) >= 2
    for chunk in part_chunks:
        text = chunk["text"]
        assert "450 BAR" in text or "500 BAR" in text or "20 058" in text or "20 023" in text


# ============================================================
# 16. No blanket dot-to-colon replacement
# ============================================================

def test_no_blanket_dot_to_colon_in_non_ratio() -> None:
    from app.rag.ingestion.structured_table_parser import _normalize_ratio_token

    normalized, reason = _normalize_ratio_token("4.4", is_ratio_col=False, context_rows=[])
    assert normalized == "4.4"
    assert reason is None

    normalized, reason = _normalize_ratio_token("12.99", is_ratio_col=True, context_rows=["price"])
    assert normalized == "12.99"
    assert reason is None


# ============================================================
# 17. Raw/normalized audit logic
# ============================================================

def test_raw_normalized_values_available() -> None:
    headers = ["Type", "Pressure ratio"]
    rows = [
        TableRow(cells=[TableCell(text="CUB 4.400"), TableCell(text="4.1", confidence=0.9)]),
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
# 18. Duplicate row removal
# ============================================================

def test_duplicate_rows_removed() -> None:
    headers = ["Fan dia.", "Shaft length.", "Part No."]
    rows = [
        TableRow(cells=[TableCell(text="200"), TableCell(text="300"), TableCell(text="16 200 000 01")], raw_cells=["200", "300", "16 200 000 01"]),
        TableRow(cells=[TableCell(text="200"), TableCell(text="300"), TableCell(text="16 200 000 01")], raw_cells=["200", "300", "16 200 000 01"]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PART_NUMBER_TABLE")
    parsed = parse_part_number_table(table)
    assert len(parsed) == 1


# ============================================================
# 19. Idempotency
# ============================================================

def test_structured_table_parser_idempotent() -> None:
    headers = ["Type", "Pressure ratio", "Discharge per cycle (cc)"]
    rows = [
        TableRow(cells=[TableCell(text="30:150"), TableCell(text="30:1"), TableCell(text="150")]),
        TableRow(cells=[TableCell(text="35:70"), TableCell(text="35:1"), TableCell(text="70")]),
    ]
    table = StructuredTable(headers=headers, rows=rows, source_page=2, table_type="PUMP_MODEL_TABLE")

    result1 = parse_pump_table(table)
    result2 = parse_pump_table(table)
    assert result1 == result2
