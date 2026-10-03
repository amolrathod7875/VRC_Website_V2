"""
Phase 9A — OCR Pipeline Validation Pilot Script

Pilot catalogues:
- rhino.pdf
- Elephant.pdf
- manual_GUNS.pdf
- VRC MIX (LOW - MEDIUM) PRESSURE.pdf
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import traceback
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure backend is importable
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.ingestion.pdf_parser import extract_pages, page_needs_ocr
from app.rag.ingestion.ocr.ocr_service import OCRService, OCRCache
from app.rag.ingestion.ocr.paddle_ocr import PaddleOCRProvider
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.metadata_builder import build_catalogue_metadata
from app.rag.product_identity import get_canonical_slug
from app.rag.constants import (
    CATALOGUE_AUTHORITY_PRIORITY,
    CHUNK_TYPE_DESCRIPTION,
    CHUNK_TYPE_FEATURES,
    CHUNK_TYPE_APPLICATIONS,
    CHUNK_TYPE_TECHNICAL_MODEL,
    CHUNK_TYPE_TECHNICAL_TABLE,
    CHUNK_TYPE_OTHER,
    CHUNK_TYPE_ACCESSORIES,
    CHUNK_TYPE_NOTES,
    SOURCE_TYPE_CATALOGUE,
    STATUS_INDEXED,
    STATUS_FAILED,
    STATUS_PROCESSING,
    DATA_STATUS_UNKNOWN_TBC,
)
from app.rag.ingestion.pdf_table_parser import extract_tables, parse_spec_table, is_likely_spec_table
from app.rag.utils.text import normalize_text
from app.rag.config import rag_settings
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.models.rag_document import RagDocument, RagIngestionRun
from app.core.database import async_session_factory
from sqlalchemy import select
import asyncio


PILOT_FILES = [
    "storage/catalogues/rhino.pdf",
    "storage/catalogues/Elephant.pdf",
    "storage/catalogues/manual_GUNS.pdf",
    "storage/catalogues/VRC MIX (LOW - MEDIUM) PRESSURE.pdf",
]

DEBUG_DIR = Path(__file__).resolve().parent / "rag_debug" / "phase9a_pilot"


@dataclass
class PreOCRInventory:
    filename: str
    sha256: str
    page_count: int
    alpha_chars_per_page: List[int]
    product_guess: str
    ocr_cache_exists: bool
    qdrant_existing_points: int
    product_slug: str


@dataclass
class OCRPageAudit:
    page_number: int
    character_count: int
    line_count: int
    avg_confidence: Optional[float]
    min_confidence: Optional[float]
    low_confidence_lines: List[Dict[str, Any]]
    technical_identifiers: List[str]
    tables_detected: bool
    warnings: List[str]
    block_count: int
    full_text_preview: str


@dataclass
class CatalogueAudit:
    filename: str
    sha256: str
    product_slug: str
    pages_total: int
    ocr_pages: int
    total_characters: int
    total_lines: int
    low_confidence_pages: int
    technical_identifiers: List[str]
    tables_reconstructed: int
    chunks_generated: int
    suspicious_chunks: List[str]
    pages_requiring_review: List[int]
    decisions: str
    approval_reason: str
    page_audits: List[OCRPageAudit] = field(default_factory=list)


def compute_sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def pre_ocr_inventory(file_path: str) -> PreOCRInventory:
    import fitz
    path = Path(file_path)
    sha = compute_sha256(file_path)
    doc = fitz.open(file_path)
    page_count = len(doc)
    alpha_per_page = []
    for page in doc:
        text = page.get_text("text") or ""
        alpha_per_page.append(sum(1 for ch in text if ch.isalpha()))
    doc.close()

    raw_name = path.stem
    slug = get_canonical_slug(raw_name) or raw_name.lower().replace(" ", "-").replace("_", "-")
    slug = slug.replace(".pdf", "")

    cache_dir = Path(".rag_cache/ocr") / sha
    cache_exists = cache_dir.exists() and any(cache_dir.iterdir())

    return PreOCRInventory(
        filename=path.name,
        sha256=sha,
        page_count=page_count,
        alpha_chars_per_page=alpha_per_page,
        product_guess=raw_name,
        ocr_cache_exists=cache_exists,
        qdrant_existing_points=0,
        product_slug=slug,
    )


def run_ocr_on_pilot(
    file_path: str,
    provider: PaddleOCRProvider,
    cache: OCRCache,
    debug_dir: Path,
) -> tuple[List[Dict[str, Any]], List[OCRPageResult], float, bool]:
    """Run OCR on a pilot file. Returns pages, ocr_results, duration, cache_hit."""
    path = Path(file_path)
    sha = compute_sha256(file_path)
    product_slug = pre_ocr_inventory(file_path).product_slug

    ocr_service = OCRService(provider=provider, cache=cache)
    doc_hash = sha

    start = time.perf_counter()
    pages, ocr_results = extract_pages(file_path, enable_ocr=True)
    duration = time.perf_counter() - start

    # Determine cache hit rate
    cache_dir = Path(".rag_cache/ocr") / sha
    cached_pages = len(list(cache_dir.glob("page_*.json"))) if cache_dir.exists() else 0
    cache_hit = cached_pages > 0 and duration < 5.0

    # Save OCR debug artifacts
    product_dir = debug_dir / product_slug
    product_dir.mkdir(parents=True, exist_ok=True)

    ocr_artifacts = []
    for ocr_res in ocr_results:
        blocks_data = []
        for b in ocr_res.blocks:
            blocks_data.append({
                "text": b.text,
                "bbox": b.bbox,
                "block_type": b.block_type,
                "confidence": b.confidence,
            })
        ocr_artifacts.append({
            "page_number": ocr_res.page_number,
            "full_text": ocr_res.full_text,
            "blocks": blocks_data,
            "tables": [
                {"bbox": t.bbox, "rows": t.rows, "markdown": t.markdown, "confidence": t.confidence}
                for t in ocr_res.tables
            ],
            "warnings": ocr_res.warnings,
            "confidence": ocr_res.confidence,
            "metadata": ocr_res.metadata,
        })

    (product_dir / "ocr_results.json").write_text(
        json.dumps(ocr_artifacts, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    # Save normalized text per page
    normalized_pages = []
    for page in pages:
        normalized_pages.append({
            "page_number": page["page_number"],
            "text": normalize_text(page["text"]),
        })
    (product_dir / "normalized_text.json").write_text(
        json.dumps(normalized_pages, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return pages, ocr_results, duration, cache_hit


def audit_ocr_page(page_result: OCRPageResult, page_number: int) -> OCRPageAudit:
    text = page_result.full_text or ""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chars = len(text)
    line_count = len(lines)

    confidences = [b.confidence for b in page_result.blocks if b.confidence is not None]
    avg_conf = sum(confidences) / len(confidences) if confidences else None
    min_conf = min(confidences) if confidences else None

    low_conf_lines = []
    for b in page_result.blocks:
        if b.confidence is not None and b.confidence < 0.8:
            low_conf_lines.append({
                "text": b.text,
                "confidence": b.confidence,
                "bbox": b.bbox,
            })

    # Detect technical identifiers
    import re
    identifiers = []
    for pattern in [r"\b\d+:\d+\b", r"\b\d+/\d+\b", r'\b\d+"\b', r"\b\d+'\"?\b", r"\b\d+\.\d+:\d+\b"]:
        identifiers.extend(re.findall(pattern, text))

    # Check for tables
    has_tables = "TECHNICAL SPECIFICATIONS" in text.upper() or len(page_result.tables) > 0

    return OCRPageAudit(
        page_number=page_number,
        character_count=chars,
        line_count=line_count,
        avg_confidence=avg_conf,
        min_confidence=min_conf,
        low_confidence_lines=low_conf_lines,
        technical_identifiers=identifiers[:20],
        tables_detected=has_tables,
        warnings=list(page_result.warnings),
        block_count=len(page_result.blocks),
        full_text_preview=text[:500],
    )


def audit_catalogue(
    file_path: str,
    pages: List[Dict[str, Any]],
    ocr_results: List[OCRPageResult],
    chunks: List[Dict[str, Any]],
    product_slug: str,
) -> CatalogueAudit:
    sha = compute_sha256(file_path)
    pages_total = len(pages)
    ocr_pages = len(ocr_results)

    total_chars = sum(len(r.full_text or "") for r in ocr_results)
    total_lines = sum(
        len([l for l in (r.full_text or "").splitlines() if l.strip()])
        for r in ocr_results
    )

    all_identifiers: List[str] = []
    page_audits = []
    low_conf_pages = 0
    suspicious_chunks = []

    for r in ocr_results:
        audit = audit_ocr_page(r, r.page_number)
        page_audits.append(audit)
        all_identifiers.extend(audit.technical_identifiers)
        if audit.low_confidence_lines:
            low_conf_pages += 1

    for chunk in chunks:
        text = chunk.get("text", "")
        if not text or len(text) < 20:
            suspicious_chunks.append(chunk.get("chunk_id", "unknown"))
        # Check for suspicious patterns like "30 150" instead of "30:150"
        import re
        if re.search(r"\b\d+\s+\d+\b", text) and ":" not in text:
            if re.search(r"\d+:\d+", text) is None:
                suspicious_chunks.append(chunk.get("chunk_id", "unknown"))

    # Table reconstruction check
    tables_count = 0
    for r in ocr_results:
        if "TECHNICAL SPECIFICATIONS" in (r.full_text or "").upper():
            tables_count += 1

    # Determine approval
    review_pages = [a.page_number for a in page_audits if a.low_confidence_lines]
    suspicious = len(suspicious_chunks)
    low_conf = low_conf_pages

    if suspicious > 3:
        decision = "OCR_REVIEW_REQUIRED"
        reason = f"{suspicious} suspicious chunks, {low_conf} low-confidence pages"
    elif low_conf > 0 and total_chars < 200:
        decision = "OCR_REVIEW_REQUIRED"
        reason = "Low OCR output with low confidence"
    elif total_chars < 50:
        decision = "FAILED"
        reason = "OCR produced too little text"
    else:
        decision = "APPROVED"
        reason = f"{total_chars} chars, {len(chunks)} chunks, {ocr_pages} OCR pages"

    return CatalogueAudit(
        filename=Path(file_path).name,
        sha256=sha,
        product_slug=product_slug,
        pages_total=pages_total,
        ocr_pages=ocr_pages,
        total_characters=total_chars,
        total_lines=total_lines,
        low_confidence_pages=low_conf_pages,
        technical_identifiers=list(set(all_identifiers)),
        tables_reconstructed=tables_count,
        chunks_generated=len(chunks),
        suspicious_chunks=suspicious_chunks[:10],
        pages_requiring_review=review_pages,
        decisions=decision,
        approval_reason=reason,
        page_audits=page_audits,
    )


async def ingest_pilot_approved(
    file_path: str,
    pages: List[Dict[str, Any]],
    ocr_results: List[OCRPageResult],
    product_slug: str,
    debug_dir: Path,
    dry_run: bool = True,
) -> Dict[str, Any]:
    """Ingest an approved pilot catalogue into Qdrant and PostgreSQL."""
    path = Path(file_path)
    document_name = path.name
    sha = compute_sha256(file_path)

    # Build chunks
    tables = extract_tables(file_path)
    document_id = None

    # Pre-chunk for counting
    chunks = chunk_catalogue(
        document_name=document_name,
        pages=pages,
        tables=tables,
        product_slug=product_slug,
        document_id="preview-doc-id",
        ocr_results=ocr_results,
    )

    if not chunks:
        return {"status": "no_chunks", "document_name": document_name}

    # Save chunks preview
    product_dir = debug_dir / product_slug
    product_dir.mkdir(parents=True, exist_ok=True)
    (product_dir / "chunks_preview.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    if dry_run:
        return {"status": "dry_run", "chunks": len(chunks), "document_name": document_name}

    # Actual ingestion
    async with async_session_factory() as db:
        qdrant_store = QdrantStore()
        dense = DenseEmbeddingService()
        sparse = SparseEmbeddingService()

        existing = await db.execute(select(RagDocument).where(RagDocument.document_name == document_name))
        existing_doc = existing.scalar_one_or_none()

        if existing_doc and existing_doc.sha256 == sha:
            return {"status": "skipped", "document_name": document_name, "reason": "unchanged"}

        if existing_doc:
            document_id = existing_doc.qdrant_document_id
        else:
            import uuid
            document_id = str(uuid.uuid4())
            existing_doc = RagDocument(
                document_name=document_name,
                source_type=SOURCE_TYPE_CATALOGUE,
                storage_path=str(path.resolve()),
                sha256=sha,
                status=STATUS_PROCESSING,
                qdrant_document_id=document_id,
                product_slug=product_slug,
            )
            db.add(existing_doc)
            await db.flush()

        run = RagIngestionRun(
            document_id=existing_doc.id,
            document_name=document_name,
            source_type=SOURCE_TYPE_CATALOGUE,
            status="started",
        )
        db.add(run)
        await db.flush()

        try:
            # Regenerate chunks with proper document_id
            chunks = chunk_catalogue(
                document_name=document_name,
                pages=pages,
                tables=tables,
                product_slug=product_slug,
                document_id=document_id,
                ocr_results=ocr_results,
            )

            texts = [c["text"] for c in chunks]
            print(f"  Embedding {len(texts)} chunks for {document_name}...")
            dense_vectors = dense.embed_documents(texts)
            sparse_vectors = sparse.embed_documents(texts)

            if existing_doc.qdrant_document_id and document_id:
                await qdrant_store.delete_by_document_id(document_id)

            payloads = []
            for chunk in chunks:
                metadata = build_catalogue_metadata(
                    document_id=document_id,
                    document_name=document_name,
                    storage_path=str(path.resolve()),
                    sha256=sha,
                    product_slug=product_slug,
                    chunk=chunk,
                )
                payloads.append(metadata)

            print(f"  Uploading {len(payloads)} points to Qdrant for {document_name}...")
            await qdrant_store.upsert_points(
                document_id=document_id,
                dense_vectors=dense_vectors,
                sparse_vectors=sparse_vectors,
                payloads=payloads,
            )

            existing_doc.sha256 = sha
            existing_doc.qdrant_document_id = document_id
            existing_doc.chunk_count = len(chunks)
            existing_doc.status = STATUS_INDEXED
            existing_doc.last_ingested_at = existing_doc.updated_at
            run.status = STATUS_INDEXED
            run.chunks_created = len(chunks)
            await db.commit()

            return {"status": "indexed", "document_name": document_name, "chunks": len(chunks)}
        except Exception as exc:
            existing_doc.status = STATUS_FAILED
            existing_doc.last_error = str(exc)
            run.status = STATUS_FAILED
            run.error = str(exc)
            await db.commit()
            traceback.print_exc()
            return {"status": "failed", "document_name": document_name, "error": str(exc)}


async def main():
    print("=" * 60)
    print("PHASE 9A — OCR PIPELINE VALIDATION PILOT")
    print("=" * 60)

    # Initialize OCR provider and cache
    provider = PaddleOCRProvider(lang="en", use_gpu=False)
    cache = OCRCache(base_dir=".rag_cache/ocr")

    DEBUG_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Pre-OCR Inventory
    print("\n[STEP 1] Pre-OCR Inventory")
    inventories: List[PreOCRInventory] = []
    for file_path in PILOT_FILES:
        inv = pre_ocr_inventory(file_path)
        inv.qdrant_existing_points = 0
        inventories.append(inv)
        print(f"  {inv.filename}: pages={inv.page_count}, sha256={inv.sha256[:16]}..., "
              f"alpha_chars_first_page={inv.alpha_chars_per_page[0]}, "
              f"slug={inv.product_slug}, cached={inv.ocr_cache_exists}")

    # Save pre-OCR inventory
    inv_data = []
    for inv in inventories:
        inv_data.append({
            "filename": inv.filename,
            "sha256": inv.sha256,
            "page_count": inv.page_count,
            "alpha_chars_per_page": inv.alpha_chars_per_page,
            "product_guess": inv.product_guess,
            "ocr_cache_exists": inv.ocr_cache_exists,
            "product_slug": inv.product_slug,
        })
    (DEBUG_DIR / "pre_ocr_inventory.json").write_text(
        json.dumps(inv_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Step 2: Run OCR on each pilot catalogue
    print("\n[STEP 2] OCR Execution")
    pilot_results: Dict[str, Any] = {}
    for file_path in PILOT_FILES:
        filename = Path(file_path).name
        slug = next(i.product_slug for i in inventories if i.filename == filename)
        print(f"\n  OCR on {filename}...")
        try:
            pages, ocr_results, duration, cache_hit = run_ocr_on_pilot(
                file_path, provider, cache, DEBUG_DIR
            )
            pilot_results[slug] = {
                "pages": pages,
                "ocr_results": ocr_results,
                "duration": duration,
                "cache_hit": cache_hit,
                "filename": filename,
                "sha256": compute_sha256(file_path),
            }
            print(f"    Pages: {len(pages)}, OCR pages: {len(ocr_results)}, "
                  f"Duration: {duration:.2f}s, Cache hit: {cache_hit}")
            for r in ocr_results:
                print(f"    Page {r.page_number}: {len(r.full_text or '')} chars, "
                      f"{len(r.blocks)} blocks, warnings={r.warnings}")
        except Exception as exc:
            print(f"    FAILED: {exc}")
            traceback.print_exc()
            pilot_results[slug] = {"error": str(exc), "filename": filename}

    # Step 3: Chunk and Audit
    print("\n[STEP 3] Chunking and Auditing")
    audits: List[CatalogueAudit] = []
    approved: List[str] = []
    review_required: List[str] = []
    failed: List[str] = []

    for file_path in PILOT_FILES:
        filename = Path(file_path).name
        slug = next(i.product_slug for i in inventories if i.filename == filename)
        result = pilot_results.get(slug)
        if not result or "error" in result:
            failed.append(filename)
            continue

        pages = result["pages"]
        ocr_results = result["ocr_results"]
        tables = extract_tables(file_path)
        document_id = "audit-doc-id"

        chunks = chunk_catalogue(
            document_name=filename,
            pages=pages,
            tables=tables,
            product_slug=slug,
            document_id=document_id,
            ocr_results=ocr_results,
        )

        audit = audit_catalogue(
            file_path=file_path,
            pages=pages,
            ocr_results=ocr_results,
            chunks=chunks,
            product_slug=slug,
        )
        audits.append(audit)

        print(f"\n  {filename}:")
        print(f"    Decision: {audit.decisions}")
        print(f"    Reason: {audit.approval_reason}")
        print(f"    Chunks: {audit.chunks_generated}")
        print(f"    Technical IDs: {audit.technical_identifiers[:5]}")
        print(f"    Review pages: {audit.pages_requiring_review}")
        print(f"    Suspicious chunks: {audit.suspicious_chunks[:3]}")

        if audit.decisions == "APPROVED":
            approved.append(filename)
        elif audit.decisions == "OCR_REVIEW_REQUIRED":
            review_required.append(filename)
        else:
            failed.append(filename)

    # Save audit results
    audit_summary = []
    for audit in audits:
        audit_summary.append({
            "filename": audit.filename,
            "sha256": audit.sha256,
            "product_slug": audit.product_slug,
            "pages_total": audit.pages_total,
            "ocr_pages": audit.ocr_pages,
            "total_characters": audit.total_characters,
            "total_lines": audit.total_lines,
            "low_confidence_pages": audit.low_confidence_pages,
            "technical_identifiers": audit.technical_identifiers,
            "tables_reconstructed": audit.tables_reconstructed,
            "chunks_generated": audit.chunks_generated,
            "suspicious_chunks": audit.suspicious_chunks,
            "pages_requiring_review": audit.pages_requiring_review,
            "decisions": audit.decisions,
            "approval_reason": audit.approval_reason,
        })
    (DEBUG_DIR / "audit_summary.json").write_text(
        json.dumps(audit_summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Save full page audits
    for audit in audits:
        page_audit_data = []
        for pa in audit.page_audits:
            page_audit_data.append({
                "page_number": pa.page_number,
                "character_count": pa.character_count,
                "line_count": pa.line_count,
                "avg_confidence": pa.avg_confidence,
                "min_confidence": pa.min_confidence,
                "low_confidence_lines": pa.low_confidence_lines[:5],
                "technical_identifiers": pa.technical_identifiers,
                "tables_detected": pa.tables_detected,
                "warnings": pa.warnings,
                "block_count": pa.block_count,
                "full_text_preview": pa.full_text_preview,
            })
        (DEBUG_DIR / audit.product_slug / "page_audits.json").write_text(
            json.dumps(page_audit_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # Step 4: Ingest approved (dry run first)
    print("\n[STEP 4] Dry-run Ingestion of Approved Pilot Catalogues")
    dry_run_results = {}
    for file_path in PILOT_FILES:
        filename = Path(file_path).name
        slug = next(i.product_slug for i in inventories if i.filename == filename)
        if filename not in approved:
            continue
        result = pilot_results.get(slug)
        if not result or "error" in result:
            continue
        pages = result["pages"]
        ocr_results = result["ocr_results"]
        try:
            ing = await ingest_pilot_approved(
                file_path, pages, ocr_results, slug, DEBUG_DIR, dry_run=True
            )
            dry_run_results[filename] = ing
            print(f"  Dry-run {filename}: {ing}")
        except Exception as exc:
            print(f"  Dry-run FAILED for {filename}: {exc}")
            traceback.print_exc()

    # Step 5: Actual Ingestion of Approved
    print("\n[STEP 5] Actual Ingestion of Approved Pilot Catalogues")
    ingestion_results = {}
    for file_path in PILOT_FILES:
        filename = Path(file_path).name
        slug = next(i.product_slug for i in inventories if i.filename == filename)
        if filename not in approved:
            continue
        result = pilot_results.get(slug)
        if not result or "error" in result:
            continue
        pages = result["pages"]
        ocr_results = result["ocr_results"]
        try:
            ing = await ingest_pilot_approved(
                file_path, pages, ocr_results, slug, DEBUG_DIR, dry_run=False
            )
            ingestion_results[filename] = ing
            print(f"  Ingested {filename}: {ing}")
        except Exception as exc:
            print(f"  Ingestion FAILED for {filename}: {exc}")
            traceback.print_exc()
            ingestion_results[filename] = {"status": "failed", "error": str(exc)}

    # Step 6: Idempotency Test
    print("\n[STEP 6] Idempotency Test (second run)")
    idempotency_results = {}
    for file_path in PILOT_FILES:
        filename = Path(file_path).name
        slug = next(i.product_slug for i in inventories if i.filename == filename)
        if filename not in approved:
            continue
        result = pilot_results.get(slug)
        if not result or "error" in result:
            continue
        pages = result["pages"]
        ocr_results = result["ocr_results"]
        try:
            ing = await ingest_pilot_approved(
                file_path, pages, ocr_results, slug, DEBUG_DIR, dry_run=False
            )
            idempotency_results[filename] = ing
            print(f"  Second run {filename}: {ing}")
        except Exception as exc:
            print(f"  Idempotency test FAILED for {filename}: {exc}")
            idempotency_results[filename] = {"status": "failed", "error": str(exc)}

    # Save final pilot report
    final_report = {
        "pilot_catalogues": [i.filename for i in inventories],
        "pre_ocr_inventory": inv_data,
        "approved": approved,
        "review_required": review_required,
        "failed": failed,
        "audits": audit_summary,
        "dry_run_results": {k: v for k, v in dry_run_results.items()},
        "ingestion_results": {k: v for k, v in ingestion_results.items()},
        "idempotency_results": {k: v for k, v in idempotency_results.items()},
    }
    (DEBUG_DIR / "phase9a_pilot_report.json").write_text(
        json.dumps(final_report, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("PHASE 9A PILOT COMPLETE")
    print(f"Approved: {approved}")
    print(f"Review Required: {review_required}")
    print(f"Failed: {failed}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
