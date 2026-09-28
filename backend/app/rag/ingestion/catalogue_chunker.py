from typing import Any, Dict, List

from .text_cleaner import normalize_text
from .pdf_parser import extract_pages
from .pdf_table_parser import extract_tables, parse_spec_table
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
    CATALOGUE_AUTHORITY_PRIORITY,
    SOURCE_TYPE_CATALOGUE,
)


def _chunk_type_for_heading(heading: str) -> str:
    h = heading.lower()
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
    if "identity" in h or "product" in h:
        return CHUNK_TYPE_PRODUCT_IDENTITY
    return CHUNK_TYPE_OTHER


def chunk_catalogue(
    document_name: str,
    pages: List[Dict[str, Any]],
    tables: List[Dict[str, Any]],
    product_slug: str,
    document_id: str,
) -> List[Dict[str, Any]]:
    chunks = []
    chunk_index = 0

    for page in pages:
        page_number = page["page_number"]
        text = normalize_text(page["text"])
        if not text:
            continue
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            continue

        current_heading = "General"
        current_block: List[str] = []

        def flush_block() -> None:
            nonlocal chunk_index, current_heading, current_block
            if not current_block:
                return
            chunk_text = "\n".join(current_block)
            chunks.append({
                "document_id": document_id,
                "chunk_id": f"{document_id}::chunk::{chunk_index}",
                "source_type": SOURCE_TYPE_CATALOGUE,
                "source_authority": "primary",
                "authority_priority": CATALOGUE_AUTHORITY_PRIORITY,
                "document_name": document_name,
                "product": current_heading,
                "product_slug": product_slug,
                "section": _chunk_type_for_heading(current_heading),
                "content_type": _chunk_type_for_heading(current_heading),
                "page_number": page_number,
                "line_start": 1,
                "line_end": len(current_block),
                "text": chunk_text,
            })
            chunk_index += 1
            current_block = []

        for line in lines:
            if line.endswith(":") or line.isupper():
                flush_block()
                current_heading = line.rstrip(":")
                continue
            current_block.append(line)
        flush_block()

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

    return chunks
