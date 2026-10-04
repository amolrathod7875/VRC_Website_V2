from typing import Any, Dict, List, Optional, Tuple

from .text_cleaner import normalize_text
from .pdf_parser import extract_pages
from .pdf_table_parser import extract_tables, parse_spec_table, extract_tables_from_ocr
from .new_chunker import (
    _classify_short_fragment,
    _is_footer,
    _is_section_heading,
    _is_garbage,
    _is_technical_value,
    _is_technical_identifier,
    _looks_like_kv_label,
    _chunk_type_for_heading,
    _merge_adjacent_kv_blocks,
    _try_merge_kv_label_with_following,
    _merge_short_with_context,
    _reclassify_description_chunks,
    _ensure_product_identity_chunk,
    _drop_short_unknown_fragments,
    _dedupe_footer_chunks,
    _page_is_mostly_garbage,
)
from .structured_table_parser import (
    StructuredTable,
    TableCell,
    TableRow,
    detect_table_type,
    parse_structured_table,
    validate_table,
    reconstruct_table_from_ocr_blocks,
)
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
    CATALOGUE_AUTHORITY_PRIORITY,
    SOURCE_TYPE_CATALOGUE,
)
from app.rag.ingestion.ocr.base import OCRPageResult
import re

# ---------------------------------------------------------------------------
# System-catalogue chunk types
# ---------------------------------------------------------------------------
CHUNK_TYPE_TECHNICAL_SPECIFICATIONS = "technical_specifications"
CHUNK_TYPE_SYSTEM_COMPONENT = "system_component"
CHUNK_TYPE_SYSTEM_WORKFLOW = "system_workflow"
CHUNK_TYPE_SYSTEM_COMPARISON = "system_comparison"

_SYSTEM_CHUNK_TYPES = {
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

# ---------------------------------------------------------------------------
# System identity and component detection
# ---------------------------------------------------------------------------
_SYSTEM_COMPONENT_HINTS = {
    "pump", "heater", "gun", "hose", "controller", "mixing block",
    "agitator", "chamber", "tank", "filter", "blower", "manifold",
    "spray ring", "nozzle", "drain valve", "auto valve", "in-line heater",
    "transfer pump", "hippo pump", "airless pump", "mixing block",
    "static mixer", "outlet manifold", "pressure transmitter",
    "suction chamber", "spray chamber", "water tank", "solvent tank",
    "coating material tank", "bag filter", "cassette filter",
    "centrifugal blower", "air ducts", "moisture separating baffle",
    "conveyor", "spraying ring",
}

_WORKFLOW_MARKERS = re.compile(
    r"^(step\s*[-–]?\s*\d+|stage\s*\d+|phase\s*\d+|\d+\.\s)",
    re.IGNORECASE,
)

_COMPARISON_MARKERS = {
    "comparison", "compare", "standard", "optional", "yes", "no",
    "features", "classification", "faults", "alarm", "system response",
}

_VARIANT_PATTERNS = [
    re.compile(r"^[A-Z][a-z]+?\s+\d+:\d+$"),  # Dragon 2.28:1
    re.compile(r"^\d+:\d+$"),  # 2.28:1
    re.compile(r"^[A-Z\s]+?\d+:\d+$"),  # POLYUREA variant patterns
]


def _looks_like_system_variant(line: str, product_slug: str = "") -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) < 3:
        return False
    if _is_footer(stripped) or _is_garbage(stripped) or _is_technical_value(stripped):
        return False
    if _is_section_heading(stripped):
        return False
    if _is_technical_identifier(stripped):
        return False
    lower = stripped.lower()
    for pat in _VARIANT_PATTERNS:
        if pat.match(stripped):
            return True
    if product_slug and product_slug.lower() in lower:
        remainder = lower.replace(product_slug.lower(), "").strip()
        if remainder and re.search(r"\d+:\d+", remainder):
            return True
    return False


def _looks_like_component(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) < 4:
        return False
    lower = stripped.lower()
    return any(hint in lower for hint in _SYSTEM_COMPONENT_HINTS)


def _looks_like_workflow_step(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) < 5:
        return False
    return bool(_WORKFLOW_MARKERS.match(stripped))


def _looks_like_comparison_table(rows: List[List[str]]) -> bool:
    if not rows:
        return False
    header = " ".join(str(c or "").lower() for c in rows[0])
    return any(m in header for m in _COMPARISON_MARKERS)


def _chunk_type_for_system_heading(heading: str, line: str = "") -> str:
    h = heading.lower()
    l = line.lower()
    if "variant" in h or any(pat.match(line.strip()) for pat in _VARIANT_PATTERNS):
        return CHUNK_TYPE_TECHNICAL_VARIANT
    if "workflow" in h or _looks_like_workflow_step(line):
        return CHUNK_TYPE_SYSTEM_WORKFLOW
    if "component" in h or "subsystem" in h or _looks_like_component(line):
        return CHUNK_TYPE_SYSTEM_COMPONENT
    if "comparison" in h or "compare" in h:
        return CHUNK_TYPE_SYSTEM_COMPARISON
    if "specification" in h or "technical data" in h or "technical spec" in h:
        return CHUNK_TYPE_TECHNICAL_SPECIFICATIONS
    if "model" in h or "specification" in h or "technical" in h:
        return CHUNK_TYPE_TECHNICAL_MODEL
    if "application" in h:
        return CHUNK_TYPE_APPLICATIONS
    if "feature" in h:
        return CHUNK_TYPE_FEATURES
    if "description" in h or "overview" in h:
        return CHUNK_TYPE_DESCRIPTION
    if "accessor" in h:
        return CHUNK_TYPE_ACCESSORIES
    if "note" in h:
        return CHUNK_TYPE_NOTES
    if "identity" in h or "product" in h:
        return CHUNK_TYPE_PRODUCT_IDENTITY
    return CHUNK_TYPE_OTHER


# ---------------------------------------------------------------------------
# Main system-catalogue chunker
# ---------------------------------------------------------------------------
def chunk_system_catalogue(
    document_name: str,
    pages: List[Dict[str, Any]],
    tables: List[Dict[str, Any]],
    product_slug: str,
    document_id: str,
    ocr_results: Optional[List[OCRPageResult]] = None,
    system_metadata: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    chunk_index = 0
    meta = system_metadata or {}
    doc_name_lower = document_name.lower()

    # Build classified lines per page
    page_lines: Dict[int, List[str]] = {}
    for page in pages:
        page_number = page["page_number"]
        text = normalize_text(page["text"])
        if not text:
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        kept: List[str] = []
        for line in lines:
            cls = _classify_short_fragment(line)
            if cls in ("FOOTER", "EMAIL", "PAGE_NUMBER", "OCR_GARBAGE"):
                continue
            kept.append(line)
        if not kept:
            continue
        if _page_is_mostly_garbage(kept):
            continue
        page_lines[page_number] = kept

    if not page_lines:
        return chunks

    # Group by section headings within each page
    raw_blocks: List[Dict[str, Any]] = []
    system_heading_patterns = {
        "DESCRIPTION", "FEATURES", "APPLICATIONS", "TECHNICAL SPECIFICATIONS",
        "TECHNICAL DATA", "TECHNICAL MODEL", "TECHNICAL TABLE", "MODELS",
        "VARIANTS", "ACCESSORIES", "DIMENSIONS", "CONNECTIONS", "MATERIALS",
        "CONTACT", "FOOTER", "NOTES", "PRODUCT IDENTITY", "PRODUCT",
        "OVERVIEW", "SPECIFICATIONS", "SPECIFICATION", "DATA", "MODEL",
        "CATEGORY", "PORT SIZE", "COMPARISON", "COMPARISON MATRIX",
        "WORKFLOW", "PROCESS", "STEPS", "COMPONENTS", "SUBSYSTEMS",
    }

    for page_number in sorted(page_lines.keys()):
        lines = page_lines[page_number]
        current_heading = "General"
        current_lines: List[str] = []

        def flush_block() -> None:
            if current_lines:
                raw_blocks.append({
                    "page_number": page_number,
                    "heading": current_heading,
                    "lines": list(current_lines),
                })

        for line in lines:
            is_known_heading = line.upper() in system_heading_patterns
            if is_known_heading and len(line) > 3:
                flush_block()
                current_heading = line.rstrip(":")
                current_lines = []
                continue
            current_lines.append(line)
        flush_block()

    # Merge short fragments and kv pairs
    processed_blocks: List[Dict[str, Any]] = []
    for block in raw_blocks:
        lines = block["lines"]
        merged = _merge_adjacent_kv_blocks(lines)
        merged = _try_merge_kv_label_with_following(merged)
        merged = _merge_short_with_context(merged)
        block["merged_lines"] = merged
        processed_blocks.append(block)

    # Build chunks
    seen_texts: set = set()
    for block in processed_blocks:
        page_number = block["page_number"]
        heading = block["heading"]
        merged_lines = block["merged_lines"]
        if not merged_lines:
            continue
        meaningful = [l for l in merged_lines if len(l.strip()) > 3]
        if not meaningful:
            continue
        chunk_text = "\n".join(merged_lines)
        if chunk_text in seen_texts:
            continue
        seen_texts.add(chunk_text)

        # Determine content type
        section = _chunk_type_for_system_heading(heading, merged_lines[0] if merged_lines else "")
        content_type = section

        # Detect variant-specific content
        variant = None
        component_name = None
        catalogue_membership = None

        if section == CHUNK_TYPE_TECHNICAL_VARIANT:
            variant = heading
            catalogue_membership = "system_variant"
        elif section == CHUNK_TYPE_SYSTEM_COMPONENT:
            component_name = heading
            catalogue_membership = "system_component"
        elif section == CHUNK_TYPE_SYSTEM_WORKFLOW:
            catalogue_membership = "system_workflow"
        elif section == CHUNK_TYPE_TECHNICAL_SPECIFICATIONS:
            catalogue_membership = "system_technical"
        elif heading.lower() in {"description", "overview", "general"}:
            catalogue_membership = "system_description"
        elif heading.lower() in {"features"}:
            catalogue_membership = "system_feature"
        elif heading.lower() in {"applications"}:
            catalogue_membership = "system_application"
        else:
            catalogue_membership = "system"

        chunk: Dict[str, Any] = {
            "document_id": document_id,
            "chunk_id": f"{document_id}::chunk::{chunk_index}",
            "source_type": SOURCE_TYPE_CATALOGUE,
            "source_authority": "primary",
            "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
            "document_name": document_name,
            "product": heading,
            "product_slug": product_slug,
            "section": section,
            "content_type": content_type,
            "page_number": page_number,
            "line_start": 1,
            "line_end": len(merged_lines),
            "text": chunk_text,
            "catalogue_membership": catalogue_membership,
        }
        if variant:
            chunk["variant"] = variant
        if component_name:
            chunk["component_name"] = component_name
        chunks.append(chunk)
        chunk_index += 1

    # Structured table reconstruction
    chunks, chunk_index = _add_system_structured_table_chunks(
        chunks, document_id, document_name, product_slug,
        tables, ocr_results, chunk_index, meta
    )

    # Post-processing
    chunks = _ensure_system_product_identity(chunks, document_name, product_slug, page_lines)
    chunks = _extract_system_variants(chunks, document_name, product_slug)
    chunks = _drop_short_unknown_fragments(chunks)
    chunks = _dedupe_footer_chunks(chunks)
    _reclassify_description_chunks(chunks)

    for c in chunks:
        if "catalogue_membership" not in c:
            c["catalogue_membership"] = "system"

    return chunks


def _ensure_system_product_identity(
    chunks: List[Dict[str, Any]],
    document_name: str,
    product_slug: str,
    page_lines: Dict[int, List[str]],
) -> List[Dict[str, Any]]:
    if 1 not in page_lines:
        return chunks
    has_identity = any(c.get("section") == CHUNK_TYPE_PRODUCT_IDENTITY for c in chunks)
    if has_identity:
        return chunks
    page1 = page_lines[1]
    identity_lines = []
    for line in page1:
        cls = _classify_short_fragment(line)
        if cls in ("FOOTER", "EMAIL", "PAGE_NUMBER", "OCR_GARBAGE", "TECHNICAL_VALUE", "TECHNICAL_IDENTIFIER"):
            continue
        stripped = line.strip()
        if len(stripped) > 1:
            identity_lines.append(stripped)
    if not identity_lines:
        return chunks
    if len(identity_lines) <= 8:
        identity_text = "\n".join(identity_lines)
        identity_words = set(identity_text.lower().split())
        for c in chunks:
            if c.get("page_number") != 1:
                continue
            existing_text = c.get("text", "")
            if not existing_text:
                continue
            existing_words = set(existing_text.lower().split())
            if not identity_words or not existing_words:
                continue
            overlap = len(identity_words & existing_words) / max(len(identity_words), len(existing_words))
            if overlap > 0.7:
                existing_section = c.get("section", "")
                if existing_section in {
                    CHUNK_TYPE_SYSTEM_COMPONENT,
                    CHUNK_TYPE_SYSTEM_WORKFLOW,
                    CHUNK_TYPE_SYSTEM_COMPARISON,
                    CHUNK_TYPE_TECHNICAL_SPECIFICATIONS,
                }:
                    continue
                c["section"] = CHUNK_TYPE_PRODUCT_IDENTITY
                c["content_type"] = CHUNK_TYPE_PRODUCT_IDENTITY
                return chunks
        existing_texts = {c.get("text", "") for c in chunks}
        if identity_text in existing_texts:
            return chunks
        base_doc_id = chunks[0]["document_id"] if chunks else f"doc-{product_slug}"
        chunks.insert(0, {
            "document_id": base_doc_id,
            "chunk_id": f"{base_doc_id}::chunk::identity",
            "source_type": SOURCE_TYPE_CATALOGUE,
            "source_authority": "primary",
            "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
            "document_name": document_name,
            "product": identity_lines[0] if identity_lines else product_slug,
            "product_slug": product_slug,
            "section": CHUNK_TYPE_PRODUCT_IDENTITY,
            "content_type": CHUNK_TYPE_PRODUCT_IDENTITY,
            "page_number": 1,
            "line_start": 1,
            "line_end": len(identity_lines),
            "text": identity_text,
            "catalogue_membership": "system_identity",
        })
    return chunks


# ---------------------------------------------------------------------------
# System-specific variant extraction
# ---------------------------------------------------------------------------
_SYSTEM_VARIANT_PATTERN = re.compile(
    r"^([A-Za-z][A-Za-z\s]+?)\s*(\d+:\d+|\d+\.\d+:\d+)$"
)


def _extract_system_variants(
    chunks: List[Dict[str, Any]],
    document_name: str,
    product_slug: str,
) -> List[Dict[str, Any]]:
    """Extract system-level variants (e.g., Dragon 2.28:1) as technical_variant chunks."""
    variant_chunks: List[Dict[str, Any]] = []
    for chunk in chunks:
        text = chunk.get("text", "")
        lines = text.splitlines()
        for line in lines:
            stripped = line.strip()
            m = _SYSTEM_VARIANT_PATTERN.match(stripped)
            if not m:
                continue
            variant_id = f"{m.group(1).strip()} {m.group(2)}"
            desc = stripped[m.end():].strip()
            if desc.startswith("("):
                desc = desc[1:]
            if desc.endswith(")"):
                desc = desc[:-1]
            desc = desc.strip()
            base_doc_id = chunk.get("document_id", f"doc-{document_name}")
            variant_chunks.append({
                "document_id": base_doc_id,
                "chunk_id": f"{base_doc_id}::chunk::variant::{variant_id.replace(' ', '-').replace(':', '-')}",
                "source_type": chunk.get("source_type", SOURCE_TYPE_CATALOGUE),
                "source_authority": "primary",
                "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                "document_name": document_name,
                "product": chunk.get("product", ""),
                "product_slug": product_slug,
                "section": CHUNK_TYPE_TECHNICAL_VARIANT,
                "content_type": CHUNK_TYPE_TECHNICAL_VARIANT,
                "page_number": chunk.get("page_number"),
                "line_start": 1,
                "line_end": 1,
                "text": f"{variant_id}: {desc}" if desc else variant_id,
                "catalogue_membership": "system_variant",
                "variant": variant_id,
            })
    if variant_chunks:
        existing_texts = {c.get("text", "") for c in chunks}
        for vc in variant_chunks:
            if vc["text"] not in existing_texts:
                chunks.append(vc)
    return chunks


# ---------------------------------------------------------------------------
# System structured table reconstruction
# ---------------------------------------------------------------------------
def _add_system_structured_table_chunks(
    chunks: List[Dict[str, Any]],
    document_id: str,
    document_name: str,
    product_slug: str,
    tables: List[Dict[str, Any]],
    ocr_results: Optional[List[OCRPageResult]],
    chunk_index_start: int,
    system_metadata: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], int]:
    chunk_index = chunk_index_start
    structured_tables: List[StructuredTable] = []

    for table in tables:
        page_number = table.get("page_number", 1)
        rows = table.get("rows", [])
        if not rows:
            continue
        headers = rows[0] if rows else []
        header_list = [str(h or "").strip() for h in headers]
        table_rows = []
        for row in rows[1:]:
            cells = [TableCell(text=str(c or "").strip(), confidence=None) for c in row]
            raw_cells = [c.text for c in cells]
            table_rows.append(TableRow(cells=cells, raw_cells=raw_cells))

        table_type = detect_table_type(header_list, table_rows[:3], document_name)
        structured = StructuredTable(
            headers=header_list,
            rows=table_rows,
            source_page=page_number,
            table_type=table_type,
        )
        is_valid, issues = validate_table(structured)
        if not is_valid:
            structured.confidence = "REVIEW_REQUIRED"
            structured.issues = issues
        structured_tables.append(structured)

    if ocr_results:
        for ocr_result in ocr_results:
            page_number = ocr_result.page_number
            structured_tables_list = reconstruct_table_from_ocr_blocks(
                ocr_result.blocks, page_number, document_name
            )
            for structured in structured_tables_list:
                is_valid, issues = validate_table(structured)
                if not is_valid:
                    structured.confidence = "REVIEW_REQUIRED"
                    structured.issues = issues
                structured_tables.append(structured)

    for table in structured_tables:
        parsed = parse_structured_table(table)
        for item in parsed:
            table_type = item.get("table_type", "UNKNOWN_TABLE")
            if table_type == "PUMP_MODEL_TABLE":
                section = CHUNK_TYPE_TECHNICAL_MODEL
                content_type = CHUNK_TYPE_TECHNICAL_MODEL
                identifier = item.get("model", "")
            elif table_type == "PART_NUMBER_TABLE":
                section = CHUNK_TYPE_TECHNICAL_PART
                content_type = CHUNK_TYPE_TECHNICAL_PART
                identifier = item.get("part_number", "")
            elif table_type == "VALVE_SPEC_TABLE":
                section = CHUNK_TYPE_TECHNICAL_PART
                content_type = CHUNK_TYPE_TECHNICAL_PART
                identifier = item.get("part_number", "")
            elif table_type == "SYSTEM_COMPARISON_TABLE":
                section = CHUNK_TYPE_SYSTEM_COMPARISON
                content_type = CHUNK_TYPE_SYSTEM_COMPARISON
                identifier = ""
            else:
                section = CHUNK_TYPE_TECHNICAL_TABLE
                content_type = CHUNK_TYPE_TECHNICAL_TABLE
                identifier = ""

            lines = []
            if identifier and table_type in ("PART_NUMBER_TABLE", "VALVE_SPEC_TABLE"):
                lines.append(f"Part Number: {identifier}")
            for v in item.get("values", []):
                label = v.get("label", "")
                value = v.get("value", "")
                raw_value = v.get("raw_value", "")
                norm_reason = v.get("normalization_reason")
                if norm_reason and raw_value != value:
                    lines.append(f"{label}: {value} (raw: {raw_value})")
                else:
                    lines.append(f"{label}: {value}")

            chunk_meta = {
                "document_id": document_id,
                "chunk_id": f"{document_id}::chunk::{chunk_index}",
                "source_type": SOURCE_TYPE_CATALOGUE,
                "source_authority": "primary",
                "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                "document_name": document_name,
                "product": product_slug.replace("-", " ").title(),
                "product_slug": product_slug,
                "section": section,
                "content_type": content_type,
                "page_number": item.get("source_page", table.source_page),
                "line_start": 1,
                "line_end": len(lines),
                "text": "\n".join(lines),
                "confidence": item.get("confidence", "USABLE"),
                "table_type": table_type,
                "issues": item.get("issues", []),
                "catalogue_membership": "system_technical",
            }

            if identifier:
                chunk_meta["model"] = identifier if table_type == "PUMP_MODEL_TABLE" else None
                chunk_meta["part_number"] = identifier if table_type in ("PART_NUMBER_TABLE", "VALVE_SPEC_TABLE") else None

            chunks.append(chunk_meta)
            chunk_index += 1

    return chunks, chunk_index
