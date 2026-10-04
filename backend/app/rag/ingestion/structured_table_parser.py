"""
Reusable table-reconstruction layer for VR Coatings catalogues.

Table types:
- PUMP_MODEL_TABLE: Pump model/spec tables (CUB, Drum Press internal pumps)
- PART_NUMBER_TABLE: Part-number-based equipment tables (Pneumatic Stirrer)
- VALVE_SPEC_TABLE: Valve dimension/pressure/material tables (Ball Valves)
- SYSTEM_COMPONENT_TABLE: Component/system tables
- KEY_VALUE_TABLE: Simple key-value pairs
- UNKNOWN_TABLE: Cannot determine type

Design principles:
1. Reuse existing OCR blocks with coordinates
2. Use layout relationships, row/column structure
3. Preserve raw OCR values alongside normalized values
4. Do not invent data or guess unreadable values
5. Classify table type before parsing
6. Normalize OCR punctuation only when deterministic
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class CellValue:
    raw_value: str
    normalized_value: str
    normalization_reason: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class TableCell:
    text: str
    bbox: Optional[List[float]] = None
    confidence: Optional[float] = None
    x: float = 0.0
    y: float = 0.0


@dataclass
class TableRow:
    cells: List[TableCell]
    raw_cells: List[str] = field(default_factory=list)
    normalized_cells: List[str] = field(default_factory=list)
    confidence: str = "USABLE"
    issues: List[str] = field(default_factory=list)


@dataclass
class StructuredTable:
    headers: List[str]
    rows: List[TableRow]
    source_page: int
    table_type: str
    confidence: str = "USABLE"
    issues: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Table type detection
# ---------------------------------------------------------------------------

def detect_table_type(headers: List[str], first_rows: List[TableRow], document_name: str = "") -> str:
    """Classify table type based on headers and content."""
    header_text = " ".join(h.lower() for h in headers)
    doc_lower = document_name.lower()

    if "valve" in doc_lower or "ball" in doc_lower:
        if any(k in header_text for k in ["port size", "moc", "part code", "mwp", "connections", "material"]):
            return "VALVE_SPEC_TABLE"

    if any(k in header_text for k in ["part no", "part number", "fan dia", "shaft length", "container"]):
        if any(k in header_text for k in ["driven", "motor", "pneumatic", "fan dia", "shaft"]):
            return "PART_NUMBER_TABLE"

    if "type" in header_text and any(k in header_text for k in ["pressure ratio", "discharge", "stroke"]):
        return "PUMP_MODEL_TABLE"

    if "parameter" in header_text and "specification" in header_text:
        return "KEY_VALUE_TABLE"

    if any(k in header_text for k in ["model", "pressure ratio", "discharge per cycle", "stroke length"]):
        return "PUMP_MODEL_TABLE"

    ratio_model_headers = sum(1 for h in headers if re.search(r"\d+:\d+", h))
    if ratio_model_headers >= 1 and len(headers) >= 2:
        return "PUMP_MODEL_TABLE"

    for row in first_rows:
        row_text = " ".join(c.text for c in row.cells).lower()
        if re.search(r"\d+:\d+", row_text):
            if any(k in header_text for k in ["pressure ratio", "discharge", "stroke", "air"]):
                return "PUMP_MODEL_TABLE"

    return "UNKNOWN_TABLE"


# ---------------------------------------------------------------------------
# Coordinate-based table reconstruction from OCR blocks
# ---------------------------------------------------------------------------

def reconstruct_table_from_ocr_blocks(
    blocks: List[Any],
    page_number: int,
    document_name: str = "",
    x_threshold: float = 120.0,
    y_threshold: float = 25.0,
    y_gap_threshold: float = 200.0,
) -> List[StructuredTable]:
    """Reconstruct tables from OCR blocks using coordinate clustering.
    
    Splits blocks into separate y-clusters when large gaps (> y_gap_threshold)
    are detected, then reconstructs tables from each cluster independently.
    Returns only clusters that have actual structured table data.
    """
    if not blocks:
        return []

    valid_blocks = [b for b in blocks if b.bbox and len(b.bbox) >= 2]
    if not valid_blocks:
        return []

    block_data = []
    for b in valid_blocks:
        x = float(b.bbox[0])
        y = float(b.bbox[1])
        text = b.text.strip()
        if not text:
            continue
        block_data.append({
            "text": text,
            "x": x,
            "y": y,
            "confidence": b.confidence,
            "bbox": b.bbox,
        })

    if not block_data:
        return []

    # Split blocks into y-clusters by large gaps
    sorted_by_y = sorted(block_data, key=lambda b: b["y"])
    y_clusters = []
    current_cluster = [sorted_by_y[0]]
    
    for b in sorted_by_y[1:]:
        if b["y"] - current_cluster[-1]["y"] > y_gap_threshold:
            y_clusters.append(current_cluster)
            current_cluster = [b]
        else:
            current_cluster.append(b)
    y_clusters.append(current_cluster)
    
    tables = []
    for cluster in y_clusters:
        table = _reconstruct_single_table(cluster, page_number, document_name, x_threshold, y_threshold)
        if table:
            tables.append(table)
    
    return tables


def _reconstruct_single_table(
    block_data: List[Dict[str, Any]],
    page_number: int,
    document_name: str = "",
    x_threshold: float = 120.0,
    y_threshold: float = 25.0,
) -> Optional[StructuredTable]:
    """Reconstruct a single table from a cluster of OCR blocks."""
    x_centers = _cluster_coordinates([b["x"] for b in block_data], x_threshold)
    y_centers = _cluster_coordinates([b["y"] for b in block_data], y_threshold)

    if len(x_centers) < 2 or len(y_centers) < 2:
        return None

    grid: Dict[int, Dict[int, TableCell]] = {}
    for b in block_data:
        x_idx = _find_cluster(b["x"], x_centers, x_threshold)
        y_idx = _find_cluster(b["y"], y_centers, y_threshold)
        grid.setdefault(y_idx, {})[x_idx] = TableCell(
            text=b["text"],
            bbox=b.get("bbox"),
            confidence=b.get("confidence"),
            x=b["x"],
            y=b["y"],
        )

    sorted_y = sorted(grid.keys())
    sorted_x = sorted(set(idx for row in grid.values() for idx in row.keys()))

    if len(sorted_x) < 2 or len(sorted_y) < 2:
        return None

    headers = [grid[sorted_y[0]].get(x_idx, TableCell(text="")).text for x_idx in sorted_x]
    rows = []
    for y_idx in sorted_y[1:]:
        cells = [grid[y_idx].get(x_idx, TableCell(text="")) for x_idx in sorted_x]
        raw_cells = [c.text for c in cells]
        rows.append(TableRow(cells=cells, raw_cells=raw_cells))

    filtered_sorted_x, filtered_headers, filtered_rows = _filter_empty_columns(sorted_x, headers, rows)
    if len(filtered_sorted_x) < 2 or len(filtered_rows) < 1:
        return None

    # Try to find the best header row if first row looks like a section title
    if filtered_headers and not any(re.search(r"\d+:\d+", h) for h in filtered_headers):
        candidate = _select_best_table_candidate(filtered_headers, filtered_rows, page_number, document_name)
        if candidate and candidate.table_type != "UNKNOWN_TABLE":
            return candidate

    first_rows = filtered_rows[:3]
    table_type = detect_table_type(filtered_headers, first_rows, document_name)

    structured = StructuredTable(
        headers=filtered_headers,
        rows=filtered_rows,
        source_page=page_number,
        table_type=table_type,
    )

    is_valid, issues = validate_table(structured)
    if not is_valid:
        structured.confidence = "REVIEW_REQUIRED"
        structured.issues = issues

    return structured


def _select_best_table_candidate(
    headers: List[str],
    rows: List[TableRow],
    page_number: int,
    document_name: str = "",
) -> Optional[StructuredTable]:
    """Select the best table candidate from clustered OCR blocks."""
    if not rows:
        return None

    # First, look for a row that strongly resembles a header:
    # - First cell is a known header keyword ("Type", "Model", etc.)
    # - Subsequent cells contain ratio-like values (e.g., "28:550", "30:150")
    # This handles cases where section titles appear before the actual table header.
    header_keywords = ["type", "model", "part no", "part number", "port size", "size"]
    for i, row in enumerate(rows):
        first_cell = row.cells[0].text.strip().lower() if row.cells else ""
        if any(k in first_cell for k in header_keywords):
            # Check if subsequent cells have ratio-like or model-like values
            other_cells = [c.text for c in row.cells[1:]]
            other_text = " ".join(other_cells)
            if re.search(r"\d+:\d+", other_text) or len([c for c in other_cells if c.strip()]) >= 2:
                best_header_idx = i
                best_headers = [row.cells[j].text if j < len(row.cells) else "" for j in range(len(headers))]
                best_rows = []
                for k, r in enumerate(rows):
                    if k == best_header_idx:
                        continue
                    raw_cells = [c.text for c in r.cells]
                    best_rows.append(TableRow(cells=r.cells, raw_cells=raw_cells, confidence=r.confidence, issues=r.issues))
                if len(best_rows) < 1:
                    return None
                table_type = detect_table_type(best_headers, best_rows[:3], document_name)
                return StructuredTable(
                    headers=best_headers,
                    rows=best_rows,
                    source_page=page_number,
                    table_type=table_type,
                )

    # Fallback: score-based selection
    all_row_texts = []
    for row in rows:
        row_text = " ".join(c.text for c in row.cells)
        all_row_texts.append(row_text)

    header_candidates = []
    for i, row_text in enumerate(all_row_texts):
        score = 0
        if any(k in row_text.lower() for k in ["type", "model", "part no", "port size", "pressure ratio", "discharge", "stroke", "moc", "mwp"]):
            score += 2
        if any(k in row_text.lower() for k in ["fan dia", "shaft", "container", "connections", "material"]):
            score += 1
        numeric_count = len(re.findall(r"\d+", row_text))
        alpha_count = len(re.findall(r"[a-zA-Z]", row_text))
        if alpha_count > numeric_count:
            score += 1
        header_candidates.append((score, i))

    header_candidates.sort(key=lambda x: x[0], reverse=True)
    best_header_idx = header_candidates[0][1] if header_candidates else 0

    best_headers = [rows[best_header_idx].cells[i].text if i < len(rows[best_header_idx].cells) else "" for i in range(len(headers))]
    best_rows = []
    for i, row in enumerate(rows):
        if i == best_header_idx:
            continue
        raw_cells = [c.text for c in row.cells]
        best_rows.append(TableRow(cells=row.cells, raw_cells=raw_cells, confidence=row.confidence, issues=row.issues))

    if len(best_rows) < 1:
        return None

    table_type = detect_table_type(best_headers, best_rows[:3], document_name)

    return StructuredTable(
        headers=best_headers,
        rows=best_rows,
        source_page=page_number,
        table_type=table_type,
    )


def _filter_empty_columns(
    sorted_x: List[int],
    headers: List[str],
    rows: List[TableRow],
) -> Tuple[List[int], List[str], List[TableRow]]:
    """Remove columns that are mostly empty."""
    if not sorted_x or not rows:
        return sorted_x, headers, rows

    total_cells = len(rows)
    non_empty_cols = []
    for i, x_idx in enumerate(sorted_x):
        empty_count = 0
        for row in rows:
            cell_text = row.raw_cells[i] if i < len(row.raw_cells) else ""
            if not cell_text.strip():
                empty_count += 1
        if empty_count < total_cells * 0.7:
            non_empty_cols.append(i)

    if not non_empty_cols:
        return sorted_x, headers, rows

    new_sorted_x = [sorted_x[i] for i in non_empty_cols]
    new_headers = [headers[i] for i in non_empty_cols]
    new_rows = []
    for row in rows:
        new_cells = [row.cells[i] for i in non_empty_cols if i < len(row.cells)]
        new_raw_cells = [row.raw_cells[i] for i in non_empty_cols if i < len(row.raw_cells)]
        new_rows.append(TableRow(cells=new_cells, raw_cells=new_raw_cells, confidence=row.confidence, issues=row.issues))

    return new_sorted_x, new_headers, new_rows


def _cluster_coordinates(values: List[float], threshold: float) -> List[float]:
    centers: List[float] = []
    for v in values:
        _find_cluster(v, centers, threshold)
    return centers


def _find_cluster(value: float, centers: List[float], threshold: float) -> int:
    for i, c in enumerate(centers):
        if abs(value - c) < threshold:
            return i
    centers.append(value)
    return len(centers) - 1


# ---------------------------------------------------------------------------
# Pump table parser
# ---------------------------------------------------------------------------

_RATIO_PATTERN = re.compile(r"^(\d+)[.:](\d+)$")
_RATIO_COLUMN_HINTS = {
    "pressure ratio", "transfer ratio", "ratio", "pressure ratio",
    "discharge", "output", "stroke", "air consumption", "inlet air",
    "maximum output", "maximum inlet", "recommended spray",
}


def _is_ratio_column(header: str) -> bool:
    h = header.lower().strip()
    return any(hint in h for hint in _RATIO_COLUMN_HINTS) or "ratio" in h


def _normalize_ratio_token(token: str, is_ratio_col: bool, context_rows: List[str]) -> Tuple[str, Optional[str]]:
    """Normalize ratio tokens like 4.1 -> 4:1 only when appropriate."""
    token = token.strip()
    if not token:
        return token, None

    match = _RATIO_PATTERN.match(token)
    if not match:
        return token, None

    if not is_ratio_col:
        return token, None

    context_lower = " ".join(context_rows).lower()
    if "ratio" not in context_lower and ":" not in context_lower:
        return token, None

    normalized = f"{match.group(1)}:{match.group(2)}"
    return normalized, "pressure_ratio_column"


def parse_pump_table(table: StructuredTable) -> List[Dict[str, Any]]:
    """Parse pump model/spec table into model chunks."""
    if table.table_type != "PUMP_MODEL_TABLE":
        return []

    headers = table.headers
    if len(headers) < 2:
        return []

    model_indices = _find_model_columns(headers)
    if not model_indices:
        return []

    results = []
    for col_idx in model_indices:
        model = headers[col_idx]
        values = []
        complete = True
        ratio_col_indices = [i for i, h in enumerate(headers) if _is_ratio_column(h)]
        context_rows = [row.raw_cells[col_idx] for row in table.rows if col_idx < len(row.raw_cells)]

        for row in table.rows:
            raw_cells = row.raw_cells if row.raw_cells else [c.text for c in row.cells]
            if not raw_cells:
                complete = False
                break

            label = raw_cells[0] if raw_cells else ""
            if not label:
                continue

            raw_value = raw_cells[col_idx] if col_idx < len(raw_cells) else ""
            if not raw_value:
                continue

            is_ratio_col = col_idx in ratio_col_indices
            normalized_value, reason = _normalize_ratio_token(raw_value, is_ratio_col, context_rows)

            values.append({
                "label": label,
                "raw_value": raw_value,
                "value": normalized_value,
                "normalization_reason": reason,
                "confidence": row.confidence,
            })

        if complete and values:
            row_confidence = _derive_row_confidence(values, table)
            results.append({
                "model": model,
                "values": values,
                "confidence": row_confidence,
                "table_type": table.table_type,
                "source_page": table.source_page,
                "issues": table.issues,
            })

    return results


def _find_model_columns(headers: List[str]) -> List[int]:
    """Find columns that contain model identifiers.

    In pump tables, column 0 typically contains row labels (e.g. 'Type',
    'Pressure ratio') and columns 1+ contain model-specific values.
    Model identifiers appear in the first data row of those columns.
    """
    if not headers:
        return []

    if len(headers) >= 2:
        first_is_label = not re.search(r"\d+:\d+", headers[0])
        if first_is_label:
            return list(range(1, len(headers)))

    model_indices = []
    for i, h in enumerate(headers):
        if re.search(r"\d+:\d+", h) or (i > 0 and h.strip()):
            model_indices.append(i)
    return model_indices if model_indices else [1] if len(headers) > 1 else []


def _derive_row_confidence(values: List[Dict[str, Any]], table: StructuredTable) -> str:
    """Derive confidence for a parsed model row."""
    if table.confidence == "REVIEW_REQUIRED":
        return "REVIEW_REQUIRED"

    low_conf_count = 0
    for v in values:
        cell_conf = v.get("confidence")
        if isinstance(cell_conf, (int, float)) and cell_conf < 0.7:
            low_conf_count += 1

    if low_conf_count > len(values) * 0.3:
        return "REVIEW_REQUIRED"

    return "USABLE"


# ---------------------------------------------------------------------------
# Part number table parser
# ---------------------------------------------------------------------------

_PART_NUMBER_PATTERN = re.compile(r"^\d{2,3}\s+\d{3,6}(?:\s+\d{1,5})?(?:\s+\d+)?$")
_ALTERNATE_PART_PATTERN = re.compile(r"^\d{2,3}\s+\d{3}\s+\d{3,5}\s+\d+$")


def _is_part_number(text: str) -> bool:
    """Check if text looks like a VR Coatings part number."""
    t = text.strip()
    if not t:
        return False
    if _PART_NUMBER_PATTERN.match(t):
        return True
    if _ALTERNATE_PART_PATTERN.match(t):
        return True
    if re.match(r"^\d{2,3}\s+\d{3,6}(?:\s+\d+)?$", t):
        return True
    return False


def parse_part_number_table(table: StructuredTable) -> List[Dict[str, Any]]:
    """Parse part-number-based equipment table."""
    if table.table_type != "PART_NUMBER_TABLE":
        return []

    headers = table.headers
    if len(headers) < 2:
        return []

    part_col_idx = _find_part_number_column(headers, table.rows)
    if part_col_idx is None:
        return []

    results = []
    seen_parts = set()

    for row in table.rows:
        raw_cells = row.raw_cells if row.raw_cells else [c.text for c in row.cells]
        if part_col_idx >= len(raw_cells):
            continue

        part_number = raw_cells[part_col_idx].strip()
        if not part_number or not _is_part_number(part_number):
            continue

        if part_number in seen_parts:
            continue
        seen_parts.add(part_number)

        values = []
        for label_idx, header in enumerate(headers):
            if label_idx == part_col_idx:
                continue
            raw_value = raw_cells[label_idx] if label_idx < len(raw_cells) else ""
            values.append({
                "label": header,
                "raw_value": raw_value,
                "value": raw_value,
                "normalization_reason": None,
                "confidence": row.confidence,
            })

        row_confidence = "USABLE"
        if any(v.get("confidence") == "REVIEW_REQUIRED" for v in values):
            row_confidence = "REVIEW_REQUIRED"

        results.append({
            "part_number": part_number,
            "values": values,
            "confidence": row_confidence,
            "table_type": table.table_type,
            "source_page": table.source_page,
            "issues": table.issues,
        })

    return results


def _find_part_number_column(headers: List[str], rows: List[TableRow]) -> Optional[int]:
    """Find the column containing part numbers."""
    for i, h in enumerate(headers):
        h_lower = h.lower()
        if "part no" in h_lower or "part number" in h_lower:
            return i

    for row in rows[:3]:
        for i, cell in enumerate(row.cells):
            if _is_part_number(cell.text):
                return i

    return None


# ---------------------------------------------------------------------------
# Valve spec table parser
# ---------------------------------------------------------------------------

def parse_valve_table(table: StructuredTable) -> List[Dict[str, Any]]:
    """Parse valve dimension/pressure/material table."""
    if table.table_type != "VALVE_SPEC_TABLE":
        return []

    headers = table.headers
    if len(headers) < 3:
        return []

    results = []
    seen_keys = set()

    for row in table.rows:
        raw_cells = row.raw_cells if row.raw_cells else [c.text for c in row.cells]
        cells_text = raw_cells
        if len(cells_text) < 3:
            continue

        part_number = cells_text[0].strip() if cells_text else ""
        if not part_number:
            continue

        key = part_number
        if key in seen_keys:
            continue
        seen_keys.add(key)

        values = []
        for label_idx, header in enumerate(headers):
            if label_idx < len(cells_text):
                raw_value = cells_text[label_idx]
                values.append({
                    "label": header,
                    "raw_value": raw_value,
                    "value": raw_value,
                    "normalization_reason": None,
                    "confidence": row.confidence,
                })

        results.append({
            "part_number": part_number,
            "values": values,
            "confidence": row.confidence,
            "table_type": table.table_type,
            "source_page": table.source_page,
            "issues": table.issues,
        })

    return results


# ---------------------------------------------------------------------------
# Generic table parser dispatcher
# ---------------------------------------------------------------------------

def parse_structured_table(table: StructuredTable) -> List[Dict[str, Any]]:
    """Dispatch to appropriate parser based on table type."""
    if table.table_type == "PUMP_MODEL_TABLE":
        return parse_pump_table(table)
    elif table.table_type == "PART_NUMBER_TABLE":
        return parse_part_number_table(table)
    elif table.table_type == "VALVE_SPEC_TABLE":
        return parse_valve_table(table)
    return []


# ---------------------------------------------------------------------------
# Table validation
# ---------------------------------------------------------------------------

def validate_table(table: StructuredTable) -> Tuple[bool, List[str]]:
    """Validate reconstructed table."""
    issues = []

    if not table.headers:
        issues.append("empty_headers")

    if not table.rows:
        issues.append("empty_rows")

    expected_cols = len(table.headers)
    for i, row in enumerate(table.rows):
        actual_cols = len(row.cells)
        if actual_cols != expected_cols:
            issues.append(f"row_{i}_column_mismatch: expected {expected_cols}, got {actual_cols}")

    seen_rows = set()
    for i, row in enumerate(table.rows):
        row_key = tuple(c.text for c in row.cells)
        if row_key in seen_rows:
            issues.append(f"duplicate_row_{i}")
        seen_rows.add(row_key)

    is_valid = len(issues) == 0
    return is_valid, issues
