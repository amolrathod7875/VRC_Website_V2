import io
import hashlib
import json
import numpy as np
from pathlib import Path
from typing import Optional
from app.rag.config import rag_settings
from app.rag.ingestion.ocr.base import OCRPageResult, OCRBlock, OCRTable, OCRProvider
from app.rag.utils.hashing import calculate_sha256


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        return super().default(obj)


def _serialize_blocks(blocks):
    return [
        {
            "text": b.text,
            "bbox": b.bbox,
            "block_type": b.block_type,
            "confidence": b.confidence,
        }
        for b in blocks
    ]


def _deserialize_blocks(data):
    return [OCRBlock(**b) for b in data]


class OCRCache:
    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = Path(base_dir or ".rag_cache/ocr")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, document_hash: str, page_number: int) -> Path:
        return self.base_dir / document_hash / f"page_{page_number:03d}.json"

    def get(self, document_hash: str, page_number: int) -> Optional[OCRPageResult]:
        path = self._path(document_hash, page_number)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            blocks = _deserialize_blocks(data.get("blocks", []))
            tables = [OCRTable(**t) for t in data.get("tables", [])]
            return OCRPageResult(
                page_number=data["page_number"],
                full_text=data.get("full_text", ""),
                blocks=blocks,
                tables=tables,
                warnings=data.get("warnings", []),
                confidence=data.get("confidence"),
                metadata=data.get("metadata", {}),
            )
        except Exception:
            return None

    def put(self, document_hash: str, page_number: int, result: OCRPageResult) -> None:
        path = self._path(document_hash, page_number)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "page_number": result.page_number,
            "full_text": result.full_text,
            "blocks": _serialize_blocks(result.blocks),
            "tables": [
                {
                    "bbox": t.bbox,
                    "rows": t.rows,
                    "markdown": t.markdown,
                    "confidence": t.confidence,
                }
                for t in result.tables
            ],
            "warnings": result.warnings,
            "confidence": result.confidence,
            "metadata": result.metadata,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2, cls=_JSONEncoder), encoding="utf-8")


class OCRService:
    def __init__(self, provider: OCRProvider, cache: Optional[OCRCache] = None) -> None:
        self.provider = provider
        self.cache = cache or OCRCache()

    def process_document_page(self, document_hash: str, page_number: int, image: str) -> OCRPageResult:
        cached = self.cache.get(document_hash, page_number)
        if cached is not None:
            return cached
        result = self.provider.process_page(image, page_number)
        self.cache.put(document_hash, page_number, result)
        return result
