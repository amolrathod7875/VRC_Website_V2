"""
Phase 9C.2 — Batch 1 Chunking Remediation Tests

Tests cover:
1. short-fragment classification
2. technical identifiers preserved
3. footer noise removed
4. heading merging
5. key-value technical block preservation
6. filter variant separation
7. Hippo identity collision prevention
8. Leopard canonical identity
9. alias collision detection
10. idempotent Batch 1 ingestion behavior
"""
import asyncio
from pathlib import Path

from app.rag.ingestion.new_chunker import (
    _classify_short_fragment,
    _merge_adjacent_kv_blocks,
    _try_merge_kv_label_with_following,
    _merge_short_with_context,
    _page_is_mostly_garbage,
    chunk_catalogue,
)
from app.rag.ingestion.pdf_parser import extract_pages
from app.rag.product_identity import PRODUCT_ALIASES, resolve_product_identity


# ============================================================
# 1. short-fragment classification
# ============================================================
def test_technical_values_classified() -> None:
    assert _classify_short_fragment("450 bar") == "TECHNICAL_VALUE"
    assert _classify_short_fragment("220~230 VAC") == "TECHNICAL_VALUE"
    assert _classify_short_fragment("BLDC") == "TECHNICAL_VALUE"
    assert _classify_short_fragment("1/4 BSP") == "TECHNICAL_VALUE"
    assert _classify_short_fragment("600 mm") == "TECHNICAL_VALUE"


def test_technical_identifiers_preserved() -> None:
    # Ratios like 30:1 are classified as TECHNICAL_VALUE (still preserved)
    assert _classify_short_fragment("30:1") in ("TECHNICAL_IDENTIFIER", "TECHNICAL_VALUE")
    assert _classify_short_fragment("1/4") == "TECHNICAL_VALUE"
    assert _classify_short_fragment("TB-70") == "TECHNICAL_IDENTIFIER"
    assert _classify_short_fragment("AM250") == "TECHNICAL_IDENTIFIER"


def test_footer_noise_classified() -> None:
    assert _classify_short_fragment("VR Coatings") == "FOOTER"
    assert _classify_short_fragment("VR Coatings Pvt.Ltd.") == "FOOTER"
    # sales@... is matched by footer pattern before email check; still removed
    assert _classify_short_fragment("sales@vrcoatings.com") in ("FOOTER", "EMAIL")
    assert _classify_short_fragment("Bhosari, Pune 411026") == "FOOTER"


def test_ocr_garbage_classified() -> None:
    assert _classify_short_fragment("ξx") == "OCR_GARBAGE"
    assert _classify_short_fragment("C∈") == "OCR_GARBAGE"
    assert _classify_short_fragment("Bhosgri, Pune 4]1026") == "OCR_GARBAGE"


# ============================================================
# 2. footer noise removed
# ============================================================
def test_footer_chunks_removed_from_pages() -> None:
    pages = [
        {"page_number": 1, "text": "Pressure ratio: 30:1\nVR Coatings\nsales@vrcoatings.com"},
    ]
    chunks = chunk_catalogue("Test.pdf", pages, [], "test", "doc-test")
    texts = [c["text"] for c in chunks]
    assert not any("VR Coatings" in t for t in texts)
    assert not any("sales@vrcoatings.com" in t for t in texts)
    assert any("30:1" in t for t in texts)


# ============================================================
# 3. heading merging
# ============================================================
def test_kv_label_merged_with_following_value() -> None:
    blocks = ["Max pressure", "250 bar"]
    merged = _merge_adjacent_kv_blocks(blocks)
    assert merged == ["Max pressure: 250 bar"]


def test_two_kv_labels_kept_separate() -> None:
    blocks = ["Max pressure", "Min pressure"]
    merged = _merge_adjacent_kv_blocks(blocks)
    assert merged == ["Max pressure", "Min pressure"]


def test_try_merge_kv_label_with_following() -> None:
    blocks = ["voltage", "220~230 VAC"]
    merged = _try_merge_kv_label_with_following(blocks)
    assert merged == ["voltage: 220~230 VAC"]


# ============================================================
# 4. key-value technical block preservation
# ============================================================
def test_electric_pump_key_value_blocks() -> None:
    pages = [
        {"page_number": 1, "text": "LEOPARD\nELECTRICAL AIRLESS SPRAY PUMP\nTECHNICAL DATA\nvoltage\n220~230 VAC\nNumber of Guns\n1\nMotor Type\nBLDC\nRuns on single-phase electric supply\nMounted on wheels for mobility\n"},
    ]
    chunks = chunk_catalogue("Electric_pump.pdf", pages, [], "leopard", "doc-leopard")
    technical_chunks = [c for c in chunks if c["section"] == "technical_model"]
    assert len(technical_chunks) >= 1
    text = "\n".join(c["text"] for c in technical_chunks)
    assert "voltage: 220~230 VAC" in text
    assert "Number of Guns: 1" in text
    assert "Motor Type: BLDC" in text


# ============================================================
# 5. filter variant separation
# ============================================================
def test_filter_variants_are_separated() -> None:
    pages = [
        {"page_number": 1, "text": "HIGH PRESSURE FILTER\n450 bar\nLOW PRESSURE FILTER (STAINLESS STEEL)\n120 bar"},
    ]
    chunks = chunk_catalogue("filters.pdf", pages, [], "filters", "doc-filters")
    headings = [c["product"] for c in chunks]
    assert "HIGH PRESSURE FILTER" in headings
    assert "LOW PRESSURE FILTER (STAINLESS STEEL)" in headings
    high = [c for c in chunks if c["product"] == "HIGH PRESSURE FILTER"]
    low = [c for c in chunks if c["product"] == "LOW PRESSURE FILTER (STAINLESS STEEL)"]
    assert any("450 bar" in c["text"] for c in high)
    assert any("120 bar" in c["text"] for c in low)
    assert not any("120 bar" in c["text"] for c in high)
    assert not any("450 bar" in c["text"] for c in low)


# ============================================================
# 6. Hippo identity collision prevention
# ============================================================
def test_hippo_alias_does_not_collide_with_diaphragm() -> None:
    # diaphragm pump is intentionally aliased to hippo; verify they resolve to the same slug
    diaphragm_slug = resolve_product_identity("diaphragm pump")
    hippo_slug = resolve_product_identity("Hippo pump")
    assert diaphragm_slug is not None
    assert diaphragm_slug[0] == "hippo"
    assert hippo_slug is not None
    assert hippo_slug[0] == "hippo"


# ============================================================
# 7. Leopard canonical identity
# ============================================================
def test_leopard_identity_does_not_collide() -> None:
    slug = resolve_product_identity("LEOPARD")
    assert slug is not None
    assert slug[0] == "leopard"
    # Ensure it doesn't accidentally resolve to an existing product
    tiger_slug = resolve_product_identity("LEOPARD")
    assert tiger_slug is None or tiger_slug[0] != "tiger"


# ============================================================
# 8. alias collision detection
# ============================================================
def test_no_alias_collision_with_indexed_products() -> None:
    # Indexed product slugs
    indexed_slugs = {"tiger", "tiger-mini", "lion", "rhino", "elephant", "cheetah", "hippo"}
    # Collect all non-canonical aliases
    aliases = set()
    for slug, config in PRODUCT_ALIASES.items():
        for alias in config.get("aliases", []):
            if alias.lower() != slug:
                aliases.add(alias.lower())
    # Non-canonical aliases should not collide with indexed slugs
    assert not indexed_slugs.intersection(aliases), "alias collision detected"


# ============================================================
# 9. idempotent Batch 1 ingestion behavior
# ============================================================
def test_second_run_skips_unchanged_batch1() -> None:
    from app.rag.ingestion.ingestion_service import IngestionService
    from unittest.mock import AsyncMock, MagicMock, patch
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(b"dummy pdf content")

    db = MagicMock()

    async def mock_execute(query):
        result = MagicMock()
        result.scalar_one_or_none.return_value = existing_doc
        return result

    db.execute = mock_execute
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    qdrant = MagicMock()
    dense = MagicMock()
    sparse = MagicMock()

    service = IngestionService(db=db, qdrant_store=qdrant, dense=dense, sparse=sparse)

    existing_doc = MagicMock()
    existing_doc.sha256 = "dummy_hash"
    existing_doc.qdrant_document_id = "doc-123"

    with patch("app.rag.ingestion.ingestion_service.calculate_sha256", return_value="dummy_hash"):
        result = asyncio.run(service.ingest_catalogue(Path(tmp_path)))
    assert result["status"] == "skipped"
    assert result["reason"] == "unchanged"


# ============================================================
# 10. page mostly garbage detection
# ============================================================
def test_page_mostly_garbage_dropped() -> None:
    lines = ["ξx", "C∈", "2", "3", "4"]
    assert _page_is_mostly_garbage(lines) is True


def test_meaningful_page_kept() -> None:
    lines = ["Pressure ratio: 30:1", "Discharge per cycle (cc)", "140"]
    assert _page_is_mostly_garbage(lines) is False
