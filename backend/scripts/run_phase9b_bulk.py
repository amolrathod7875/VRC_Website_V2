"""
Phase 9B — Bulk OCR Pipeline Validation and Ingestion

Processes the 24 unprocessed catalogues in 4 batches of ~6 documents each.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import sys
import time
import traceback
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure backend is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import fitz
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.rag.ingestion.pdf_parser import extract_pages, page_needs_ocr
from app.rag.ingestion.ocr.ocr_service import OCRCache, OCRService
from app.rag.ingestion.ocr.paddle_ocr import PaddleOCRProvider
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.metadata_builder import build_catalogue_metadata
from app.rag.product_identity import get_canonical_slug, PRODUCT_ALIASES
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
)
from app.rag.ingestion.pdf_table_parser import extract_tables, parse_spec_table
from app.rag.utils.text import normalize_text
from app.rag.config import rag_settings
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.models.rag_document import RagDocument, RagIngestionRun
from app.core.database import async_session_factory


CATALOGUE_ROOT = Path(__file__).resolve().parent.parent / "storage" / "catalogues"
DEBUG_DIR = Path(__file__).resolve().parent / "rag_debug" / "phase9b_bulk"
OCR_CACHE_DIR = Path(".rag_cache/ocr")

# Files excluded from normal Phase 9B bulk ingestion
EXCLUDED_FILES = {
    "manual_GUNS.pdf",
    "VRC MIX (LOW - MEDIUM) PRESSURE.pdf",
}

# Already indexed files (from PostgreSQL)
INDEXED_FILES = {
    "Tiger.pdf",
    "LION_Catalogue.pdf",
    "rhino.pdf",
    "Elephant.pdf",
}


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
    action: str = "OCR_AUDIT"


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


@dataclass
class BatchResult:
    batch_number: int
    files_processed: List[str]
    approved: List[str]
    review_required: List[str]
    failed: List[str]
    chunks_generated: int
    chunks_indexed: int
    qdrant_before: int
    qdrant_after: int
    postgres_before: int
    postgres_after: int
    warnings: List[str]


def compute_sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_qdrant_point_count() -> int:
    from qdrant_client import QdrantClient
    client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
    return client.count(collection_name=rag_settings.QDRANT_COLLECTION_NAME).count


def get_qdrant_points_for_document(document_id: str) -> int:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
    points, _ = client.scroll(
        collection_name=rag_settings.QDRANT_COLLECTION_NAME,
        scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]),
        limit=4096,
        with_payload=False,
    )
    return len(points)


async def get_postgres_document_count() -> int:
    from sqlalchemy import func
    from app.models.rag_document import RagDocument

    async with async_session_factory() as db:
        from sqlalchemy import select, func
        result = await db.execute(select(func.count()).select_from(RagDocument))
        return result.scalar_one()


def pre_ocr_inventory(file_path: str, existing_points: int = 0) -> PreOCRInventory:
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
    slug = get_canonical_slug(raw_name)
    if not slug:
        slug = raw_name.lower().replace(" ", "-").replace("_", "-")
        slug = re.sub(r"[^a-z0-9-]", "", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")

    cache_dir = OCR_CACHE_DIR / sha
    cache_exists = cache_dir.exists() and any(cache_dir.iterdir())

    return PreOCRInventory(
        filename=path.name,
        sha256=sha,
        page_count=page_count,
        alpha_chars_per_page=alpha_per_page,
        product_guess=raw_name,
        ocr_cache_exists=cache_exists,
        qdrant_existing_points=existing_points,
        product_slug=slug,
    )


def run_ocr_on_document(
    file_path: str,
    provider: PaddleOCRProvider,
    cache: OCRCache,
    debug_dir: Path,
) -> tuple[List[Dict[str, Any]], List[Any], float, bool]:
    """Run OCR on a document. Returns pages, ocr_results, duration, cache_hit."""
    path = Path(file_path)
    sha = compute_sha256(file_path)
    product_slug = pre_ocr_inventory(file_path).product_slug

    ocr_service = OCRService(provider=provider, cache=cache)

    start = time.perf_counter()
    pages, ocr_results = extract_pages(file_path, enable_ocr=True)
    duration = time.perf_counter() - start

    # Determine cache hit rate
    cache_dir = OCR_CACHE_DIR / sha
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


def audit_ocr_page(page_result: Any, page_number: int) -> OCRPageAudit:
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
    ocr_results: List[Any],
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
        if re.search(r"\b\d+\s+\d+\b", text) and ":" not in text:
            if re.search(r"\d+:\d+", text) is None:
                suspicious_chunks.append(chunk.get("chunk_id", "unknown"))

    # Table reconstruction check
    tables_count = 0
    for r in ocr_results:
        if "TECHNICAL SPECIFICATIONS" in (r.full_text or "").upper():
            tables_count += 1

    # Determine approval
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
        pages_requiring_review=[a.page_number for a in page_audits if a.low_confidence_lines],
        decisions=decision,
        approval_reason=reason,
        page_audits=page_audits,
    )


async def ingest_approved_document(
    file_path: str,
    pages: List[Dict[str, Any]],
    ocr_results: List[Any],
    product_slug: str,
    debug_dir: Path,
) -> Dict[str, Any]:
    """Ingest an approved catalogue into Qdrant and PostgreSQL."""
    path = Path(file_path)
    document_name = path.name
    sha = compute_sha256(file_path)

    # Build chunks
    tables = extract_tables(file_path)
    document_id = None

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
            document_id = str(__import__("uuid").uuid4())
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

            # Save chunks for debugging
            product_dir = debug_dir / product_slug
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "chunks.json").write_text(
                json.dumps(chunks, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8",
            )

            texts = [c["text"] for c in chunks]
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


async def generate_manifest() -> List[PreOCRInventory]:
    """Generate the Phase 9B manifest of all unprocessed catalogues."""
    manifest = []
    qdrant_total = get_qdrant_point_count()

    # Get existing Qdrant document counts
    from qdrant_client import QdrantClient
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    from collections import Counter
    client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
    points, _ = client.scroll(collection_name=rag_settings.QDRANT_COLLECTION_NAME, limit=10000, with_payload=True)
    doc_counts = Counter(p.payload.get('document_name', '') for p in points if p.payload)

    # Get PostgreSQL status
    postgres_docs = {}
    try:
        async with async_session_factory() as db:
            result = await db.execute(select(RagDocument))
            for doc in result.scalars().all():
                postgres_docs[doc.document_name] = {
                    "status": doc.status,
                    "sha256": doc.sha256,
                    "chunk_count": doc.chunk_count,
                    "product_slug": doc.product_slug,
                }
    except Exception:
        pass

    pdfs = sorted(CATALOGUE_ROOT.glob("*.pdf"))
    for pdf in pdfs:
        filename = pdf.name
        if filename in EXCLUDED_FILES:
            continue
        if filename in INDEXED_FILES:
            continue

        # Skip files that already have a RagDocument entry (already processed)
        if filename in postgres_docs:
            continue

        inv = pre_ocr_inventory(str(pdf), existing_points=doc_counts.get(filename, 0))
        inv.qdrant_existing_points = doc_counts.get(filename, 0)
        inv.action = "OCR_AUDIT"

        manifest.append(inv)

    return manifest


async def process_batch(
    batch_number: int,
    batch_files: List[str],
    provider: PaddleOCRProvider,
    cache: OCRCache,
    debug_dir: Path,
) -> BatchResult:
    """Process a batch of 6 catalogues."""
    warnings: List[str] = []
    approved: List[str] = []
    review_required: List[str] = []
    failed: List[str] = []
    chunks_generated = 0
    chunks_indexed = 0
    qdrant_before = get_qdrant_point_count()
    postgres_before = await get_postgres_document_count()

    for file_path in batch_files:
        filename = Path(file_path).name
        path = Path(file_path)
        print(f"\n  Processing: {filename}")

        try:
            # Step 1: OCR
            pages, ocr_results, duration, cache_hit = run_ocr_on_document(
                file_path, provider, cache, debug_dir
            )
            print(f"    OCR: {len(ocr_results)} pages, {duration:.2f}s, cache_hit={cache_hit}")
            if not ocr_results:
                failed.append(filename)
                warnings.append(f"{filename}: No OCR results")
                continue

            # Step 2: Extract tables
            tables = extract_tables(file_path)

            # Step 3: Get product slug
            product_slug = pre_ocr_inventory(file_path).product_slug

            # Step 4: Generate chunks
            chunks = chunk_catalogue(
                document_name=filename,
                pages=pages,
                tables=tables,
                product_slug=product_slug,
                document_id="audit-doc-id",
                ocr_results=ocr_results,
            )
            print(f"    Chunks: {len(chunks)}")
            chunks_generated += len(chunks)

            # Step 5: Audit
            audit = audit_catalogue(file_path, pages, ocr_results, chunks, product_slug)

            # Save audit
            product_dir = debug_dir / product_slug
            product_dir.mkdir(parents=True, exist_ok=True)
            (product_dir / "audit.json").write_text(
                json.dumps({
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
                }, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            (product_dir / "page_audits.json").write_text(
                json.dumps([asdict(a) for a in audit.page_audits], ensure_ascii=False, indent=2, default=str),
                encoding="utf-8",
            )

            print(f"    Decision: {audit.decisions}")
            print(f"    Reason: {audit.approval_reason}")
            print(f"    Technical IDs: {audit.technical_identifiers[:5]}")
            print(f"    Review pages: {audit.pages_requiring_review}")
            print(f"    Suspicious chunks: {audit.suspicious_chunks[:3]}")

            if audit.decisions == "APPROVED":
                approved.append(filename)
                # Step 6: Ingest
                ing_result = await ingest_approved_document(
                    file_path, pages, ocr_results, product_slug, debug_dir
                )
                print(f"    Ingestion: {ing_result['status']}")
                if ing_result.get("chunks"):
                    chunks_indexed += ing_result["chunks"]
            elif audit.decisions == "OCR_REVIEW_REQUIRED":
                review_required.append(filename)
                # Create a RagDocument entry to track review-required status
                async with async_session_factory() as db:
                    existing = await db.execute(select(RagDocument).where(RagDocument.document_name == filename))
                    existing_doc = existing.scalar_one_or_none()
                    if not existing_doc:
                        existing_doc = RagDocument(
                            document_name=filename,
                            source_type=SOURCE_TYPE_CATALOGUE,
                            storage_path=str(path.resolve()),
                            sha256=compute_sha256(file_path),
                            status="review_required",
                            product_slug=product_slug,
                        )
                        db.add(existing_doc)
                        await db.commit()
            else:
                failed.append(filename)
                # Create failed RagDocument entry
                async with async_session_factory() as db:
                    existing = await db.execute(select(RagDocument).where(RagDocument.document_name == filename))
                    existing_doc = existing.scalar_one_or_none()
                    if not existing_doc:
                        existing_doc = RagDocument(
                            document_name=filename,
                            source_type=SOURCE_TYPE_CATALOGUE,
                            storage_path=str(path.resolve()),
                            sha256=compute_sha256(file_path),
                            status=STATUS_FAILED,
                            product_slug=product_slug,
                            last_error=audit.approval_reason,
                        )
                        db.add(existing_doc)
                        await db.commit()

        except Exception as exc:
            print(f"    FAILED: {exc}")
            traceback.print_exc()
            failed.append(filename)
            warnings.append(f"{filename}: {exc}")

    qdrant_after = get_qdrant_point_count()
    postgres_after = await get_postgres_document_count()

    return BatchResult(
        batch_number=batch_number,
        files_processed=[Path(f).name for f in batch_files],
        approved=approved,
        review_required=review_required,
        failed=failed,
        chunks_generated=chunks_generated,
        chunks_indexed=chunks_indexed,
        qdrant_before=qdrant_before,
        qdrant_after=qdrant_after,
        postgres_before=postgres_before,
        postgres_after=postgres_after,
        warnings=warnings,
    )


def generate_product_aliases(approved_files: List[str]) -> Dict[str, List[str]]:
    """Generate conservative aliases for approved products."""
    new_aliases = {}
    for filename in approved_files:
        raw_name = Path(filename).stem
        slug = get_canonical_slug(raw_name)
        if not slug:
            slug = raw_name.lower().replace(" ", "-").replace("_", "-")
            slug = re.sub(r"[^a-z0-9-]", "", slug)
            slug = re.sub(r"-+", "-", slug).strip("-")

        # Conservative aliases based on filename
        aliases = [slug, slug.replace("-", " ")]
        if "pump" in raw_name.lower():
            aliases.append(f"{slug} pump")
        elif "gun" in raw_name.lower():
            aliases.append(f"{slug} gun")
        elif "press" in raw_name.lower():
            aliases.append(f"{slug} press")

        new_aliases[slug] = list(set(aliases))

    return new_aliases


async def main():
    print("=" * 60)
    print("PHASE 9B — BULK OCR PIPELINE VALIDATION AND INGESTION")
    print("=" * 60)

    DEBUG_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize OCR provider and cache
    provider = PaddleOCRProvider(lang="en", use_gpu=False)
    cache = OCRCache(base_dir=str(OCR_CACHE_DIR))

    # Step 1: Generate manifest
    print("\n[STEP 1] GENERATING PHASE 9B MANIFEST")
    manifest = await generate_manifest()

    # Save manifest
    manifest_data = []
    for inv in manifest:
        manifest_data.append({
            "filename": inv.filename,
            "sha256": inv.sha256,
            "page_count": inv.page_count,
            "alpha_chars_per_page": inv.alpha_chars_per_page,
            "product_guess": inv.product_guess,
            "ocr_cache_exists": inv.ocr_cache_exists,
            "qdrant_existing_points": inv.qdrant_existing_points,
            "product_slug": inv.product_slug,
            "action": inv.action,
        })
    (DEBUG_DIR / "phase9b_manifest.json").write_text(
        json.dumps(manifest_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nTotal unprocessed catalogues: {len(manifest)}")
    for inv in manifest:
        print(f"  {inv.filename}: pages={inv.page_count}, sha256={inv.sha256[:16]}..., "
              f"slug={inv.product_slug}, cached={inv.ocr_cache_exists}, action={inv.action}")

    # Step 2: Process in batches
    print("\n[STEP 2] PROCESSING IN BATCHES")
    batch_size = 6
    batches = [manifest[i:i + batch_size] for i in range(0, len(manifest), batch_size)]
    print(f"Batches: {len(batches)} x ~{batch_size} documents")

    all_approved = []
    all_review_required = []
    all_failed = []
    batch_results = []

    for batch_idx, batch_inv in enumerate(batches, start=1):
        print(f"\n{'=' * 60}")
        print(f"BATCH {batch_idx}")
        print(f"{'=' * 60}")

        batch_files = [str(CATALOGUE_ROOT / inv.filename) for inv in batch_inv]
        result = await process_batch(
            batch_number=batch_idx,
            batch_files=batch_files,
            provider=provider,
            cache=cache,
            debug_dir=DEBUG_DIR,
        )
        batch_results.append(result)

        all_approved.extend(result.approved)
        all_review_required.extend(result.review_required)
        all_failed.extend(result.failed)

        # Print batch report
        print(f"\n  BATCH {batch_idx} REPORT")
        print(f"  Files: {', '.join(result.files_processed)}")
        print(f"  Approved: {result.approved}")
        print(f"  Review required: {result.review_required}")
        print(f"  Failed: {result.failed}")
        print(f"  Chunks: generated={result.chunks_generated} / indexed={result.chunks_indexed}")
        print(f"  Qdrant: {result.qdrant_before} -> {result.qdrant_after} ({result.qdrant_after - result.qdrant_before:+d})")
        print(f"  PostgreSQL: {result.postgres_before} -> {result.postgres_after} ({result.postgres_after - result.postgres_before:+d})")
        if result.warnings:
            print(f"  Warnings: {result.warnings}")

    # Step 3: Generate aliases
    print("\n[STEP 3] PRODUCT ALIASES")
    new_aliases = generate_product_aliases(all_approved)
    for slug, aliases in new_aliases.items():
        print(f"  {slug}: {aliases}")

    (DEBUG_DIR / "new_aliases.json").write_text(
        json.dumps(new_aliases, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Step 4: Idempotency test
    print("\n[STEP 4] IDEMPOTENCY TEST")
    print("  Re-running manifest generation...")
    manifest2 = generate_manifest()
    unchanged_count = sum(1 for inv in manifest2 if inv.action == "SKIP_UNCHANGED")
    print(f"  Unchanged files on second run: {unchanged_count}")

    # Step 5: Final report
    print("\n[STEP 5] FINAL REPORT")
    print(f"  Total approved: {len(all_approved)}")
    print(f"  Total review required: {len(all_review_required)}")
    print(f"  Total failed: {len(all_failed)}")
    print(f"  Total chunks generated: {sum(r.chunks_generated for r in batch_results)}")
    print(f"  Total chunks indexed: {sum(r.chunks_indexed for r in batch_results)}")

    # Save final report
    final_report = {
        "manifest": manifest_data,
        "batches": [asdict(r) for r in batch_results],
        "approved": all_approved,
        "review_required": all_review_required,
        "failed": all_failed,
        "new_aliases": new_aliases,
        "idempotency": {"unchanged_on_rerun": unchanged_count},
    }
    (DEBUG_DIR / "phase9b_final_report.json").write_text(
        json.dumps(final_report, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("PHASE 9B BULK PROCESSING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
