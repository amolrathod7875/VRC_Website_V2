import re
from typing import Any, Dict, List, Optional


def normalize_status_token(token: str) -> Optional[str]:
    t = token.strip()
    mapping = {
        "VR VERIFIED": "VR VERIFIED",
        "EXTERNALLY VERIFIED": "EXTERNALLY VERIFIED",
        "DERIVED": "DERIVED",
        "INFERRED": "INFERRED",
        "PROPOSED": "PROPOSED",
        "UNKNOWN / TBC": "UNKNOWN / TBC",
        "UNKNOWN/TBC": "UNKNOWN / TBC",
        "CONFLICT": "CONFLICT",
    }
    return mapping.get(t)


def extract_status_from_text(text: str) -> Optional[str]:
    for token in [
        "VR VERIFIED",
        "EXTERNALLY VERIFIED",
        "DERIVED",
        "INFERRED",
        "PROPOSED",
        "UNKNOWN / TBC",
        "UNKNOWN/TBC",
        "CONFLICT",
    ]:
        if token in text:
            return normalize_status_token(token)
    return None


def parse_section_heading(line: str) -> Optional[Dict[str, str]]:
    m = re.match(r"^SECTION\s+(\d+)\s*[—\-]\s*(.+)$", line.strip(), re.IGNORECASE)
    if not m:
        return None
    return {"section_number": m.group(1), "section_title": m.group(2).strip()}


def parse_company_text(text: str) -> List[Dict[str, Any]]:
    lines = text.splitlines()
    sections = []
    current_section = None
    current_lines: List[str] = []

    def flush_section() -> None:
        nonlocal current_section, current_lines
        if current_section:
            sections.append({
                **current_section,
                "lines": current_lines,
                "line_start": current_section.get("line_start"),
                "line_end": current_section.get("line_end"),
            })
        current_section = None
        current_lines = []

    for idx, line in enumerate(lines, start=1):
        heading = parse_section_heading(line)
        if heading:
            flush_section()
            current_section = {
                "section_number": heading["section_number"],
                "section_title": heading["section_title"],
                "line_start": idx,
                "line_end": idx,
            }
            current_lines = [line]
            continue
        if current_section is not None:
            current_section["line_end"] = idx
            current_lines.append(line)

    flush_section()
    return sections
