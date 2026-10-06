"""
Page-specific OCR remediation for VR Coatings catalogues.

Provides targeted OCR repair for individual pages while preserving
existing cached OCR for good pages. Tests a controlled set of
preprocessing variants and selects the best result based on
semantic quality.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import fitz
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage


def _doc_hash(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def render_page(page, dpi: int = 200) -> str:
    pix = page.get_pixmap(dpi=dpi)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp_path = tmp.name
    pix.save(tmp_path)
    tmp.close()
    return tmp_path


def preprocess_image(image_path: str, variant: str) -> str:
    img = Image.open(image_path)
    if variant == "base_200dpi":
        return image_path
    elif variant == "base_300dpi":
        return image_path
    elif variant == "grayscale_200dpi":
        img = img.convert("L")
    elif variant == "grayscale_300dpi":
        img = img.convert("L")
    elif variant == "contrast_enhanced_200dpi":
        img = img.convert("RGB")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
    elif variant == "sharpened_200dpi":
        img = img.convert("RGB")
        img = img.filter(ImageFilter.SHARPEN)
    elif variant == "contrast_sharpen_200dpi":
        img = img.convert("RGB")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        img = img.filter(ImageFilter.SHARPEN)
    elif variant == "threshold_200dpi":
        img = img.convert("L")
        img = img.point(lambda x: 0 if x < 128 else 255, "1")
    elif variant == "contrast_sharpen_300dpi":
        img = img.convert("RGB")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        img = img.filter(ImageFilter.SHARPEN)
    elif variant.startswith("adaptive_"):
        parts = variant.split("_")
        size = int(parts[1])
        offset = int(parts[2])
        img = img.convert("L")
        arr = np.array(img)
        mean = ndimage.uniform_filter(arr.astype(np.float32), size=size)
        binary = np.where(arr > mean + offset, 255, 0).astype(np.uint8)
        out = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        out_path = out.name
        Image.fromarray(binary).save(out_path)
        out.close()
        return out_path
    else:
        return image_path

    if variant in ("grayscale_200dpi", "grayscale_300dpi", "threshold_200dpi"):
        out = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    else:
        out = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    out_path = out.name
    img.save(out_path)
    out.close()
    return out_path


def run_ocr(image_path: str) -> Tuple[str, List[Dict[str, Any]]]:
    os.environ.setdefault("FLAGS_enable_pir_api", "0")
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(lang="en", enable_mkldnn=False)
    result = ocr.ocr(image_path)
    full_text = ""
    blocks: List[Dict[str, Any]] = []
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
            blocks.append({"text": text, "bbox": bbox, "confidence": float(score) if score is not None else None})
        full_text = "\n".join(texts)
    return full_text, blocks


def audit_ocr(full_text: str, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    lines = [l.strip() for l in full_text.splitlines() if l.strip()]
    useful_chars = sum(1 for ch in full_text if ch.isalpha())
    garbage_indicators = {
        "ce", "Polyhose", "équipent", "irle", "panting", "low", "duty",
        "VR Coatings", "I", "PUUP", "AEL", "VR ngs", "VR Congs",
    }
    garbage_count = sum(1 for line in lines if any(g in line for g in garbage_indicators))
    detected_blocks = len(blocks)
    technical_ids = [
        b["text"] for b in blocks
        if ":" in b["text"] and any(c.isdigit() for c in b["text"])
    ]
    table_labels = [
        b["text"] for b in blocks
        if b["text"].lower() in {
            "type", "pressure ratio", "output per cycle", "air motor piston",
            "stroke length", "recommended spray", "air inlet pressure", "output pressure",
        }
    ]
    return {
        "useful_char_count": useful_chars,
        "lines": len(lines),
        "detected_blocks": detected_blocks,
        "technical_identifiers_recovered": len(technical_ids),
        "technical_identifiers": technical_ids[:10],
        "table_labels_recovered": len(table_labels),
        "table_labels": table_labels,
        "garbage_lines": garbage_count,
        "obvious_garbage_ratio": garbage_count / max(len(lines), 1),
        "full_text_preview": full_text[:500],
    }


def score_variant(audit: Dict[str, Any]) -> float:
    score = 0.0
    score += min(audit["useful_char_count"], 200) * 0.5
    score += audit["detected_blocks"] * 2.0
    score += audit["technical_identifiers_recovered"] * 10.0
    score += audit["table_labels_recovered"] * 15.0
    score -= audit["obvious_garbage_ratio"] * 100.0
    return score


def remediate_page(
    pdf_path: str,
    page_number: int,
    variants: Optional[List[str]] = None,
    cache_dir: Optional[str] = None,
) -> Dict[str, Any]:
    if variants is None:
        variants = [
            "base_200dpi",
            "base_300dpi",
            "grayscale_200dpi",
            "contrast_enhanced_200dpi",
            "sharpened_200dpi",
            "contrast_sharpen_200dpi",
            "threshold_200dpi",
            "adaptive_15_5",
            "adaptive_25_0",
        ]

    doc_hash = _doc_hash(pdf_path)
    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]

    results: Dict[str, Any] = {}
    for variant in variants:
        try:
            if "300dpi" in variant:
                dpi = 300
            else:
                dpi = 200
            rendered = render_page(page, dpi=dpi)
            processed = preprocess_image(rendered, variant)
            full_text, blocks = run_ocr(processed)
            audit = audit_ocr(full_text, blocks)
            results[variant] = {
                "audit": audit,
                "full_text": full_text,
                "blocks_count": len(blocks),
                "score": score_variant(audit),
            }
            if processed != rendered:
                try:
                    os.unlink(processed)
                except Exception:
                    pass
            try:
                os.unlink(rendered)
            except Exception:
                pass
        except Exception as exc:
            results[variant] = {"error": str(exc), "score": -999.0}

    doc.close()

    best_variant = max(
        (k for k, v in results.items() if "error" not in v),
        key=lambda k: results[k]["score"],
        default=None,
    )

    best_result = results.get(best_variant, {}) if best_variant else {}
    best_audit = best_result.get("audit", {})

    report = {
        "document_hash": doc_hash,
        "page_number": page_number,
        "variants_tested": len(variants),
        "best_variant": best_variant,
        "best_score": best_result.get("score"),
        "best_audit": best_audit,
        "best_full_text": best_result.get("full_text"),
        "best_blocks_count": best_result.get("blocks_count"),
        "all_results": results,
    }

    if cache_dir and best_variant:
        cache_path = Path(cache_dir) / doc_hash / f"page_{page_number:03d}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_data = {
            "page_number": page_number,
            "full_text": best_result.get("full_text", ""),
            "blocks": [
                {
                    "text": b["text"],
                    "bbox": b.get("bbox", []),
                    "block_type": "text",
                    "confidence": b.get("confidence"),
                }
                for b in best_result.get("blocks", [])
            ],
            "tables": [],
            "warnings": [],
            "confidence": best_audit.get("useful_char_count", 0) / max(
                len(best_result.get("full_text", "")), 1
            ),
            "metadata": {
                "remediation_variant": best_variant,
                "remediation_score": best_result.get("score"),
            },
        }
        cache_path.write_text(
            json.dumps(cache_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report["cache_written"] = str(cache_path)

    return report


def remediate_barrel_pump(
    pdf_path: str,
    bad_pages: Optional[List[int]] = None,
    cache_dir: Optional[str] = None,
) -> Dict[str, Any]:
    if bad_pages is None:
        bad_pages = [1]

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    doc.close()

    page_reports = {}
    for page_number in bad_pages:
        if page_number < 1 or page_number > total_pages:
            continue
        report = remediate_page(pdf_path, page_number, cache_dir=cache_dir)
        page_reports[page_number] = report

    return {
        "pdf_path": pdf_path,
        "document_hash": _doc_hash(pdf_path),
        "total_pages": total_pages,
        "remediated_pages": list(page_reports.keys()),
        "page_reports": page_reports,
    }
