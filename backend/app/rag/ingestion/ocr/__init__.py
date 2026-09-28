import io
from pathlib import Path
from typing import Optional
from app.rag.ingestion.ocr.base import OCRPageResult, OCRProvider
from app.rag.ingestion.ocr.ocr_service import OCRCache, OCRService
from app.rag.utils.hashing import calculate_sha256


class LayoutModels:
    pass


def ocr_service_from_settings() -> Optional[OCRService]:
    try:
        from app.rag.ingestion.ocr.paddle_ocr import PaddleOCRProvider
        provider = PaddleOCRProvider()
        cache = OCRCache()
        return OCRService(provider=provider, cache=cache)
    except Exception:
        return None
