from typing import Any, Dict, List, Optional, Tuple

from .text_cleaner import normalize_text
from .pdf_parser import extract_pages
from .pdf_table_parser import extract_tables, parse_spec_table, extract_tables_from_ocr
from app.rag.constants import (
    CHUNK_TYPE_PRODUCT_IDENTITY,
    CHUNK_TYPE_DESCRIPTION,
    CHUNK_TYPE_FEATURES,
    CHUNK_TYPE_APPLICATIONS,
    CHUNK_TYPE_TECHNICAL_MODEL,
    CHUNK_TYPE_TECHNICAL_TABLE,
    CHUNK_TYPE_ACCESSORIES,
    CHUNK_TYPE_NOTES,
    CHUNK_TYPE_OTHER,
    CHUNK_TYPE_TECHNICAL_VARIANT,
    CHUNK_TYPE_CONTACT,
    CATALOGUE_AUTHORITY_PRIORITY,
    SOURCE_TYPE_CATALOGUE,
)
from app.rag.ingestion.ocr.base import OCRPageResult
import re


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_KNOWN_GARBAGE = {
    "ξx", "C∈", "C", "∈", "YR", "三", "anr", "mps",
    "anr mps", "Uui aint", "Polyhose", "gi ere", "PUUP",
    "VR ngs", "DOV00", "202k", "S0A", "00C0", "D照", "ntuw",
    "1:]", "Act ns.", "Ho est", "Éina nt", "Phcone", "GIERE",
    "Mabaraebtra", "Bhosgri", "Bhosari", "sales@vrcoatinas.cor",
    "Bhosari, Pune 4]1026", "Bhosgri, Pune 4]1026", "03/25", "427",
}

_FOOTER_PATTERNS = [
    r"^VR\s*Coatings\s*Pvt\.?Ltd\.?$",
    r"^VR\s*Coatings$",
    r"^VR\s*COATINGS\s*PVT\.?\s*LTD\.?$",
    r"^Registered\s*Office:?$",
    r"^J-I38\s*MIDC,?$",
    r"^Bhosari?,?\s*Pune$",
    r"^Bhosari?,?\s*Pune\s*\d{6}$",
    r"^\+91\s*[\d\s]+$",
    r"^sales@vrcoatings\.com$",
    r"^sales@vrcoatinas\.cor$",
    r"^sales@vrcoatings\.co$",
    r"^Mabaraebtra\s*INDIA$",
    r"^INDIA$",
    r"^C\s*∈$",
    r"^C∈$",
    r"^ξx$",
    r"^2$",
    r"^3$",
    r"^4$",
    r"^Kingfisher$",
    r"^Falcon$",
    r"^JANA$",
    r"^JANATICSA$",
    r"^ARCOATINGS$",
    r"^Polyhose$",
    r"^Uui\s*aint$",
    r"^anr\s*mps$",
    r"^YR$",
    r"^三$",
    r"^CE$",
]

_SECTION_HEADINGS = {
    "DESCRIPTION", "FEATURES", "APPLICATIONS", "TECHNICAL SPECIFICATIONS",
    "TECHNICAL DATA", "TECHNICAL MODEL", "TECHNICAL TABLE", "MODELS",
    "VARIANTS", "ACCESSORIES", "DIMENSIONS", "CONNECTIONS", "MATERIALS",
    "CONTACT", "FOOTER", "NOTES", "PRODUCT IDENTITY", "PRODUCT",
    "OVERVIEW", "SPECIFICATIONS", "SPECIFICATION", "DATA", "MODEL",
    "CATEGORY", "PORT SIZE",
}

_FILTER_VARIANT_HEADINGS = {
    "FILTERS",
    "HIGH PRESSURE FILTER",
    "LOW PRESSURE FILTER (STAINLESS STEEL)",
    "LOW PRESSURE FILTER (ALUMINIUM)",
    "CARTRIDGE TYPE INLINE FILTER",
    "BAG TYPE INLINE FILTER",
    "TIP FILTER ASSEMBLY",
    "FILTER CASSETTE L145",
}

_KV_TECHNICAL_LABELS = {
    "voltage", "flow rate", "power", "pressure", "motor type",
    "maximum flow rate", "max. operating pressure", "max operating pressure",
    "maximum pressure", "max pressure", "rated pressure",
    "current consumption", "max. current consumption", "acceptance capacity",
    "sound pressure level", "overall length", "overall height", "overall width",
    "power cord", "altitude", "vibration", "temperature", "max tip size",
    "number of guns", "model", "motor type", "volume flow", "max viscosity",
    "maximum sound", "pressure level", "max. temperature", "max flow rate",
    "rated flow", "flow rate", "discharge per cycle", "air consumption",
    "inlet air pressure", "output pressure", "wetted part", "weight",
    "transfer ratio", "pressure ratio", "stroke length", "recommended spray",
    "maximum inlet air pressure", "maximum output pressure", "maximum fluid temperature",
    "t rating", "fluid inlet", "fluid outlet", "air inlet",
    "maximum working pressure", "inlet, outlet, drain ports", "filter cassette size",
    "wetted parts", "bag size", "inlet, outlet", "disc tip filter",
    "mesh sizes", "construction material", "size", "total fill volume",
    "max. current consumption", "maximum sound pressure level",
    "max. operating pressure", "max viscosity", "max tip size",
    "volume flow at", "max. temperature of the coating material",
    "spray gun does not exceed", "correctly up to", "altitude above mean sea level",
    "recommended spray volume", "discharge per cycle",
    "capacity", "pot capacity", "power supply", "net weight", "net wt",
    "max. working pressure", "max working pressure", "net wt.",
    "watt", "kw", "litre", "liter", "ltr", "ltrs", "itrs",
    "working pressure", "gross weight",
}

_TECHNICAL_VALUE_PATTERNS = [
    # Pressure values
    r"^\d+[\s/~-]*bar$",
    r"^\d+[\s/~-]*:?\s*\d+[\s/~-]*bar$",
    r"^\d+[\s/~-]*PSI$",
    # Voltage values
    r"^\d+[\s/~-]*VAC$",
    r"^\d+[\s/~-]*VDC$",
    r"^\d+[\s/~-]*kV$",
    r"^\d+[\s/~-]*~[\s/~-]*\d+[\s/~-]*VAC$",
    r"^\d+[\s/~-]*~[\s/~-]*\d+[\s/~-]*V$",
    # Power / current
    r"^\d+[\s/~-]*kW$",
    r"^\d+[\s/~-]*HP$",
    r"^\d+[\s/~-]*A$",
    r"^\d+[\s/~-]*Hz$",
    # Dimensions / weight
    r"^\d+[\s/~-]*mm$",
    r"^\d+[\s/~-]*inch$",
    r"^\d+[\s/~-]*in$",
    r"^\d+[\s/~-]*kg$",
    r"^\d+[\s/~-]*kgs$",
    r"^\d+[\s/~-]*g$",
    # Flow rates
    r"^\d+[\s/~-]*L/min$",
    r"^\d+[\s/~-]*LPM$",
    r"^\d+[\s/~-]*ml/min$",
    # Motor / drive types
    r"^BLDC$",
    r"^DC$",
    r"^AC$",
    r"^Pneumatic$",
    # Port sizes
    r"^1/4\s*BSP$",
    r"^1/2\s*BSP$",
    r"^3/4\s*BSP$",
    r"^3/8\s*BSP$",
    r"^M\s*\d+x?\s*\d+$",
    # Ratio / range
    r"^\d+[\s/~-]*:?\s*\d+[\s/~-]*$",
    # Percentage
    r"^\d+[\s/~-]*%$",
    # Temperature
    r"^\d+[\s/~-]*°C$",
    r"^\d+[\s/~-]*°F$",
    # Degrees
    r"^\d+[\s/~-]*°$",
]

_COMPILED_TECHNICAL_VALUE = [re.compile(p, re.IGNORECASE) for p in _TECHNICAL_VALUE_PATTERNS]


# ---------------------------------------------------------------------------
# Short-fragment classification
# ---------------------------------------------------------------------------
def _classify_short_fragment(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return "EMPTY"
    if stripped in _KNOWN_GARBAGE:
        return "OCR_GARBAGE"
    for pat in _FOOTER_PATTERNS:
        if re.search(pat, stripped, re.IGNORECASE):
            return "FOOTER"
    if stripped.startswith("sales@"):
        return "EMAIL"
    if stripped.startswith("http"):
        return "ADDRESS"
    for pat in _COMPILED_TECHNICAL_VALUE:
        if pat.match(stripped):
            return "TECHNICAL_VALUE"
    if re.match(r"^\d+:\d+$", stripped):
        return "TECHNICAL_IDENTIFIER"
    if re.match(r"^\d+/\d+$", stripped):
        return "TECHNICAL_IDENTIFIER"
    if re.match(r"^[A-Za-z]+[-]?\d+$", stripped):
        return "TECHNICAL_IDENTIFIER"
    if re.match(r"^[A-Za-z]{1,4}\d+$", stripped):
        return "TECHNICAL_IDENTIFIER"
    if re.match(r"^TB-\d+", stripped):
        return "TECHNICAL_IDENTIFIER"
    if re.match(r"^[A-Z]{2,}-\d+", stripped):
        return "TECHNICAL_IDENTIFIER"
    if re.match(r"^304\s*Stainless", stripped, re.IGNORECASE):
        return "TECHNICAL_IDENTIFIER"
    if stripped.upper() in _SECTION_HEADINGS:
        return "SECTION_HEADING"
    if stripped in _FILTER_VARIANT_HEADINGS:
        return "PRODUCT_VARIANT"
    if re.match(r"^Page\s*\d+$", stripped, re.IGNORECASE):
        return "PAGE_NUMBER"
    if re.match(r"^\d+\s*/\s*\d+$", stripped):
        return "PAGE_NUMBER"
    return "UNKNOWN"


def _is_footer(text: str) -> bool:
    return _classify_short_fragment(text) == "FOOTER"


def _is_technical_identifier(text: str) -> bool:
    return _classify_short_fragment(text) == "TECHNICAL_IDENTIFIER"


def _is_section_heading(text: str) -> bool:
    return _classify_short_fragment(text) == "SECTION_HEADING"


def _is_product_variant(text: str) -> bool:
    return _classify_short_fragment(text) == "PRODUCT_VARIANT"


def _is_garbage(text: str) -> bool:
    return _classify_short_fragment(text) == "OCR_GARBAGE"


def _is_technical_value(text: str) -> bool:
    return _classify_short_fragment(text) == "TECHNICAL_VALUE"


def _looks_like_kv_label(text: str) -> bool:
    t = text.lower().strip().rstrip(":")
    if not t:
        return False
    if t in _KV_TECHNICAL_LABELS:
        return True
    import re
    t_no_paren = re.sub(r'\s*\([^)]*\)\s*$', '', t).strip()
    if t_no_paren in _KV_TECHNICAL_LABELS:
        return True
    first_colon = t.find(":")
    if first_colon != -1:
        left = t[:first_colon].strip()
        if left in _KV_TECHNICAL_LABELS:
            return True
        left_no_paren = re.sub(r'\s*\([^)]*\)\s*$', '', left).strip()
        if left_no_paren in _KV_TECHNICAL_LABELS:
            return True
    for l in _KV_TECHNICAL_LABELS:
        if t.endswith(" " + l):
            return True
        if t.endswith("(" + l + ")"):
            return True
        if t.endswith("(" + l + " "):
            return True
    return False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _chunk_type_for_heading(heading: str) -> str:
    h = heading.lower()
    if "variant" in h or "filter" in h:
        return CHUNK_TYPE_TECHNICAL_VARIANT
    if "model" in h or "specification" in h or "technical" in h:
        return CHUNK_TYPE_TECHNICAL_MODEL
    if "application" in h:
        return CHUNK_TYPE_APPLICATIONS
    if "feature" in h:
        return CHUNK_TYPE_FEATURES
    if "description" in h:
        return CHUNK_TYPE_DESCRIPTION
    if "accessor" in h:
        return CHUNK_TYPE_ACCESSORIES
    if "note" in h:
        return CHUNK_TYPE_NOTES
    if "contact" in h or "footer" in h:
        return CHUNK_TYPE_CONTACT
    if "identity" in h or "product" in h:
        return CHUNK_TYPE_PRODUCT_IDENTITY
    return CHUNK_TYPE_OTHER


def _dedupe_footer_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen: set = set()
    out: List[Dict[str, Any]] = []
    for chunk in chunks:
        key = chunk.get("text", "")
        if _is_footer(key):
            if key in seen:
                continue
            seen.add(key)
        out.append(chunk)
    return out


def _merge_adjacent_kv_blocks(blocks: List[str]) -> List[str]:
    merged: List[str] = []
    i = 0
    while i < len(blocks):
        cur = blocks[i]
        if i + 1 < len(blocks) and _looks_like_kv_label(cur):
            nxt = blocks[i + 1]
            nxt_cls = _classify_short_fragment(nxt)
            # If next block is also a KV label, keep them separate
            if _looks_like_kv_label(nxt):
                merged.append(cur)
                i += 1
                continue
            # Otherwise try to merge kv_label with next block if it's a value
            if nxt_cls not in ("SECTION_HEADING", "PRODUCT_VARIANT", "FOOTER", "EMAIL", "PAGE_NUMBER", "OCR_GARBAGE"):
                merged.append(f"{cur.rstrip(':')}: {nxt}")
                i += 2
                continue
        merged.append(cur)
        i += 1
    return merged


def _try_merge_kv_label_with_following(blocks: List[str]) -> List[str]:
    """Specifically handle the case where a line ending with ':' or a known KV
    label is followed by a TECHNICAL_VALUE or a short technical fragment."""
    merged: List[str] = []
    i = 0
    while i < len(blocks):
        cur = blocks[i]
        cur_cls = _classify_short_fragment(cur)
        if i + 1 < len(blocks):
            nxt = blocks[i + 1]
            nxt_cls = _classify_short_fragment(nxt)
            # Check if cur looks like a KV label (possibly ending with ':')
            is_kv = _looks_like_kv_label(cur) or cur.rstrip().endswith(":")
            if is_kv and nxt_cls in ("TECHNICAL_VALUE", "UNKNOWN", "TECHNICAL_IDENTIFIER"):
                merged.append(f"{cur.rstrip(':').strip()}: {nxt}")
                i += 2
                continue
        merged.append(cur)
        i += 1
    return merged


def _merge_short_with_context(blocks: List[str]) -> List[str]:
    merged: List[str] = []
    buffer: List[str] = []
    buf_len = 0

    def flush_buffer() -> None:
        nonlocal buffer, buf_len
        if buffer:
            merged.append("\n".join(buffer))
            buffer = []
            buf_len = 0

    for block in blocks:
        cls = _classify_short_fragment(block)
        if cls in ("TECHNICAL_IDENTIFIER", "UNKNOWN", "TECHNICAL_VALUE"):
            # If the previous buffered line is a KV label, try to merge this as label: value
            if buffer and _looks_like_kv_label(buffer[-1]):
                label_line = buffer.pop()
                label_len = len(label_line)
                if buffer:
                    buf_len -= label_len + 1
                else:
                    buf_len = 0
                merged_line = f"{label_line.rstrip(':').strip()}: {block}"
                buffer.append(merged_line)
                buf_len += len(merged_line) + 1
            elif buf_len + len(block) + 1 <= 400:
                buffer.append(block)
                buf_len += len(block) + 1
            else:
                flush_buffer()
                buffer.append(block)
                buf_len = len(block)
        elif cls == "SECTION_HEADING":
            flush_buffer()
            merged.append(block)
        elif cls in ("FOOTER", "EMAIL", "PAGE_NUMBER", "OCR_GARBAGE"):
            flush_buffer()
        else:
            if buf_len + len(block) + 1 <= 400:
                buffer.append(block)
                buf_len += len(block) + 1
            else:
                flush_buffer()
                buffer.append(block)
                buf_len = len(block)
    flush_buffer()
    return merged


def _page_is_mostly_garbage(lines: List[str]) -> bool:
    """Heuristic: if most non-empty lines are very short and look like diagram
    labels, page numbers, or OCR noise, treat the page as garbage."""
    if not lines:
        return True
    garbage_count = 0
    suspect_count = 0
    for line in lines:
        cls = _classify_short_fragment(line)
        if cls == "OCR_GARBAGE":
            garbage_count += 1
        elif cls in ("PAGE_NUMBER", "UNKNOWN") and len(line) < 10:
            suspect_count += 1
        elif cls == "FOOTER" and len(line.strip()) <= 3:
            suspect_count += 1
    total = len(lines)
    if total == 0:
        return True
    return (garbage_count + suspect_count) / total > 0.7


# ---------------------------------------------------------------------------
# Main chunker
# ---------------------------------------------------------------------------
def chunk_catalogue(
    document_name: str,
    pages: List[Dict[str, Any]],
    tables: List[Dict[str, Any]],
    product_slug: str,
    document_id: str,
    ocr_results: Optional[List[OCRPageResult]] = None,
) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    chunk_index = 0
    doc_name_lower = document_name.lower()

    is_filters = "filter" in doc_name_lower and "filters" in doc_name_lower

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
        # Drop pages that are mostly garbage/diagram labels
        if _page_is_mostly_garbage(kept):
            continue
        page_lines[page_number] = kept

    if not page_lines:
        return chunks

    # Group by section headings within each page
    raw_blocks: List[Dict[str, Any]] = []
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
            # Only treat lines as section headings if they match a known heading
            # or are a known filter variant. This avoids treating product names,
            # model IDs, diagram labels, and technical values as headings.
            is_known_heading = line.upper() in _SECTION_HEADINGS
            is_filter_variant = line in _FILTER_VARIANT_HEADINGS
            if is_known_heading and len(line) > 3 and not is_filter_variant:
                flush_block()
                current_heading = line.rstrip(":")
                current_lines = []
                continue
            if is_filter_variant:
                flush_block()
                current_heading = line
                current_lines = [line]
                flush_block()
                current_heading = line
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

    # For filters, split into filter variants while preserving all pages
    if is_filters:
        variant_blocks: List[Dict[str, Any]] = []
        last_variant = "FILTERS"
        for block in processed_blocks:
            lines = block["merged_lines"]
            current_variant = last_variant
            current_variant_lines: List[str] = []

            for line in lines:
                if line in _FILTER_VARIANT_HEADINGS:
                    if current_variant_lines:
                        variant_blocks.append({
                            "page_number": block["page_number"],
                            "heading": current_variant,
                            "merged_lines": list(current_variant_lines),
                        })
                    current_variant = line
                    current_variant_lines = [line]
                    last_variant = line
                else:
                    current_variant_lines.append(line)
            if current_variant_lines:
                variant_blocks.append({
                    "page_number": block["page_number"],
                    "heading": current_variant,
                    "merged_lines": list(current_variant_lines),
                })
        # Merge same-variant blocks across pages
        merged_variants: Dict[str, Dict[str, Any]] = {}
        for vb in variant_blocks:
            h = vb["heading"]
            if h not in merged_variants:
                merged_variants[h] = {
                    "page_number": vb["page_number"],
                    "heading": h,
                    "merged_lines": list(vb["merged_lines"]),
                }
            else:
                existing = merged_variants[h]
                existing["merged_lines"].extend(vb["merged_lines"])
        processed_blocks = list(merged_variants.values())

    # Build chunks
    seen_texts: set = set()
    for block in processed_blocks:
        page_number = block["page_number"]
        heading = block["heading"]
        merged_lines = block["merged_lines"]
        if not merged_lines:
            continue
        # Drop chunks that are only a heading/variant name with no real content
        meaningful = [l for l in merged_lines if len(l.strip()) > 3 and l.strip() not in _FILTER_VARIANT_HEADINGS]
        if not meaningful:
            continue
        chunk_text = "\n".join(merged_lines)
        if chunk_text in seen_texts:
            continue
        seen_texts.add(chunk_text)
        chunks.append({
            "document_id": document_id,
            "chunk_id": f"{document_id}::chunk::{chunk_index}",
            "source_type": SOURCE_TYPE_CATALOGUE,
            "source_authority": "primary",
            "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
            "document_name": document_name,
            "product": heading,
            "product_slug": product_slug,
            "section": _chunk_type_for_heading(heading),
            "content_type": _chunk_type_for_heading(heading),
            "page_number": page_number,
            "line_start": 1,
            "line_end": len(merged_lines),
            "text": chunk_text,
        })
        chunk_index += 1

    # Table chunks
    for table in tables:
        rows = table.get("rows", [])
        parsed = parse_spec_table(rows)
        if not parsed:
            continue
        for item in parsed:
            model = item["model"]
            lines = [f"{v['label']}: {v['value']}" for v in item["values"]]
            chunks.append({
                "document_id": document_id,
                "chunk_id": f"{document_id}::chunk::{chunk_index}",
                "source_type": SOURCE_TYPE_CATALOGUE,
                "source_authority": "primary",
                "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                "document_name": document_name,
                "product": product_slug.replace("-", " ").title(),
                "product_slug": product_slug,
                "section": CHUNK_TYPE_TECHNICAL_MODEL,
                "content_type": CHUNK_TYPE_TECHNICAL_MODEL,
                "model": model,
                "page_number": table["page_number"],
                "line_start": 1,
                "line_end": len(lines),
                "text": "\n".join(lines),
            })
            chunk_index += 1

    if ocr_results:
        ocr_tables = extract_tables_from_ocr(ocr_results)
        for table in ocr_tables:
            rows = table.get("rows", [])
            parsed = parse_spec_table(rows)
            if not parsed:
                continue
            for item in parsed:
                model = item["model"]
                lines = [f"{v['label']}: {v['value']}" for v in item["values"]]
                chunks.append({
                    "document_id": document_id,
                    "chunk_id": f"{document_id}::chunk::{chunk_index}",
                    "source_type": SOURCE_TYPE_CATALOGUE,
                    "source_authority": "primary",
                    "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                    "document_name": document_name,
                    "product": product_slug.replace("-", " ").title(),
                    "product_slug": product_slug,
                    "section": CHUNK_TYPE_TECHNICAL_MODEL,
                    "content_type": CHUNK_TYPE_TECHNICAL_MODEL,
                    "model": model,
                    "page_number": table["page_number"],
                    "line_start": 1,
                    "line_end": len(lines),
                    "text": "\n".join(lines),
                })
                chunk_index += 1

    # Post-processing
    chunks = _ensure_product_identity_chunk(chunks, document_name, product_slug, page_lines)
    chunks = _extract_turbine_variants(chunks, document_name)
    chunks = _split_mixed_technical_chunks(chunks, document_name)
    chunks = _drop_short_unknown_fragments(chunks)

    # Deduplicate footer chunks
    chunks = _dedupe_footer_chunks(chunks)

    _reclassify_description_chunks(chunks)

    return chunks


_DESCRIPTION_KEYWORDS = [
    "suitable for",
    "range is",
    "ideal for",
    "designed for",
    "used for",
    "application includes",
    "coating is",
    "paint is",
]


def _reclassify_description_chunks(chunks: List[Dict[str, Any]]) -> None:
    for chunk in chunks:
        current_section = chunk.get("section", "")
        if current_section not in (CHUNK_TYPE_OTHER, "General"):
            continue
        text_lower = chunk.get("text", "").lower()
        if any(keyword in text_lower for keyword in _DESCRIPTION_KEYWORDS):
            chunk["section"] = CHUNK_TYPE_DESCRIPTION
            chunk["content_type"] = CHUNK_TYPE_DESCRIPTION


_VARIANT_PATTERN = re.compile(r'\b(?:TB|TB-)[\s-]?\d+\b', re.IGNORECASE)


def _extract_turbine_variants(chunks: List[Dict[str, Any]], document_name: str) -> List[Dict[str, Any]]:
    """Extract TB-70/TB-110/TB-180 style variants as technical_variant chunks."""
    doc_lower = document_name.lower()
    if "turbine" not in doc_lower and "stirrer" not in doc_lower:
        return chunks
    variant_chunks: List[Dict[str, Any]] = []
    for chunk in chunks:
        text = chunk.get("text", "")
        lines = text.splitlines()
        for line in lines:
            m = _VARIANT_PATTERN.search(line)
            if not m:
                continue
            variant_id = m.group(0).upper().replace(" ", "-")
            desc = line[m.end():].strip()
            if desc.startswith("("):
                desc = desc[1:]
            if desc.endswith(")"):
                desc = desc[:-1]
            desc = desc.strip()
            if not desc:
                continue
            base_doc_id = chunk.get("document_id", f"doc-{document_name}")
            variant_chunks.append({
                "document_id": base_doc_id,
                "chunk_id": f"{base_doc_id}::chunk::variant::{variant_id}",
                "source_type": chunk.get("source_type", SOURCE_TYPE_CATALOGUE),
                "source_authority": "primary",
                "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                "document_name": document_name,
                "product": chunk.get("product", ""),
                "product_slug": chunk.get("product_slug", ""),
                "section": CHUNK_TYPE_TECHNICAL_VARIANT,
                "content_type": CHUNK_TYPE_TECHNICAL_VARIANT,
                "page_number": chunk.get("page_number"),
                "line_start": 1,
                "line_end": 1,
                "text": f"{variant_id}: {desc}",
            })
    if variant_chunks:
        existing_texts = {c.get("text", "") for c in chunks}
        for vc in variant_chunks:
            if vc["text"] not in existing_texts:
                chunks.append(vc)
    return chunks


def _ensure_product_identity_chunk(
    chunks: List[Dict[str, Any]],
    document_name: str,
    product_slug: str,
    page_lines: Dict[int, List[str]],
) -> List[Dict[str, Any]]:
    """Ensure short meaningful page-1 content gets a product_identity chunk."""
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
        })
    return chunks


def _split_mixed_technical_chunks(chunks: List[Dict[str, Any]], document_name: str) -> List[Dict[str, Any]]:
    """Split technical_model chunks that mix specs with accessories/components."""
    _ACCESSORY_HINTS = {
        "drum jacket heater", "electrical stirrer", "transfer pump",
        "hoisting unit", "stirrer", "pump", "heater", "jacket",
        "pot", "outlet tube", "gasket", "valve",
    }
    result: List[Dict[str, Any]] = []
    for chunk in chunks:
        if chunk.get("section") != CHUNK_TYPE_TECHNICAL_MODEL:
            result.append(chunk)
            continue
        text = chunk.get("text", "")
        lines = text.splitlines()
        spec_lines = []
        accessory_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            cls = _classify_short_fragment(stripped)
            if cls == "OCR_GARBAGE":
                continue
            if ":" in stripped or _is_technical_value(stripped) or _looks_like_kv_label(stripped):
                spec_lines.append(stripped)
            elif cls == "SECTION_HEADING" or len(stripped) <= 3:
                spec_lines.append(stripped)
            else:
                lower = stripped.lower()
                is_accessory = any(h in lower for h in _ACCESSORY_HINTS)
                if is_accessory:
                    accessory_lines.append(stripped)
                else:
                    spec_lines.append(stripped)
        if spec_lines:
            new_chunk = dict(chunk)
            new_chunk["text"] = "\n".join(spec_lines)
            new_chunk["line_end"] = len(spec_lines)
            result.append(new_chunk)
        if accessory_lines:
            new_chunk = dict(chunk)
            new_chunk["text"] = "\n".join(accessory_lines)
            new_chunk["section"] = CHUNK_TYPE_ACCESSORIES
            new_chunk["content_type"] = CHUNK_TYPE_ACCESSORIES
            new_chunk["line_end"] = len(accessory_lines)
            result.append(new_chunk)
    return result


def _drop_short_unknown_fragments(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove very short UNKNOWN fragments that aren't part of KV pairs."""
    cleaned: List[Dict[str, Any]] = []
    for chunk in chunks:
        lines = chunk.get("text", "").splitlines()
        kept = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            cls = _classify_short_fragment(stripped)
            if cls == "UNKNOWN" and len(stripped) < 4:
                continue
            kept.append(stripped)
        if not kept:
            continue
        new_chunk = dict(chunk)
        new_chunk["text"] = "\n".join(kept)
        new_chunk["line_end"] = len(kept)
        cleaned.append(new_chunk)
    return cleaned
