import fitz
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from app.rag.ingestion.ocr.base import OCRPageResult
from app.rag.ingestion.ocr import ocr_service_from_settings
from app.rag.ingestion.ocr.page_renderer import render_page_to_image


def page_needs_ocr(page_text: str, threshold: int = 40) -> bool:
    cleaned = page_text.strip()
    if not cleaned:
        return True
    meaningful = sum(1 for ch in cleaned if ch.isalpha())
    return meaningful < threshold


def extract_pages(file_path: str, enable_ocr: bool = True) -> Tuple[List[Dict[str, Any]], List[OCRPageResult]]:
    doc = fitz.open(file_path)
    pages = []
    ocr_results: List[OCRPageResult] = []
    ocr_service = ocr_service_from_settings() if enable_ocr else None
    document_hash = _doc_hash(file_path)
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text") or ""
        if page_needs_ocr(text) and ocr_service is not None:
            image_path = render_page_to_image(page, dpi=200)
            try:
                ocr_result = ocr_service.process_document_page(document_hash=document_hash, page_number=page_number, image=image_path)
                ocr_results.append(ocr_result)
                text = ocr_result.full_text or text
            except Exception as exc:
                ocr_results.append(OCRPageResult(page_number=page_number, full_text="", warnings=[f"OCR failed: {exc}"]))
            finally:
                try:
                    Path(image_path).unlink(missing_ok=True)
                except Exception:
                    pass
        elif page_needs_ocr(text) and ocr_service is None:
            ocr_results.append(OCRPageResult(page_number=page_number, full_text="", warnings=["OCR unavailable: install backend/requirements-rag-ingestion.txt"]))
        pages.append({"page_number": page_number, "text": text})
    doc.close()
    return pages, ocr_results


def extract_tables(file_path: str, enable_ocr: bool = True) -> List[Dict[str, Any]]:
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


def _doc_hash(file_path: str) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
