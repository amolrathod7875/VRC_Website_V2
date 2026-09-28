import fitz
from typing import List, Dict, Any, Optional


def extract_pages(file_path: str) -> List[Dict[str, Any]]:
    doc = fitz.open(file_path)
    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text")
        pages.append({"page_number": page_number, "text": text or ""})
    doc.close()
    return pages


def page_needs_ocr(page_text: str, threshold: int = 40) -> bool:
    cleaned = page_text.strip()
    return len(cleaned) < threshold
