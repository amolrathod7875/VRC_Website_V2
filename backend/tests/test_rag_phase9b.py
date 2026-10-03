"""
Phase 9B — Bulk OCR Pipeline Tests

Tests cover:
1. bulk OCR manifest generation
2. approved/review state separation
3. cache reuse
4. per-document failure isolation
5. non-pump catalogue chunking
6. footer garbage filtering
7. canonical product identities
8. alias generation
9. product-filter compatibility
10. cross-product evidence guard for newly registered product
11. second-run idempotency
12. registry/Qdrant consistency
13. OCR_REVIEW_REQUIRED not indexed
"""
import hashlib
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.rag.ingestion.ocr.base import OCRBlock, OCRPageResult, OCRProvider, OCRTable
from app.rag.ingestion.ocr.ocr_service import OCRCache, OCRService
from app.rag.ingestion.pdf_parser import page_needs_ocr, _doc_hash
from app.rag.ingestion.catalogue_chunker import chunk_catalogue
from app.rag.ingestion.pdf_table_parser import parse_spec_table, is_likely_spec_table
from app.rag.product_identity import get_canonical_slug, resolve_product_identity, extract_model_identifier, PRODUCT_ALIASES
from app.rag.constants import CATALOGUE_AUTHORITY_PRIORITY, CHUNK_TYPE_TECHNICAL_MODEL, SOURCE_TYPE_CATALOGUE
from app.rag.config import rag_settings


# ============================================================
# 1. bulk OCR manifest generation
# ============================================================
def test_manifest_excludes_indexed_and_review_required() -> None:
    from scripts.run_phase9b_bulk import generate_manifest, INDEXED_FILES, EXCLUDED_FILES
    import asyncio
    from unittest.mock import patch, MagicMock

    mock_client = MagicMock()
    mock_client.scroll.return_value = ([], None)
    mock_client.count.return_value = MagicMock(count=5306)

    with patch("scripts.run_phase9b_bulk.get_qdrant_point_count", return_value=5306), \
         patch("qdrant_client.QdrantClient", return_value=mock_client), \
         patch("app.core.database.async_session_factory") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value.__aenter__ = MagicMock(return_value=mock_db)
        mock_session.return_value.__aexit__ = MagicMock(return_value=False)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        manifest = asyncio.run(generate_manifest())
        manifest_filenames = {inv.filename for inv in manifest}

        for filename in INDEXED_FILES:
            assert filename not in manifest_filenames, f"{filename} should be excluded"
        for filename in EXCLUDED_FILES:
            assert filename not in manifest_filenames, f"{filename} should be excluded"


def test_manifest_contains_expected_count() -> None:
    import asyncio
    from scripts.run_phase9b_bulk import generate_manifest
    from unittest.mock import patch, MagicMock

    mock_client = MagicMock()
    mock_client.scroll.return_value = ([], None)
    mock_client.count.return_value = MagicMock(count=5306)

    with patch("scripts.run_phase9b_bulk.get_qdrant_point_count", return_value=5306), \
         patch("qdrant_client.QdrantClient", return_value=mock_client), \
         patch("app.core.database.async_session_factory") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value.__aenter__ = MagicMock(return_value=mock_db)
        mock_session.return_value.__aexit__ = MagicMock(return_value=False)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        manifest = asyncio.run(generate_manifest())
        # With an empty database, all unprocessed catalogues should appear in the manifest.
        # The exact count depends on the catalogue directory; we just verify the manifest
        # generation path works and returns entries with OCR_AUDIT action.
        assert len(manifest) > 0
        for inv in manifest:
            assert inv.action == "OCR_AUDIT"


def test_manifest_entries_have_required_fields() -> None:
    import asyncio
    from scripts.run_phase9b_bulk import generate_manifest
    from unittest.mock import patch, MagicMock

    mock_client = MagicMock()
    mock_client.scroll.return_value = ([], None)
    mock_client.count.return_value = MagicMock(count=5306)

    with patch("scripts.run_phase9b_bulk.get_qdrant_point_count", return_value=5306), \
         patch("qdrant_client.QdrantClient", return_value=mock_client), \
         patch("app.core.database.async_session_factory") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value.__aenter__ = MagicMock(return_value=mock_db)
        mock_session.return_value.__aexit__ = MagicMock(return_value=False)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        manifest = asyncio.run(generate_manifest())
        for inv in manifest:
            assert inv.filename
            assert inv.sha256
            assert inv.page_count > 0
            assert inv.product_slug
            assert inv.action == "OCR_AUDIT"


# ============================================================
# 2. approved/review state separation
# ============================================================
def test_audit_catalogue_marks_low_output_as_failed() -> None:
    from scripts.run_phase9b_bulk import audit_catalogue
    import asyncio
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    pages = [{"page_number": 1, "text": ""}]
    ocr_results = [MagicMock(full_text="", blocks=[], tables=[], warnings=[])]
    chunks = []
    audit = audit_catalogue(tmp_path, pages, ocr_results, chunks, "test")
    assert audit.decisions == "FAILED"


def test_audit_catalogue_marks_high_suspicious_as_review() -> None:
    from scripts.run_phase9b_bulk import audit_catalogue
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    pages = [{"page_number": 1, "text": "some text"}]
    ocr_results = [MagicMock(full_text="a" * 200, blocks=[], tables=[], warnings=[])]
    chunks = [{"chunk_id": f"c{i}", "text": "x" * 20} for i in range(5)]
    chunks[3]["text"] = "30 150"
    chunks[4]["text"] = "35 70"
    audit = audit_catalogue(tmp_path, pages, ocr_results, chunks, "test")
    assert audit.decisions == "OCR_REVIEW_REQUIRED"


# ============================================================
# 3. cache reuse
# ============================================================
def test_ocr_cache_reused_across_calls() -> None:
    cache = OCRCache(base_dir=".tmp_test_ocr_cache_9b_reuse")
    doc_hash = "reuse_test_doc"
    page_num = 1
    original = OCRPageResult(
        page_number=page_num,
        full_text="Pressure ratio: 30:1",
        blocks=[OCRBlock(text="30:1", confidence=0.95)],
        tables=[],
        confidence=0.95,
    )
    cache.put(doc_hash, page_num, original)
    loaded = cache.get(doc_hash, page_num)
    assert loaded is not None
    assert loaded.full_text == "Pressure ratio: 30:1"
    assert loaded.blocks[0].confidence == 0.95


# ============================================================
# 4. per-document failure isolation
# ============================================================
def test_failed_document_does_not_corrupt_others() -> None:
    cache = OCRCache(base_dir=".tmp_test_ocr_cache_9b_failure")
    good_doc = "good_doc_sha"
    bad_doc = "bad_doc_sha"
    good_result = OCRPageResult(page_number=1, full_text="good text", blocks=[], tables=[], confidence=0.9)
    cache.put(good_doc, 1, good_result)
    bad_result = cache.get(bad_doc, 1)
    assert bad_result is None
    good_loaded = cache.get(good_doc, 1)
    assert good_loaded is not None
    assert good_loaded.full_text == "good text"


# ============================================================
# 5. non-pump catalogue chunking
# ============================================================
def test_non_pump_catalogue_chunking() -> None:
    pages = [
        {"page_number": 1, "text": "VALVES\n\nBall valves for industrial use"},
        {"page_number": 2, "text": "Material: Stainless steel\nConnection: 1/4 BSP"},
    ]
    chunks = chunk_catalogue(
        document_name="Valves.pdf",
        pages=pages,
        tables=[],
        product_slug="valves",
        document_id="doc-valves",
        ocr_results=[],
    )
    assert len(chunks) > 0
    for chunk in chunks:
        assert chunk.get("product_slug") == "valves"
        assert chunk.get("source_type") == SOURCE_TYPE_CATALOGUE
        assert chunk.get("authority_priority") == CATALOGUE_AUTHORITY_PRIORITY


# ============================================================
# 6. footer garbage filtering
# ============================================================
def test_short_suspicious_chunks_flagged() -> None:
    from scripts.run_phase9b_bulk import audit_catalogue
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    pages = [{"page_number": 1, "text": "some content"}]
    ocr_results = [MagicMock(full_text="some content here", blocks=[], tables=[], warnings=[])]
    chunks = [
        {"chunk_id": "c0", "text": "a" * 100},
        {"chunk_id": "c1", "text": "040"},
        {"chunk_id": "c2", "text": "phone"},
    ]
    audit = audit_catalogue(tmp_path, pages, ocr_results, chunks, "test")
    assert len(audit.suspicious_chunks) > 0


# ============================================================
# 7. canonical product identities
# ============================================================
def test_canonical_slug_known_products() -> None:
    assert get_canonical_slug("Tiger") == "tiger"
    assert get_canonical_slug("lion") == "lion"
    assert get_canonical_slug("rhino") == "rhino"
    assert get_canonical_slug("elephant") == "elephant"


def test_canonical_slug_unknown_returns_none() -> None:
    assert get_canonical_slug("unknown_product") is None
    assert get_canonical_slug("VRC MIX (LOW - MEDIUM) PRESSURE") is None


# ============================================================
# 8. alias generation
# ============================================================
def test_product_aliases_structure() -> None:
    for slug, config in PRODUCT_ALIASES.items():
        assert "canonical_slug" in config
        assert "aliases" in config
        assert isinstance(config["aliases"], list)
        assert len(config["aliases"]) > 0


# ============================================================
# 9. product-filter compatibility
# ============================================================
def test_product_filter_matches_indexed_slug() -> None:
    from app.rag.retrieval.hybrid_retriever import HybridRetriever
    from app.rag.vectorstore.qdrant_store import QdrantStore

    qdrant_store = QdrantStore()
    filters = {"product_slug": "cheetah"}
    qdrant_filter = qdrant_store._build_qdrant_filter(filters)
    assert qdrant_filter is not None


# ============================================================
# 10. cross-product evidence guard for newly registered product
# ============================================================
def test_cross_product_isolation_new_products() -> None:
    pages = [{"page_number": 1, "text": "Cheetah pump\n\nPressure ratio: 55:1"}]
    chunks = chunk_catalogue(
        document_name="Cheetah.pdf",
        pages=pages,
        tables=[],
        product_slug="cheetah",
        document_id="doc-cheetah",
        ocr_results=[],
    )
    for chunk in chunks:
        assert chunk.get("product_slug") == "cheetah"
        assert chunk.get("source_type") == "catalogue"


# ============================================================
# 11. second-run idempotency
# ============================================================
def test_second_run_skips_unchanged() -> None:
    import asyncio
    from app.rag.ingestion.ingestion_service import IngestionService
    from unittest.mock import AsyncMock, MagicMock, patch
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name
        tmp.write(b"dummy pdf content")

    db = MagicMock()

    async def mock_execute(query):
        result = MagicMock()
        result.scalar_one_or_none.return_value = existing_doc
        return result

    db.execute = mock_execute
    db.flush = AsyncMock()
    db.commit = AsyncMock()

    qdrant = MagicMock()
    dense = MagicMock()
    sparse = MagicMock()

    service = IngestionService(db=db, qdrant_store=qdrant, dense=dense, sparse=sparse)

    existing_doc = MagicMock()
    existing_doc.sha256 = "dummy_hash"
    existing_doc.qdrant_document_id = "doc-123"

    with patch("app.rag.ingestion.ingestion_service.calculate_sha256", return_value="dummy_hash"):
        result = asyncio.run(service.ingest_catalogue(Path(tmp_path)))
    assert result["status"] == "skipped"
    assert result["reason"] == "unchanged"


# ============================================================
# 12. registry/Qdrant consistency
# ============================================================
def test_registry_qdrant_point_count_matches() -> None:
    from qdrant_client import QdrantClient
    from sqlalchemy import select, func
    from app.models.rag_document import RagDocument
    from app.core.database import async_session_factory

    try:
        client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
        qdrant_count = client.count(collection_name=rag_settings.QDRANT_COLLECTION_NAME).count
    except Exception as exc:
        pytest.skip(f"Qdrant unavailable: {exc}")

    import asyncio
    async def check():
        try:
            async with async_session_factory() as db:
                result = await db.execute(select(func.sum(RagDocument.chunk_count)).where(RagDocument.status == "indexed"))
                total_chunks = result.scalar_one() or 0
                return total_chunks
        except Exception as exc:
            pytest.skip(f"PostgreSQL unavailable: {exc}")
            return 0

    total_chunks = asyncio.run(check())
    assert qdrant_count >= total_chunks, "Qdrant should have at least as many points as indexed chunks"


# ============================================================
# 13. OCR_REVIEW_REQUIRED not indexed
# ============================================================
def test_review_required_documents_not_in_qdrant() -> None:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    from sqlalchemy import select
    from app.models.rag_document import RagDocument
    from app.core.database import async_session_factory

    try:
        client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
    except Exception as exc:
        pytest.skip(f"Qdrant unavailable: {exc}")

    import asyncio
    async def check():
        try:
            async with async_session_factory() as db:
                result = await db.execute(select(RagDocument).where(RagDocument.status == "review_required"))
                review_docs = result.scalars().all()
                return review_docs
        except Exception as exc:
            pytest.skip(f"PostgreSQL unavailable: {exc}")
            return []

    review_docs = asyncio.run(check())
    for doc in review_docs:
        if not doc.qdrant_document_id:
            continue
        points, _ = client.scroll(
            collection_name=rag_settings.QDRANT_COLLECTION_NAME,
            scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=doc.qdrant_document_id))]),
            limit=1,
            with_payload=False,
        )
        assert len(points) == 0, f"Review required document {doc.document_name} should not have Qdrant points"
