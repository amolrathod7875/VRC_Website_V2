"""Source-anchored OCR corrections applied during catalogue ingestion.

Corrections are keyed by source document name and consist of exact,
verified replacements. They are applied to extracted page text and table
cells before chunking so that future ingestion regenerates the corrected
text and vectors instead of restoring the original OCR error.
"""

from typing import Any, Dict, List, Tuple


# (document_name) -> list of (incorrect, corrected) exact replacements.
OCR_TEXT_REPLACEMENTS: Dict[str, List[Tuple[str, str]]] = {
    "Elephant.pdf": [("3:]", "3:1")],
}


def apply_ocr_corrections(
    document_name: str,
    pages: List[Dict[str, Any]],
    tables: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    replacements = OCR_TEXT_REPLACEMENTS.get(document_name, [])
    if not replacements:
        return pages, tables

    for page in pages or []:
        text = page.get("text") or ""
        for incorrect, corrected in replacements:
            text = text.replace(incorrect, corrected)
        page["text"] = text

    for table in tables or []:
        rows = table.get("rows")
        if not rows:
            continue
        new_rows = []
        for row in rows:
            new_row = []
            for cell in row:
                if isinstance(cell, str):
                    for incorrect, corrected in replacements:
                        cell = cell.replace(incorrect, corrected)
                new_row.append(cell)
            new_rows.append(new_row)
        table["rows"] = new_rows

    return pages, tables
