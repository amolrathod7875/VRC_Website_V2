"""Phase 8 regression tests for multi-catalogue ingestion."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.metadata_builder import build_catalogue_metadata
from app.rag.constants import CATALOGUE_AUTHORITY_PRIORITY, SOURCE_TYPE_CATALOGUE
def test_lion_catalogue_chunks_preserve_product_slug() -> None:
    pages = [
        {"page_number": 1, "text": "LION\nHydraulic high-volume fluid transfer pump"},
        {"page_number": 2, "text": "LION is a hydraulically driven pump. Pressure Ratio 0.14:1"},
    ]
    tables = []
    chunks = chunk_catalogue("LION_Catalogue.pdf", pages, tables, "lion", "doc-1")
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk["product_slug"] == "lion"
        assert chunk["source_type"] == SOURCE_TYPE_CATALOGUE
        assert chunk["authority_priority"] == CATALOGUE_AUTHORITY_PRIORITY
def test_lion_catalogue_metadata_contains_document_id() -> None:
    chunk = {
        "chunk_id": "doc-1::chunk::0",
        "source_type": SOURCE_TYPE_CATALOGUE,
        "source_authority": "primary",
        "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
        "document_name": "LION_Catalogue.pdf",
        "product": "LION",
        "product_slug": "lion",
        "section": "description",
        "content_type": "description",
        "page_number": 2,
        "line_start": 1,
        "line_end": 3,
        "model": None,
        "text": "LION is a hydraulically driven pump.",
    }
    metadata = build_catalogue_metadata("doc-1", "LION_Catalogue.pdf", "/path/to/LION.pdf", "sha256", "lion", chunk)
    assert metadata["document_id"] == "doc-1"
    assert metadata["product_slug"] == "lion"
    assert metadata["authority_priority"] == CATALOGUE_AUTHORITY_PRIORITY
    assert metadata["source_type"] == SOURCE_TYPE_CATALOGUE
def test_lion_catalogue_preserves_exact_model_identifiers() -> None:
    pages = [
        {"page_number": 2, "text": "Pressure Ratio 0.14:1 Hydraulic Motor Type (mm) D66"},
    ]
    tables = [
        {
            "page_number": 2,
            "rows": [
                ["Specification", "Value"],
                ["Pressure Ratio", "0.14:1"],
                ["Hydraulic Capacity", "4000 cc"],
            ],
        }
    ]
    chunks = chunk_catalogue("LION_Catalogue.pdf", pages, tables, "lion", "doc-1")
    technical_chunks = [c for c in chunks if c.get("section") == "technical_model"]
    assert len(technical_chunks) > 0
    for chunk in technical_chunks:
        text = chunk.get("text", "")
        assert "0.14:1" in text or "Pressure Ratio" in text
def test_multi_catalogue_manifest_detects_text_capable() -> None:
    from app.rag.ingestion.pdf_parser import extract_pages
    from app.rag.ingestion.pdf_table_parser import extract_tables

    lion_path = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues/LION_Catalogue.pdf")
    tiger_path = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues/Tiger.pdf")

    lion_pages, _ = extract_pages(str(lion_path), enable_ocr=False)
    tiger_pages, _ = extract_pages(str(tiger_path), enable_ocr=False)

    lion_text = "".join(p.get("text", "") for p in lion_pages)
    tiger_text = "".join(p.get("text", "") for p in tiger_pages)

    assert len(lion_text.strip()) > 100, "LION should have extractable text"
    assert len(tiger_text.strip()) == 0, "Tiger.pdf should have no extractable text without OCR"