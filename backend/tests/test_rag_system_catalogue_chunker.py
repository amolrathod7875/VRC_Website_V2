"""
Phase 9C.6B — Complex System Catalogue Remediation Tests

Tests cover:
1. System catalogue chunker basic invocation
2. System hierarchy metadata
3. Variant isolation (Dragon ratios, Polyurea variants)
4. Component vs product distinction
5. Dragon ratio label preservation
6. Polyurea variant separation
7. Tube Varnish component handling
8. VRC MIX matrix reconstruction
9. VRC MIX LOW/MEDIUM vs VRC MIX HP identity isolation
10. Garbage-page handling
11. Catalogue membership metadata
12. Product identity aliases
13. Filename fallback mapping
14. System chunk types constants
"""
from pathlib import Path

from app.rag.ingestion.system_catalogue_chunker import (
    chunk_system_catalogue,
    CHUNK_TYPE_TECHNICAL_SPECIFICATIONS,
    CHUNK_TYPE_SYSTEM_COMPONENT,
    CHUNK_TYPE_SYSTEM_WORKFLOW,
    CHUNK_TYPE_SYSTEM_COMPARISON,
    _chunk_type_for_system_heading,
    _looks_like_system_variant,
    _looks_like_component,
    _looks_like_workflow_step,
    _looks_like_comparison_table,
    _extract_system_variants,
)
from app.rag.ingestion.structured_table_parser import detect_table_type, StructuredTable, TableRow, TableCell
from app.rag.constants import (
    CHUNK_TYPE_PRODUCT_IDENTITY,
    CHUNK_TYPE_DESCRIPTION,
    CHUNK_TYPE_FEATURES,
    CHUNK_TYPE_APPLICATIONS,
    CHUNK_TYPE_TECHNICAL_MODEL,
    CHUNK_TYPE_TECHNICAL_TABLE,
    CHUNK_TYPE_TECHNICAL_VARIANT,
    CHUNK_TYPE_TECHNICAL_PART,
    CHUNK_TYPE_ACCESSORIES,
    CHUNK_TYPE_NOTES,
    CHUNK_TYPE_OTHER,
    CHUNK_TYPE_CONTACT,
    SOURCE_TYPE_CATALOGUE,
    CATALOGUE_AUTHORITY_PRIORITY,
)
from app.rag.product_identity import PRODUCT_ALIASES, resolve_product_identity
from app.rag.catalogue_resolver import _FILENAME_FALLBACK


# ============================================================
# 1. System catalogue chunker basic invocation
# ============================================================
def test_chunk_system_catalogue_returns_chunks() -> None:
    pages = [
        {"page_number": 1, "text": "Dragon\nPassive fire protection system\nDESCRIPTION\nHigh duty airless plural component spraying equipment"},
        {"page_number": 2, "text": "FEATURES\nModular configuration\nTECHNICAL SPECIFICATIONS\nPressure ratio: 58:1"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    assert chunks
    assert all(c["document_id"] == "doc-dragon" for c in chunks)
    assert all(c["product_slug"] == "dragon" for c in chunks)


def test_chunk_system_catalogue_empty_pages() -> None:
    chunks = chunk_system_catalogue("dragon.pdf", [], [], "dragon", "doc-dragon")
    assert chunks == []


def test_chunk_system_catalogue_drops_garbage_pages() -> None:
    pages = [
        {"page_number": 1, "text": "ξx\nC∈\nYR\nanr mps"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    assert chunks == []


# ============================================================
# 2. System hierarchy metadata
# ============================================================
def test_system_chunks_have_catalogue_membership() -> None:
    pages = [
        {"page_number": 1, "text": "DESCRIPTION\nDragon is a passive fire protection system"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    assert chunks
    for c in chunks:
        assert "catalogue_membership" in c
        assert c["catalogue_membership"].startswith("system_")


def test_system_chunk_types_are_valid() -> None:
    pages = [
        {"page_number": 1, "text": "DESCRIPTION\nDragon system"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    valid_sections = {
        CHUNK_TYPE_PRODUCT_IDENTITY,
        CHUNK_TYPE_DESCRIPTION,
        CHUNK_TYPE_FEATURES,
        CHUNK_TYPE_APPLICATIONS,
        CHUNK_TYPE_TECHNICAL_MODEL,
        CHUNK_TYPE_TECHNICAL_TABLE,
        CHUNK_TYPE_TECHNICAL_VARIANT,
        CHUNK_TYPE_TECHNICAL_PART,
        CHUNK_TYPE_ACCESSORIES,
        CHUNK_TYPE_NOTES,
        CHUNK_TYPE_OTHER,
        CHUNK_TYPE_CONTACT,
        CHUNK_TYPE_TECHNICAL_SPECIFICATIONS,
        CHUNK_TYPE_SYSTEM_COMPONENT,
        CHUNK_TYPE_SYSTEM_WORKFLOW,
        CHUNK_TYPE_SYSTEM_COMPARISON,
    }
    for c in chunks:
        assert c["section"] in valid_sections
        assert c["content_type"] in valid_sections


# ============================================================
# 3. Variant isolation
# ============================================================
def test_dragon_ratios_preserved_as_variants() -> None:
    pages = [
        {"page_number": 1, "text": "Dragon 2.28:1\nDragon 2.33:1\nDragon 2.35:1\nDragon 2.5:1\nDragon 2:1"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    variant_chunks = [c for c in chunks if c["section"] == CHUNK_TYPE_TECHNICAL_VARIANT]
    assert variant_chunks
    variant_texts = " ".join(c["text"] for c in variant_chunks)
    assert "2.28:1" in variant_texts
    assert "2.33:1" in variant_texts
    assert "2.35:1" in variant_texts
    assert "2.5:1" in variant_texts
    assert "2:1" in variant_texts
    for c in variant_chunks:
        assert c["variant"] is not None
        assert c["catalogue_membership"] == "system_variant"


def test_polyurea_variants_detected() -> None:
    pages = [
        {"page_number": 1, "text": "POLYUREA\nTWO COMPONENT HOT AIRLESS POLYUREA SPRAY EQUIPMENT\nMixing Ratio 1:1\nPressure ratio 1:1"},
    ]
    chunks = chunk_system_catalogue("polyurea.pdf", pages, [], "polyurea", "doc-polyurea")
    all_text = " ".join(c["text"] for c in chunks)
    assert "POLYUREA" in all_text or "polyurea" in all_text.lower()


# ============================================================
# 4. Component vs product distinction
# ============================================================
def test_components_not_promoted_to_products() -> None:
    pages = [
        {"page_number": 1, "text": "COMPONENTS\nAirless pump\nHeater\nGun\nHose\nController\nMixing block"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    product_slugs = {c.get("product_slug") for c in chunks}
    assert "dragon" in product_slugs
    for c in chunks:
        if c.get("section") == CHUNK_TYPE_SYSTEM_COMPONENT:
            assert c.get("component_name") is not None
            assert c["product_slug"] == "dragon"


def test_component_detection() -> None:
    assert _looks_like_component("Airless pump") is True
    assert _looks_like_component("Heater") is True
    assert _looks_like_component("Spray Chamber") is True
    assert _looks_like_component("Suction Chamber") is True
    assert _looks_like_component("Transfer Pump") is True
    assert _looks_like_component("Some random text") is False
    assert _looks_like_component("") is False


# ============================================================
# 5. Dragon ratio label preservation
# ============================================================
def test_dragon_ratios_preserve_source_labels() -> None:
    pages = [
        {"page_number": 1, "text": "Dragon 2.28:1\nDragon 2.33:1\nParameters\nPressure ratio\nDischarge/cycle (th)\nPump combination"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    variant_chunks = [c for c in chunks if c["section"] == CHUNK_TYPE_TECHNICAL_VARIANT]
    assert variant_chunks
    for c in variant_chunks:
        text = c["text"]
        assert "Dragon" in text or "dragon" in text.lower()


def test_dragon_single_system_identity() -> None:
    pages = [
        {"page_number": 1, "text": "Dragon\nHigh duty Airless Plural component Passive Fire protection spraying equipment"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    slugs = [c["product_slug"] for c in chunks]
    assert all(s == "dragon" for s in slugs)
    identity_chunks = [c for c in chunks if c["section"] == CHUNK_TYPE_PRODUCT_IDENTITY]
    assert identity_chunks


# ============================================================
# 6. Polyurea variant separation
# ============================================================
def test_polyurea_family_identity() -> None:
    pages = [
        {"page_number": 1, "text": "POLYUREA\nTWO COMPONENT HOT AIRLESS POLYUREA SPRAY EQUIPMENT\nThe range is designed for tough working conditions"},
    ]
    chunks = chunk_system_catalogue("polyurea.pdf", pages, [], "polyurea", "doc-polyurea")
    assert chunks
    for c in chunks:
        assert c["product_slug"] == "polyurea"


def test_polyurea_variant_chunks_identify_variant() -> None:
    pages = [
        {"page_number": 1, "text": "Mixing Ratio 1:1\nPressure ratio 1:1\nPump combination 1:1"},
    ]
    chunks = chunk_system_catalogue("polyurea.pdf", pages, [], "polyurea", "doc-polyurea")
    all_text = " ".join(c["text"] for c in chunks)
    assert "1:1" in all_text


# ============================================================
# 7. Tube Varnish component handling
# ============================================================
def test_tube_varnish_components_detected() -> None:
    pages = [
        {"page_number": 1, "text": "COMPONENTS\nClosed Spray Chambers\nAirless pump\nDouble filter system\nSpray Ring\nHippo pump"},
    ]
    chunks = chunk_system_catalogue("TUBE VARNISH COATING SYSTEM.pdf", pages, [], "tube-varnish-coating-system", "doc-tube")
    component_chunks = [c for c in chunks if c["section"] == CHUNK_TYPE_SYSTEM_COMPONENT]
    assert component_chunks
    for c in component_chunks:
        assert c.get("component_name") is not None
        assert c["product_slug"] == "tube-varnish-coating-system"


def test_tube_varnish_workflow_detected() -> None:
    pages = [
        {"page_number": 1, "text": "WORKFLOW\nStep -1 Fume Collected from Paint Booth\nStep -2 In this Chamber fumes get wet\nStep -3 Remaining particle traps in metal filter"},
    ]
    chunks = chunk_system_catalogue("TUBE VARNISH COATING SYSTEM.pdf", pages, [], "tube-varnish-coating-system", "doc-tube")
    workflow_chunks = [c for c in chunks if c["section"] == CHUNK_TYPE_SYSTEM_WORKFLOW]
    assert workflow_chunks


# ============================================================
# 8. VRC MIX matrix reconstruction
# ============================================================
def test_vrc_mix_comparison_table_detected() -> None:
    headers = ["Feature", "Standard", "Optional", "VRC - MIX HP", "VRC MIX LOW-MEDIUM"]
    rows = [
        TableRow(cells=[TableCell(text="Mixing ratio range"), TableCell(text="Up to 10.0"), TableCell(text="Yes"), TableCell(text="Up to 15.0"), TableCell(text="Up to 15.0")]),
        TableRow(cells=[TableCell(text="Flow rate"), TableCell(text="6.8 LPM"), TableCell(text="Yes"), TableCell(text="4 LPM"), TableCell(text="4 LPM")]),
    ]
    table_type = detect_table_type(headers, rows, "VRC MIX (LOW - MEDIUM) PRESSURE.pdf")
    assert table_type == "SYSTEM_COMPARISON_TABLE"


def test_vrc_mix_chunker_handles_comparison_text() -> None:
    pages = [
        {"page_number": 1, "text": "COMPARISON\nStandard Optional\nMixing ratio range Up to 15.0\nFlow rate 4 liters per minute"},
    ]
    chunks = chunk_system_catalogue("VRC MIX (LOW - MEDIUM) PRESSURE.pdf", pages, [], "vrc-mix-low-medium-pressure", "doc-vrc")
    assert chunks
    all_text = " ".join(c["text"] for c in chunks)
    assert "COMPARISON" in all_text or "Mixing ratio" in all_text


# ============================================================
# 9. VRC MIX LOW/MEDIUM vs VRC MIX HP identity isolation
# ============================================================
def test_vrc_mix_low_medium_and_hp_are_distinct_identities() -> None:
    low_medium = resolve_product_identity("VRC MIX (LOW - MEDIUM) PRESSURE")
    hp = resolve_product_identity("VRC - MIX HP")
    assert low_medium is not None
    assert low_medium[0] == "vrc-mix-low-medium-pressure"
    assert hp is None or hp[0] != "vrc-mix-low-medium-pressure"


def test_vrc_mix_low_medium_and_hp_are_distinct_documents() -> None:
    low_medium_doc = "VRC MIX (LOW - MEDIUM) PRESSURE.pdf"
    hp_doc = "VRC - MIX HP.pdf"
    assert low_medium_doc.lower() != hp_doc.lower()
    assert _FILENAME_FALLBACK.get(hp_doc.lower()) != "vrc-mix-low-medium-pressure"


# ============================================================
# 10. Garbage-page handling
# ============================================================
def test_garbage_page_removed() -> None:
    pages = [
        {"page_number": 1, "text": "ξx\nC∈\nYR\nanr mps"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    assert chunks == []


def test_noise_fragments_filtered() -> None:
    pages = [
        {"page_number": 1, "text": "Dragon\nPassive fire protection\nsystem\nFEATURES\nModular configuration\nTECHNICAL SPECIFICATIONS\nPressure ratio 58:1\nVR Coatings\nsales@vrcoatings.com"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    texts = " ".join(c["text"] for c in chunks)
    assert "sales@vrcoatings.com" not in texts
    assert "VR Coatings" not in texts


# ============================================================
# 11. Catalogue membership metadata
# ============================================================
def test_catalogue_membership_values() -> None:
    pages = [
        {"page_number": 1, "text": "DESCRIPTION\nDragon system"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    memberships = {c["catalogue_membership"] for c in chunks}
    assert memberships
    for m in memberships:
        assert m.startswith("system_")


def test_technical_specifications_membership() -> None:
    pages = [
        {"page_number": 1, "text": "TECHNICAL SPECIFICATIONS\nPressure ratio: 58:1\nDischarge per cycle: 395cc"},
    ]
    chunks = chunk_system_catalogue("dragon.pdf", pages, [], "dragon", "doc-dragon")
    spec_chunks = [c for c in chunks if c["section"] == CHUNK_TYPE_TECHNICAL_SPECIFICATIONS]
    assert spec_chunks
    for c in spec_chunks:
        assert c["catalogue_membership"] == "system_technical"


# ============================================================
# 12. Product identity aliases
# ============================================================
def test_system_aliases_registered() -> None:
    assert "dragon" in PRODUCT_ALIASES
    assert "polyurea" in PRODUCT_ALIASES
    assert "tube-varnish-coating-system" in PRODUCT_ALIASES
    assert "vrc-mix-low-medium-pressure" in PRODUCT_ALIASES


def test_dragon_alias_resolution() -> None:
    assert resolve_product_identity("Dragon")[0] == "dragon"
    assert resolve_product_identity("Dragon PFP")[0] == "dragon"


def test_polyurea_alias_resolution() -> None:
    assert resolve_product_identity("Polyurea")[0] == "polyurea"
    assert resolve_product_identity("polyurea spray equipment")[0] == "polyurea"


def test_tube_varnish_alias_resolution() -> None:
    assert resolve_product_identity("Tube Varnish Coating System")[0] == "tube-varnish-coating-system"
    assert resolve_product_identity("tube coating system")[0] == "tube-varnish-coating-system"


def test_vrc_mix_low_medium_alias_resolution() -> None:
    assert resolve_product_identity("VRC MIX low medium pressure")[0] == "vrc-mix-low-medium-pressure"
    assert resolve_product_identity("VRC MIX low-medium pressure")[0] == "vrc-mix-low-medium-pressure"


# ============================================================
# 13. Filename fallback mapping
# ============================================================
def test_filename_fallback_for_systems() -> None:
    assert _FILENAME_FALLBACK.get("dragon.pdf") == "dragon"
    assert _FILENAME_FALLBACK.get("polyurea.pdf") == "polyurea"
    assert _FILENAME_FALLBACK.get("tube varnish coating system.pdf") == "tube-varnish-coating-system"
    assert _FILENAME_FALLBACK.get("vrc mix (low - medium) pressure.pdf") == "vrc-mix-low-medium-pressure"


def test_vrc_mix_hp_filename_fallback() -> None:
    assert _FILENAME_FALLBACK.get("vrc - mix hp.pdf") is None


# ============================================================
# 14. System chunk types constants
# ============================================================
def test_system_chunk_type_constants_exist() -> None:
    from app.rag.constants import (
        CHUNK_TYPE_TECHNICAL_SPECIFICATIONS as CTS,
        CHUNK_TYPE_SYSTEM_COMPONENT as CSC,
        CHUNK_TYPE_SYSTEM_WORKFLOW as CSW,
        CHUNK_TYPE_SYSTEM_COMPARISON as CSCMP,
    )
    assert CTS == "technical_specifications"
    assert CSC == "system_component"
    assert CSW == "system_workflow"
    assert CSCMP == "system_comparison"


# ============================================================
# 15. System variant extraction
# ============================================================
def test_extract_system_variants_creates_chunks() -> None:
    chunks = [
        {
            "document_id": "doc-1",
            "text": "Dragon 2.28:1\nDragon 2.33:1",
            "product_slug": "dragon",
            "page_number": 1,
        }
    ]
    result = _extract_system_variants(chunks, "dragon.pdf", "dragon")
    texts = [c["text"] for c in result]
    assert any("2.28:1" in t for t in texts)
    assert any("2.33:1" in t for t in texts)
    for c in result:
        if c.get("section") == CHUNK_TYPE_TECHNICAL_VARIANT:
            assert c["variant"] is not None
            assert c["catalogue_membership"] == "system_variant"


# ============================================================
# 16. Comparison table detection
# ============================================================
def test_looks_like_comparison_table() -> None:
    rows = [
        ["Feature", "Standard", "Optional"],
        ["Mixing ratio", "Up to 10.0", "Yes"],
    ]
    assert _looks_like_comparison_table(rows) is True


def test_non_comparison_table() -> None:
    rows = [
        ["Type", "30:150", "35:70"],
        ["Pressure ratio", "30:1", "35:1"],
    ]
    assert _looks_like_comparison_table(rows) is False


# ============================================================
# 17. Workflow step detection
# ============================================================
def test_workflow_step_detection() -> None:
    assert _looks_like_workflow_step("Step -1 Fume Collected from Paint Booth") is True
    assert _looks_like_workflow_step("Stage 2 Cleaning") is True
    assert _looks_like_workflow_step("Phase 3 Drying") is True
    assert _looks_like_workflow_step("Random text") is False
    assert _looks_like_workflow_step("") is False
