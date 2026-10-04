"""
Phase 9C.3 — Batch 2 Chunking Remediation Tests

Tests cover:
1. section heading does not imply table
2. accessory key/value merging
3. short technical value preservation
4. cover/title page preservation
5. garbage page filtering
6. Paint Preparation section chunking
7. Pressure Feed Pot technical spec grouping
8. Turbine variant preservation
9. TB-70 / TB-110 / TB-180 identifier preservation
10. alias collision detection
11. turbine vs pneumatic-stirrer collision prevention
12. duplicate removal
13. second-run idempotency
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
# 1. section heading does not imply table
# ============================================================
def test_technical_specifications_heading_does_not_trigger_table() -> None:
    pages = [
        {"page_number": 1, "text": "TECHNICAL SPECIFICATIONS\nCAPACITY\n6 KW\nPOWER SUPPLY\n230 V AC 50HZ"},
    ]
    chunks = chunk_catalogue("test.pdf", pages, [], "test", "doc-test")
    table_chunks = [c for c in chunks if c.get("section") == "technical_table"]
    assert len(table_chunks) == 0, "TECHNICAL SPECIFICATIONS heading alone should not create a table chunk"


# ============================================================
# 2. accessory key/value merging
# ============================================================
def test_paint_preparation_kv_merging() -> None:
    pages = [
        {"page_number": 1, "text": "TECHNICAL SPECIFICATIONS\nCAPACITY\n6 KW\nPOWER SUPPLY\n230 V AC 50HZ\nTEMPERATURE\nIS 2148 WEATHER PROOF IP 55"},
    ]
    chunks = chunk_catalogue("Paint Preparation Unit.pdf", pages, [], "paint-preparation-unit", "doc-ppu")
    technical_chunks = [c for c in chunks if c.get("section") == "technical_model"]
    assert len(technical_chunks) >= 1
    text = "\n".join(c["text"] for c in technical_chunks)
    assert "CAPACITY: 6 KW" in text
    assert "POWER SUPPLY: 230 V AC 50HZ" in text
    assert "TEMPERATURE: IS 2148 WEATHER PROOF IP 55" in text


def test_pressure_feed_pot_kv_merging() -> None:
    pages = [
        {"page_number": 1, "text": "TECHNICAL SPECIFICATIONS\nPot capacity\n2.5 Itrs Approx\nMax. Working Pressure\n4 Bar\nNet Wt.\n3 Kg."},
    ]
    chunks = chunk_catalogue("PORTABLE PRESSURE FEED POT.pdf", pages, [], "portable-pressure-feed-pot", "doc-pfp")
    technical_chunks = [c for c in chunks if c.get("section") == "technical_model"]
    assert len(technical_chunks) >= 1
    text = "\n".join(c["text"] for c in technical_chunks)
    assert "Pot capacity: 2.5 Itrs Approx" in text
    assert "Max. Working Pressure: 4 Bar" in text
    assert "Net Wt.: 3 Kg." in text


# ============================================================
# 3. short technical value preservation
# ============================================================
def test_short_technical_values_not_dropped() -> None:
    pages = [
        {"page_number": 1, "text": "4 Bar\n3 Kg\n2.5 Ltrs\n230 V AC"},
    ]
    chunks = chunk_catalogue("test.pdf", pages, [], "test", "doc-test")
    texts = " ".join(c["text"] for c in chunks)
    assert "4 Bar" in texts
    assert "3 Kg" in texts
    assert "2.5 Ltrs" in texts or "2.5 Itrs" in texts


# ============================================================
# 4. cover/title page preservation
# ============================================================
def test_paint_preparation_identity_preserved() -> None:
    pages = [
        {"page_number": 1, "text": "PAINT PREPARATION\nVR Coatings\nUNIT\n200LTR BARREL"},
    ]
    chunks = chunk_catalogue("Paint Preparation Unit.pdf", pages, [], "paint-preparation-unit", "doc-ppu")
    identity_chunks = [c for c in chunks if c.get("section") == "product_identity"]
    assert len(identity_chunks) >= 1
    assert any("PAINT PREPARATION" in c["text"] for c in identity_chunks)


def test_turbine_identity_preserved() -> None:
    pages = [
        {"page_number": 1, "text": "TURBINE\nSTIRRERS\nPaint Agitation System\nV R COATINGS PVT. LTD."},
    ]
    chunks = chunk_catalogue("turbine.pdf", pages, [], "turbine", "doc-turbine")
    identity_chunks = [c for c in chunks if c.get("section") == "product_identity"]
    assert len(identity_chunks) >= 1
    assert any("TURBINE" in c["text"] for c in identity_chunks)


# ============================================================
# 5. garbage page filtering
# ============================================================
def test_garbage_page_dropped() -> None:
    pages = [
        {"page_number": 1, "text": "ξx\nC∈\n2\n3\n4\nC\n∈"},
    ]
    chunks = chunk_catalogue("test.pdf", pages, [], "test", "doc-test")
    assert len(chunks) == 0


def test_mostly_garbage_page_dropped() -> None:
    pages = [
        {"page_number": 1, "text": "some text\nξx\nC∈\n2\n3\n4"},
    ]
    chunks = chunk_catalogue("test.pdf", pages, [], "test", "doc-test")
    assert len(chunks) == 0


# ============================================================
# 6. Paint Preparation section chunking
# ============================================================
def test_paint_preparation_has_expected_sections() -> None:
    file_path = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues/Paint Preparation Unit.pdf")
    pages, _ = extract_pages(str(file_path), enable_ocr=True)
    chunks = chunk_catalogue("Paint Preparation Unit.pdf", pages, [], "paint-preparation-unit", "doc-ppu")
    sections = {c.get("section") for c in chunks}
    assert "product_identity" in sections
    assert "description" in sections
    assert "applications" in sections
    assert "technical_model" in sections


# ============================================================
# 7. Pressure Feed Pot technical spec grouping
# ============================================================
def test_pressure_feed_pot_technical_specs() -> None:
    file_path = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues/PORTABLE PRESSURE FEED POT.pdf")
    pages, _ = extract_pages(str(file_path), enable_ocr=True)
    chunks = chunk_catalogue("PORTABLE PRESSURE FEED POT.pdf", pages, [], "portable-pressure-feed-pot", "doc-pfp")
    technical_chunks = [c for c in chunks if c.get("section") == "technical_model"]
    assert len(technical_chunks) >= 1
    text = "\n".join(c["text"] for c in technical_chunks)
    assert "2.5" in text
    assert "4 Bar" in text
    assert "3 Kg" in text


# ============================================================
# 8. Turbine variant preservation
# ============================================================
def test_turbine_variants_extracted() -> None:
    file_path = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues/turbine.pdf")
    pages, _ = extract_pages(str(file_path), enable_ocr=True)
    chunks = chunk_catalogue("turbine.pdf", pages, [], "turbine", "doc-turbine")
    variant_chunks = [c for c in chunks if c.get("section") == "technical_variant"]
    assert len(variant_chunks) >= 3
    variant_ids = set()
    for c in variant_chunks:
        text = c.get("text", "")
        if text.startswith("TB-"):
            variant_ids.add(text.split(":")[0].strip())
    assert "TB-70" in variant_ids
    assert "TB-110" in variant_ids
    assert "TB-180" in variant_ids


# ============================================================
# 9. TB-70 / TB-110 / TB-180 identifier preservation
# ============================================================
def test_tb_identifiers_preserved() -> None:
    assert _classify_short_fragment("TB-70") == "TECHNICAL_IDENTIFIER"
    assert _classify_short_fragment("TB-110") == "TECHNICAL_IDENTIFIER"
    assert _classify_short_fragment("TB-180") == "TECHNICAL_IDENTIFIER"


# ============================================================
# 10. alias collision detection
# ============================================================
def test_no_alias_collision_with_indexed_products() -> None:
    indexed_slugs = {"tiger", "tiger-mini", "lion", "rhino", "elephant", "cheetah", "hippo", "leopard", "filters"}
    aliases = set()
    for slug, config in PRODUCT_ALIASES.items():
        for alias in config.get("aliases", []):
            if alias.lower() != slug:
                aliases.add(alias.lower())
    assert not indexed_slugs.intersection(aliases), "alias collision detected"


# ============================================================
# 11. turbine vs pneumatic-stirrer collision prevention
# ============================================================
def test_turbine_alias_does_not_collide_with_pneumatic_stirrer() -> None:
    turbine_aliases = [a.lower() for a in PRODUCT_ALIASES.get("turbine", {}).get("aliases", [])]
    # Pneumatic stirrer aliases should not contain "turbine" or "turbine stirrer"
    # Verify turbine aliases are distinct from pneumatic-stirrer concepts
    assert "turbine" in turbine_aliases
    assert "turbine stirrer" in turbine_aliases
    # Ensure "turbine stirrer" is NOT also registered under pneumatic stirrer (not yet indexed)
    # This test verifies the current state; when pneumatic stirrer is indexed,
    # it must NOT use "turbine stirrer" as an alias
    pneumatic_slug = resolve_product_identity("pneumatic stirrer")
    if pneumatic_slug:
        assert pneumatic_slug[0] != "turbine", "turbine and pneumatic stirrer must not share aliases"


# ============================================================
# 12. duplicate removal
# ============================================================
def test_duplicate_chunks_removed() -> None:
    pages = [
        {"page_number": 1, "text": "description text\nmore description\nTECHNICAL SPECIFICATIONS\n4 Bar\n4 Bar"},
    ]
    chunks = chunk_catalogue("test.pdf", pages, [], "test", "doc-test")
    texts = [c["text"] for c in chunks]
    assert len(texts) == len(set(texts)), "duplicate chunks should be removed"


# ============================================================
# 13. second-run idempotency
# ============================================================
def test_second_run_skips_unchanged_batch2() -> None:
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
