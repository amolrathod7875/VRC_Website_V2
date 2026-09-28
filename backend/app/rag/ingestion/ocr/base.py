from typing import Any, Dict, List, Optional


class OCRBlock:
    def __init__(self, text: str, bbox: Optional[List[float]] = None, block_type: str = "text", confidence: Optional[float] = None) -> None:
        self.text = text
        self.bbox = bbox or []
        self.block_type = block_type
        self.confidence = confidence


class OCRTable:
    def __init__(
        self,
        bbox: Optional[List[float]] = None,
        rows: Optional[List[List[str]]] = None,
        markdown: str = "",
        confidence: Optional[float] = None,
    ) -> None:
        self.bbox = bbox or []
        self.rows = rows or []
        self.markdown = markdown
        self.confidence = confidence


class OCRPageResult:
    def __init__(
        self,
        page_number: int,
        full_text: str = "",
        blocks: Optional[List[OCRBlock]] = None,
        tables: Optional[List[OCRTable]] = None,
        warnings: Optional[List[str]] = None,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.page_number = page_number
        self.full_text = full_text
        self.blocks = blocks or []
        self.tables = tables or []
        self.warnings = warnings or []
        self.confidence = confidence
        self.metadata = metadata or {}


class OCRProvider:
    def process_page(self, image, page_number: int) -> OCRPageResult:
        raise NotImplementedError
