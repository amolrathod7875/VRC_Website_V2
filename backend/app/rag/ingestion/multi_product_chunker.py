from __future__ import annotations

import re
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
    _split_mixed_technical_chunks,
    _drop_short_unknown_fragments,
    _dedupe_footer_chunks,
)
from app.rag.constants import (
    CHUNK_TYPE_PRODUCT_IDENTITY,
    CHUNK_TYPE_DESCRIPTION,
    CHUNK_TYPE_FEATURES,
    CHUNK_TYPE_APPLICATIONS,
    CHUNK_TYPE_TECHNICAL_MODEL,
    CHUNK_TYPE_TECHNICAL_TABLE,
    CHUNK_TYPE_TECHNICAL_VARIANT,
    CHUNK_TYPE_ACCESSORIES,
    CHUNK_TYPE_NOTES,
    CHUNK_TYPE_OTHER,
    CHUNK_TYPE_CONTACT,
    CATALOGUE_AUTHORITY_PRIORITY,
    SOURCE_TYPE_CATALOGUE,
)
from app.rag.ingestion.ocr.base import OCRPageResult

# ---------------------------------------------------------------------------
# Product heading detection
# ---------------------------------------------------------------------------

_MODEL_PAREN_PATTERN = re.compile(
    r"^(.*?)\s*\(([^)]+)\)\s*(.*)$",
    re.IGNORECASE,
)

_VARIANT_SUFFIX_PATTERN = re.compile(
    r"^(.*?)\s*[\(\-]?\s*(ALUMINIUM|STAINLESS\s+STEEL|SS|AL|GOLD|SILVER|BLUE|RED)\s*[\)]?\s*$",
    re.IGNORECASE,
)

_GUN_TYPE_WORDS = re.compile(
    r"\b(?:AUTOMATIC|AIRLESS|AIR\s+ASSISTED|AIR\s+ASSISTED\s+AIRLESS|MANUAL|CONVENTIONAL|SPRAY\s+PAINTING|SPRAY|DISPENSING|EXTRUSION|PAINT|PRESSURE\s+FEED|CARTRIDGE)\b",
    re.IGNORECASE,
)

_GUN_SUFFIX_WORDS = re.compile(
    r"\b(?:GUN|GUNS|SPRAY\s+GUN|DISPENSING\s+GUN|EXTRUSION\s+GUN|PAINT\s+GUN|AIRLESS\s+GUN|AUTOMATIC\s+GUN|MANUAL\s+GUN)\b",
    re.IGNORECASE,
)


def _looks_like_product_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) < 5:
        return False
    if _is_section_heading(stripped):
        return False
    if _is_footer(stripped):
        return False
    if _is_garbage(stripped):
        return False
    if _is_technical_value(stripped):
        return False
    if _is_technical_identifier(stripped):
        return False
    if stripped.startswith("sales@") or stripped.startswith("http"):
        return False
    if stripped.startswith("VR Coatings") or stripped.startswith("VR COATINGS"):
        return False
    if stripped.startswith("Registered Office"):
        return False
    if re.match(r"^\d+\s*/\s*\d+$", stripped):
        return False
    if re.match(r"^Page\s*\d+$", stripped, re.IGNORECASE):
        return False

    generic_gun_types = {
        "SPRAY PAINTING GUN", "SPRAY PAINTING GUNS",
        "AUTOMATIC SPRAY PAINTING GUN", "AUTOMATIC SPRAY PAINTING GUNS",
        "MANUAL SPRAY PAINTING GUNS",
        "AIRLESS MANUAL SPRAY GUN", "AIRLESS MANUAL SPRAY GUNS",
        "AUTOMATIC AIRLESS SPRAY GUN", "AUTOMATIC AIRLESS SPRAY GUNS",
        "AUTOMATIC DISPENSING GUN", "AUTOMATIC DISPENSING GUNS",
        "MANUAL SPRAY GUN", "MANUAL SPRAY GUNS",
        "CONVENTIONAL SPRAY PAINTING GUN",
        "WETTED PARTS VRIL", "WETTED PARTS",
        "CARTRIDGE DISPENSING GUN",
    }
    if stripped.upper() in generic_gun_types:
        return False

    if _GUN_SUFFIX_WORDS.search(stripped):
        return True
    if re.match(r"^[A-Z][A-Z\s\-]+$", stripped) and len(stripped) >= 8:
        if any(k in stripped.upper() for k in [
            "GUN", "SPRAY", "DISPENSING", "EXTRUSION",
            "VRIA", "VRIAD", "FLAMINGO", "HAWK", "FALCON",
            "EAGLE", "AM250", "VRIL", "VRID", "EXT", "WAX", "POLE",
            "HOTMELT", "KINGFISHER",
        ]):
            return True
    return False


def _normalize_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text


def _strip_gun_type_words(text: str) -> str:
    result = text
    result = _GUN_TYPE_WORDS.sub("", result)
    result = _GUN_SUFFIX_WORDS.sub("", result)
    result = re.sub(r"\s+", " ", result).strip()
    result = result.replace("ASSISETD", "ASSISTED")
    result = result.replace("ASSISED", "ASSISTED")
    return result


def _extract_model_and_variant(heading: str) -> Tuple[str, Optional[str]]:
    heading = heading.strip()
    variant = None
    working = heading

    vm = _VARIANT_SUFFIX_PATTERN.match(working)
    if vm:
        working = vm.group(1).strip()
        variant = vm.group(2).strip().lower()
        variant = re.sub(r"\s+", "-", variant)

    m = _MODEL_PAREN_PATTERN.match(working)
    if m:
        prefix = m.group(1).strip()
        paren = m.group(2).strip()
        suffix = m.group(3).strip()

        has_gun_type_prefix = bool(_GUN_SUFFIX_WORDS.search(prefix) or _GUN_TYPE_WORDS.search(prefix))
        if has_gun_type_prefix:
            model = paren
            if suffix:
                suffix_stripped = _strip_gun_type_words(suffix)
                if suffix_stripped and len(suffix_stripped) > 2:
                    model = suffix_stripped
            return model, variant
        if suffix:
            suffix_stripped = _strip_gun_type_words(suffix)
            if suffix_stripped and len(suffix_stripped) > 2:
                model = suffix_stripped
            else:
                model = prefix
            return model, variant
        model = _strip_gun_type_words(prefix)
        if not model or len(model) <= 2:
            model = paren
        return model, variant

    stripped = _strip_gun_type_words(working)
    if stripped and len(stripped) > 2:
        if len(stripped) >= 4:
            return stripped, variant
        if not re.search(r"[A-Za-z]{3,}", working):
            return stripped, variant
        if re.search(r"\bGUN\b", working) and len(stripped.split()) == 1 and len(stripped) <= 5:
            return working, variant
    return working, variant


def _product_slug_from_heading(heading: str) -> Tuple[str, Optional[str]]:
    model, variant = _extract_model_and_variant(heading)
    slug = _normalize_slug(model)
    return slug, variant


def _chunk_has_technical_data(chunk_text: str) -> bool:
    lines = chunk_text.splitlines()
    technical_lines = 0
    for line in lines:
        cls = _classify_short_fragment(line)
        if cls in ("TECHNICAL_VALUE", "TECHNICAL_IDENTIFIER"):
            technical_lines += 1
        elif _looks_like_kv_label(line):
            technical_lines += 1
    return technical_lines >= 2


# ---------------------------------------------------------------------------
# Main multi-product chunker
# ---------------------------------------------------------------------------

def chunk_multi_product_catalogue(
    document_name: str,
    pages: List[Dict[str, Any]],
    tables: List[Dict[str, Any]],
    document_id: str,
    ocr_results: Optional[List[OCRPageResult]] = None,
) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    chunk_index = 0
    seen_texts: set = set()

    page_ocr_map: Dict[int, List[Dict[str, Any]]] = {}
    if ocr_results:
        for ocr_result in ocr_results:
            page_ocr_map[ocr_result.page_number] = [
                {
                    "text": b.text,
                    "x": float(b.bbox[0]) if b.bbox and len(b.bbox) > 0 else 0.0,
                    "y": float(b.bbox[1]) if b.bbox and len(b.bbox) > 1 else 0.0,
                    "confidence": b.confidence or 0.0,
                }
                for b in ocr_result.blocks
                if b.text and b.text.strip()
            ]

    for page in pages:
        page_number = page["page_number"]
        text = normalize_text(page["text"])
        if not text:
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            continue

        page_blocks = page_ocr_map.get(page_number, [])
        line_info: Dict[str, Dict[str, Any]] = {}
        if page_blocks:
            page_text = " ".join(b["text"] for b in page_blocks)
            for block in page_blocks:
                if block["text"] in page_text:
                    line_info[block["text"]] = {
                        "y": block["y"],
                        "x": block["x"],
                    }

        def _sort_key(line: str) -> Tuple[float, float]:
            info = line_info.get(line, {"y": 99999.0, "x": 99999.0})
            return (info["y"], info["x"])

        sorted_lines = sorted(lines, key=_sort_key)
        seen_lines = set()
        ordered_lines = []
        for line in sorted_lines:
            if line not in seen_lines:
                ordered_lines.append(line)
                seen_lines.add(line)

        heading_blocks: List[Tuple[str, float, float]] = []
        content_blocks: List[Tuple[str, float, float]] = []
        for line in ordered_lines:
            if line not in line_info:
                continue
            info = line_info[line]
            y = info["y"]
            x = info["x"]
            if _looks_like_product_heading(line):
                heading_blocks.append((line, y, x))
            elif re.match(r"^\([A-Z][A-Z\s\-]+\)$", line) and len(line) <= 30:
                paren_model = line.strip("()")
                heading_blocks.append((line, y, x))
            else:
                content_blocks.append((line, y, x))

        heading_blocks.sort(key=lambda t: (t[1], t[2]))

        sections: List[Tuple[str, List[str]]] = []
        for content_line, content_y, content_x in content_blocks:
            best_heading = None
            best_dist = None
            for heading_line, heading_y, heading_x in heading_blocks:
                if heading_y >= content_y:
                    continue
                y_dist = content_y - heading_y
                x_dist = abs(content_x - heading_x)
                if x_dist > 800:
                    continue
                dist = y_dist + x_dist * 0.01
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_heading = heading_line
            if best_heading is None:
                continue
            found = False
            for heading, section_lines in sections:
                if heading == best_heading:
                    section_lines.append(content_line)
                    found = True
                    break
            if not found:
                sections.append((best_heading, [content_line]))

        if not sections:
            continue

        for heading, section_lines in sections:
            product_slug, variant = _product_slug_from_heading(heading)
            if not product_slug:
                continue

            merged = _merge_adjacent_kv_blocks(section_lines)
            merged = _try_merge_kv_label_with_following(merged)
            merged = _merge_short_with_context(merged)

            meaningful = [
                l for l in merged
                if len(l.strip()) > 3 and not _is_section_heading(l)
            ]
            if not meaningful:
                continue

            chunk_text = "\n".join(meaningful)
            if chunk_text in seen_texts:
                continue
            seen_texts.add(chunk_text)

            if _chunk_has_technical_data(chunk_text):
                section = CHUNK_TYPE_TECHNICAL_MODEL
                content_type = CHUNK_TYPE_TECHNICAL_MODEL
            else:
                section = CHUNK_TYPE_PRODUCT_IDENTITY
                content_type = CHUNK_TYPE_PRODUCT_IDENTITY

            chunks.append({
                "document_id": document_id,
                "chunk_id": f"{document_id}::chunk::{chunk_index}",
                "source_type": SOURCE_TYPE_CATALOGUE,
                "source_authority": "primary",
                "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                "document_name": document_name,
                "product": heading,
                "product_slug": product_slug,
                "parent_product_slug": None,
                "variant": variant,
                "section": section,
                "content_type": content_type,
                "page_number": page_number,
                "line_start": 1,
                "line_end": len(meaningful),
                "text": chunk_text,
            })
            chunk_index += 1

    for table in tables:
        rows = table.get("rows", [])
        parsed = parse_spec_table(rows)
        if not parsed:
            continue
        for item in parsed:
            model = item["model"]
            lines = [f"{v['label']}: {v['value']}" for v in item["values"]]
            product_slug, variant = _product_slug_from_heading(model)
            chunk_text = "\n".join(lines)
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
                "product": model,
                "product_slug": product_slug or document_name.lower().replace(" ", "_").replace(".pdf", ""),
                "parent_product_slug": None,
                "variant": variant,
                "section": CHUNK_TYPE_TECHNICAL_MODEL,
                "content_type": CHUNK_TYPE_TECHNICAL_MODEL,
                "page_number": table["page_number"],
                "line_start": 1,
                "line_end": len(lines),
                "text": chunk_text,
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
                product_slug, variant = _product_slug_from_heading(model)
                chunk_text = "\n".join(lines)
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
                    "product": model,
                    "product_slug": product_slug or document_name.lower().replace(" ", "_").replace(".pdf", ""),
                    "parent_product_slug": None,
                    "variant": variant,
                    "section": CHUNK_TYPE_TECHNICAL_MODEL,
                    "content_type": CHUNK_TYPE_TECHNICAL_MODEL,
                    "page_number": table["page_number"],
                    "line_start": 1,
                    "line_end": len(lines),
                    "text": chunk_text,
                })
                chunk_index += 1

    _reclassify_description_chunks(chunks)
    return chunks


def chunk_catalogue(
    document_name: str,
    pages: List[Dict[str, Any]],
    tables: List[Dict[str, Any]],
    product_slug: str,
    document_id: str,
    ocr_results: Optional[List[OCRPageResult]] = None,
) -> List[Dict[str, Any]]:
    doc_lower = document_name.lower()
    is_multi_product = any(name in doc_lower for name in [
        "automatic_gun",
        "conventional guns",
        "manual_guns",
    ])

    if is_multi_product:
        return chunk_multi_product_catalogue(document_name, pages, tables, document_id, ocr_results)

    return _chunk_catalogue_single(document_name, pages, tables, product_slug, document_id, ocr_results)
