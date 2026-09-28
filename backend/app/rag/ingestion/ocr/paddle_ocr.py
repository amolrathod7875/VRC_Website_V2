from typing import Any, Dict, List, Optional
from app.rag.ingestion.ocr.base import OCRBlock, OCRPageResult, OCRProvider


class PaddleOCRProvider(OCRProvider):
    def __init__(self, lang: str = "en", use_gpu: bool = False) -> None:
        self.lang = lang
        self.use_gpu = use_gpu
        self._client = None
        self._init_time: Optional[float] = None

    def _lazy_init(self) -> None:
        if self._client is None:
            import os
            os.environ.setdefault("FLAGS_enable_pir_api", "0")
            from paddleocr import PaddleOCR
            self._client = PaddleOCR(lang=self.lang, enable_mkldnn=False)

    def process_page(self, image_path: str, page_number: int) -> OCRPageResult:
        self._lazy_init()
        result = self._client.ocr(image_path)
        full_text = ""
        blocks: List[OCRBlock] = []
        tables: List[dict] = []
        warnings: List[str] = []
        confidence = None
        table_confidence = None

        if result and result[0]:
            page_result = result[0]
            texts = getattr(page_result, "rec_texts", None) or page_result.get("rec_texts", []) if hasattr(page_result, "get") else []
            scores = getattr(page_result, "rec_scores", None) or page_result.get("rec_scores", []) if hasattr(page_result, "get") else []
            boxes = getattr(page_result, "rec_boxes", None) or page_result.get("rec_boxes", []) if hasattr(page_result, "get") else []

            for idx, text in enumerate(texts):
                if not text:
                    continue
                score = scores[idx] if idx < len(scores) else None
                box = boxes[idx] if idx < len(boxes) else None
                bbox = box.flatten().tolist() if hasattr(box, "flatten") else list(box) if box is not None else []
                blocks.append(OCRBlock(text=text, bbox=bbox, confidence=float(score) if score is not None else None))
            full_text = "\n".join(texts)
            if blocks:
                confidence = sum(b.confidence or 0 for b in blocks) / len(blocks)
                numeric_blocks = [b for b in blocks if self._is_numeric(b.text)]
                if numeric_blocks:
                    table_confidence = sum(b.confidence or 0 for b in numeric_blocks) / len(numeric_blocks)
                    if table_confidence < 0.9:
                        warnings.append(
                            f"TABLE_CONFIDENCE_WARNING: numeric block confidence {table_confidence:.3f} "
                            "is below 0.9; technical values may require manual verification."
                        )

        metadata: Dict[str, Any] = {
            "text_confidence": confidence,
            "table_confidence": table_confidence,
        }
        return OCRPageResult(
            page_number=page_number,
            full_text=full_text,
            blocks=blocks,
            tables=tables,
            warnings=warnings,
            confidence=confidence,
            metadata=metadata,
        )

    @staticmethod
    def _is_numeric(text: str) -> bool:
        import re
        return bool(re.search(r"\d", text))
