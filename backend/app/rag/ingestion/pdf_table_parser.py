import re
import fitz
from typing import List, Dict, Any, Optional

from app.rag.ingestion.ocr.base import OCRPageResult


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


def extract_tables_from_ocr(ocr_results: List[OCRPageResult]) -> List[Dict[str, Any]]:
    tables: List[Dict[str, Any]] = []
    for result in ocr_results:
        page_tables = _parse_ocr_page_table(result)
        for table in page_tables:
            table["page_number"] = result.page_number
            tables.append(table)
    return tables


def _parse_ocr_page_table(result: OCRPageResult) -> List[Dict[str, Any]]:
    text = result.full_text or ""
    if "TECHNICAL SPECIFICATIONS" not in text:
        return []

    labels: List[Dict[str, Any]] = []
    values: List[Dict[str, Any]] = []
    for block in result.blocks:
        if not block.bbox or len(block.bbox) < 2:
            continue
        x = block.bbox[0]
        y = block.bbox[1]
        if x < 400:
            labels.append({"text": block.text, "y": y, "confidence": block.confidence})
        elif 1200 <= y <= 1900:
            values.append({"text": block.text, "x": x, "y": y, "confidence": block.confidence})

    centers: List[float] = []
    columns: Dict[int, List[Dict[str, Any]]] = {}
    for v in values:
        col_idx = _cluster_x(v["x"], centers, threshold=100)
        columns.setdefault(col_idx, []).append(v)

    if not columns:
        return []

    sorted_cols = sorted(columns.items(), key=lambda x: centers[x[0]])
    if len(sorted_cols) < 2:
        return []

    model_names = []
    for _, col in sorted_cols:
        top = sorted(col, key=lambda b: b["y"])[0]
        model_names.append(top["text"])

    row_centers: List[float] = []
    rows: List[Dict[str, Any]] = []
    for col_idx, col in sorted_cols:
        for v in sorted(col, key=lambda b: b["y"]):
            row_idx = _cluster_y(v["y"], row_centers, threshold=30)
            rows.append({"row": row_idx, "col": col_idx, "text": v["text"], "y": v["y"], "confidence": v["confidence"]})
    rows.sort(key=lambda r: (r["row"], r["col"]))

    grid: Dict[int, Dict[int, str]] = {}
    for r in rows:
        grid.setdefault(r["row"], {})[r["col"]] = r["text"]

    label_map = {l["y"]: l["text"] for l in labels}
    row_labels: Dict[int, str] = {}
    for row_idx in sorted(grid.keys()):
        y_val = next(r["y"] for r in rows if r["row"] == row_idx)
        nearest_label = min(label_map.keys(), key=lambda ly: abs(ly - y_val))
        row_labels[row_idx] = label_map[nearest_label]

    num_models = len(grid.get(0, {}))
    if num_models < 2:
        return []

    parsed = []
    for col_idx, model in enumerate(model_names):
        if not model:
            continue
        values = []
        complete = True
        for row_idx in sorted(grid.keys()):
            if row_idx == 0:
                continue
            value = grid[row_idx].get(col_idx, "")
            if not value:
                complete = False
                break
            label = row_labels.get(row_idx, f"Row {row_idx}")
            values.append({"label": label, "value": value})
        if complete and values:
            parsed.append({"model": model, "values": values})

    if parsed:
        row_label_map: Dict[int, str] = {}
        for l in labels:
            ry = l["y"]
            matched_row = None
            min_dist = float("inf")
            for ri in sorted(grid.keys()):
                row_y = next((r["y"] for r in rows if r["row"] == ri), None)
                if row_y is not None and abs(row_y - ry) < min_dist:
                    min_dist = abs(row_y - ry)
                    matched_row = ri
            if matched_row is not None and min_dist < 40:
                row_label_map[matched_row] = l["text"]

        raw_rows = []
        for row_idx in sorted(grid.keys()):
            label = row_labels.get(row_idx, row_label_map.get(row_idx, f"Row {row_idx}"))
            raw_rows.append([label] + [grid[row_idx].get(col, "") for col in sorted(grid[row_idx].keys())])
        return [{"page_number": result.page_number, "rows": raw_rows}]
    return []


def _cluster_x(x: float, centers: List[float], threshold: float = 100) -> int:
    for i, c in enumerate(centers):
        if abs(x - c) < threshold:
            return i
    centers.append(x)
    return len(centers) - 1


def _cluster_y(y: float, centers: List[float], threshold: float = 30) -> int:
    for i, c in enumerate(centers):
        if abs(y - c) < threshold:
            return i
    centers.append(y)
    return len(centers) - 1


def is_likely_spec_table(rows: List[List[Optional[str]]]) -> bool:
    if len(rows) < 2:
        return False
    header_text = " ".join(str(cell or "") for cell in rows[0]).lower()
    if any(token in header_text for token in ["model", "pressure", "ratio", "output", "type", "specification", "spec"]):
        return True
    import re
    if any(re.search(r"\d+:\d+", str(cell or "")) for cell in rows[0]):
        return True
    return False


def model_columns_from_rows(rows: List[List[Optional[str]]]) -> List[str]:
    if not rows:
        return []
    header = rows[0]
    if len(header) < 2:
        return []
    import re
    if all(re.search(r"\d+:\d+", str(cell or "")) for cell in header):
        return [str(cell or "").strip() for cell in header]
    return [str(cell or "").strip() for cell in header[1:]]


def parse_spec_table(rows: List[List[Optional[str]]]) -> List[Dict[str, Any]]:
    if not is_likely_spec_table(rows) or len(rows) < 2:
        return []
    header = rows[0]
    models = [m for m in model_columns_from_rows(rows) if m]
    if not models:
        return []
    expected_data_cols = len(header) - 1
    for row in rows[1:]:
        if len(row) - 1 < expected_data_cols:
            return []
    chunks = []
    for model in models:
        values = []
        complete = True
        for row in rows[1:]:
            if not row or len(row) < 2:
                complete = False
                break
            label = str(row[0] or "").strip()
            if not label:
                complete = False
                break
            try:
                col_idx = header.index(model)
            except ValueError:
                complete = False
                break
            if col_idx >= len(row):
                complete = False
                break
            value = str(row[col_idx] or "").strip()
            if not value:
                complete = False
                break
            values.append({"label": label, "value": value})
        if complete and values:
            chunks.append({"model": model, "values": values})
    return chunks
