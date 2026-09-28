from app.rag.ingestion.ocr.base import OCRBlock, OCRPageResult, OCRProvider
from app.rag.ingestion.ocr.ocr_service import OCRCache, _serialize_blocks, _deserialize_blocks
from app.rag.ingestion.pdf_table_parser import extract_tables_from_ocr, parse_spec_table


def test_ocr_cache_roundtrip_preserves_blocks() -> None:
    cache = OCRCache(base_dir=".tmp_test_ocr_cache")
    document_hash = "abc123"
    page_number = 1
    result = OCRPageResult(
        page_number=page_number,
        full_text="hello world",
        blocks=[OCRBlock(text="hello", bbox=[0, 0, 10, 10], confidence=0.9)],
        tables=[],
        warnings=[],
        confidence=0.9,
    )
    cache.put(document_hash, page_number, result)
    loaded = cache.get(document_hash, page_number)
    assert loaded is not None
    assert loaded.page_number == page_number
    assert loaded.full_text == "hello world"
    assert len(loaded.blocks) == 1
    assert loaded.blocks[0].text == "hello"
    assert loaded.blocks[0].confidence == 0.9


def test_ocr_cache_roundtrip_preserves_tables() -> None:
    from app.rag.ingestion.ocr.base import OCRTable

    cache = OCRCache(base_dir=".tmp_test_ocr_cache_2")
    result = OCRPageResult(
        page_number=1,
        full_text="",
        blocks=[],
        tables=[OCRTable(bbox=[0, 0, 100, 100], rows=[["a", "b"]], confidence=0.8)],
        warnings=[],
        confidence=0.8,
    )
    cache.put("doc2", 1, result)
    loaded = cache.get("doc2", 1)
    assert loaded is not None
    assert len(loaded.tables) == 1
    assert loaded.tables[0].rows == [["a", "b"]]
    assert loaded.tables[0].confidence == 0.8


def test_ocr_block_serialization_roundtrip() -> None:
    blocks = [
        OCRBlock(text="test", bbox=[1, 2, 3, 4], block_type="text", confidence=0.5),
        OCRBlock(text="num", bbox=[10, 20, 30, 40], confidence=None),
    ]
    serialized = _serialize_blocks(blocks)
    deserialized = _deserialize_blocks(serialized)
    assert len(deserialized) == 2
    assert deserialized[0].text == "test"
    assert deserialized[0].bbox == [1, 2, 3, 4]
    assert deserialized[0].confidence == 0.5
    assert deserialized[1].text == "num"
    assert deserialized[1].confidence is None


def test_extract_tables_from_ocr_empty_without_technical_section() -> None:
    result = OCRPageResult(
        page_number=1,
        full_text="Some random text without table",
        blocks=[],
        tables=[],
        warnings=[],
        confidence=0.0,
    )
    tables = extract_tables_from_ocr([result])
    assert tables == []


def test_parse_spec_table_preserves_numeric_values() -> None:
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
    assert ":" not in model_a["values"][1]["value"] or "150" in model_a["values"][1]["value"]


def test_parse_spec_table_model_header_pattern() -> None:
    rows = [
        ["30:150", "35:70", "40:110"],
        ["30:1", "35:1", "40:1"],
        ["150", "70", "110"],
    ]
    parsed = parse_spec_table(rows)
    assert len(parsed) == 3
    assert {p["model"] for p in parsed} == {"30:150", "35:70", "40:110"}


def test_normal_fastapi_imports_without_paddle() -> None:
    import importlib
    import sys

    for mod_name in ["paddle", "paddleocr"]:
        if mod_name in sys.modules:
            del sys.modules[mod_name]

    import app.main  # noqa: F401


def test_paddle_ocr_provider_text_and_table_confidence() -> None:
    from unittest.mock import MagicMock
    from app.rag.ingestion.ocr.paddle_ocr import PaddleOCRProvider

    provider = PaddleOCRProvider(lang="en")
    mock_page_result = MagicMock()
    mock_page_result.rec_texts = ["hello", "180", "bar"]
    mock_page_result.rec_scores = [0.95, 0.92, 0.98]
    mock_page_result.rec_boxes = [[0, 0, 10, 10], [20, 20, 30, 30], [40, 40, 50, 50]]

    provider._client = MagicMock()
    provider._client.ocr.return_value = [mock_page_result]

    result = provider.process_page("/tmp/fake.png", 1)
    assert result.confidence is not None
    assert result.metadata["text_confidence"] is not None
    assert result.metadata["table_confidence"] is not None


def test_paddle_ocr_provider_warns_on_low_table_confidence() -> None:
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
