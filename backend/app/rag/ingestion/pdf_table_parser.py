import re
import fitz
from typing import List, Dict, Any, Optional


def extract_tables(file_path: str) -> List[Dict[str, Any]]:
    doc = fitz.open(file_path)
    tables = []
    for page_number, page in enumerate(doc, start=1):
        tabs = page.find_tables()
        for table in tabs:
            try:
                rows = table.extract()
            except Exception:
                continue
            if not rows:
                continue
            tables.append({"page_number": page_number, "rows": rows})
    doc.close()
    return tables


def is_likely_spec_table(rows: List[List[Optional[str]]]) -> bool:
    if len(rows) < 2:
        return False
    header_text = " ".join(str(cell or "") for cell in rows[0]).lower()
    return any(token in header_text for token in ["model", "pressure", "ratio", "output", "model"])


def model_columns_from_rows(rows: List[List[Optional[str]]]) -> List[str]:
    if not rows:
        return []
    return [str(cell or "").strip() for cell in rows[0]]


def parse_spec_table(rows: List[List[Optional[str]]]) -> List[Dict[str, Any]]:
    if not is_likely_spec_table(rows):
        return []
    models = model_columns_from_rows(rows)
    chunks = []
    for model in models:
        if not model:
            continue
        values = []
        for row in rows[1:]:
            if not row:
                continue
            label = str(row[0] or "").strip()
            if not label:
                continue
            col_idx = models.index(model) if model in models else None
            if col_idx is None or col_idx >= len(row):
                continue
            value = str(row[col_idx] or "").strip()
            if not value:
                continue
            values.append({"label": label, "value": value})
        if values:
            chunks.append({"model": model, "values": values})
    return chunks
