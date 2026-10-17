"""Ingestion change-safety test suite.

Tests the IngestionService against an isolated fake Qdrant store to verify
that changed-document ingestion is safe: old known-good points must remain
available or be restorable when any step in the pipeline fails.

Never tests destructive failure injection against the production collection.
"""
from __future__ import annotations

import asyncio
import copy
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest
from unittest.mock import patch, MagicMock

from app.rag.utils.ids import generate_document_id_for, stable_point_id
from app.rag.constants import SOURCE_TYPE_CATALOGUE, SOURCE_TYPE_COMPANY_MASTER
from app.rag.utils.hashing import calculate_sha256


@pytest.fixture
def mock_pipeline(monkeypatch):
    """Mock file I/O, PDF parsing, and OCR to avoid needing real files."""
    fake_sha = "new_sha_def456"
    monkeypatch.setattr(
        "app.rag.ingestion.ingestion_service.calculate_sha256",
        lambda file_path: fake_sha,
    )
    monkeypatch.setattr(
        "app.rag.ingestion.ingestion_service.extract_pages",
        lambda file_path, enable_ocr=True: (
            [{"page_number": 1, "text": "Fake page text for testing"}],
            [],
        ),
    )
    monkeypatch.setattr(
        "app.rag.ingestion.ingestion_service.extract_tables",
        lambda file_path, enable_ocr=True: [],
    )
    return fake_sha


class FakeQdrantClient:
    """In-memory Qdrant client that records all operations and supports failure injection."""

    def __init__(
        self,
        points: Optional[Dict[str, Dict[str, Any]]] = None,
        fail_on: Optional[str] = None,
    ):
        # points: { point_id: payload }
        self.points: Dict[str, Dict[str, Any]] = dict(points or {})
        self.fail_on = fail_on
        self.upsert_calls: List[Tuple[int, List]] = []
        self.delete_calls: List[Tuple[int, List]] = []
        self.scroll_calls = 0
        self.upsert_call_count = 0
        self.delete_call_count = 0

    def _check_fail(self, operation: str):
        if self.fail_on == operation:
            raise RuntimeError(f"Injected failure: {operation}")

    def scroll(
        self,
        collection_name: str,
        scroll_filter=None,
        limit: int = 100,
        with_payload: bool = True,
        with_vectors: bool = False,
        offset=None,
    ) -> Tuple[List[Any], Optional[Any]]:
        self._check_fail("scroll")
        self.scroll_calls += 1
        filter_field = None
        filter_value = None
        if scroll_filter and hasattr(scroll_filter, "must") and scroll_filter.must:
            condition = scroll_filter.must[0]
            filter_field = condition.key
            filter_value = condition.match.value

        matching_ids = list(self.points.keys())
        if filter_field and filter_value:
            filtered = []
            for pid, payload in self.points.items():
                if payload.get(filter_field) == filter_value:
                    filtered.append(pid)
            matching_ids = filtered

        # Paginate
        if offset:
            start = matching_ids.index(offset) + 1 if offset in matching_ids else 0
        else:
            start = 0

        page = matching_ids[start:start + limit]
        next_offset = None
        if start + limit < len(matching_ids):
            next_offset = page[-1] if page else None

        class FakePoint:
            def __init__(self, pid, payload, vectors=None):
                self.id = pid
                self.payload = payload
                self.vector = {}
                self.score = 0.0
                self.version = 1

        results = [FakePoint(pid, payload) for pid, payload in [(p, self.points[p]) for p in page]]
        return results, next_offset

    def upsert(self, collection_name: str, points: List) -> None:
        self._check_fail("upsert")
        self.upsert_call_count += 1
        self.upsert_calls.append((collection_name, copy.deepcopy(points)))
        for pt in points:
            pid = str(pt["id"])
            self.points[pid] = dict(pt.get("payload", {}))

    def delete(self, collection_name: str, points_selector):
        self._check_fail("delete")
        self.delete_call_count += 1
        if isinstance(points_selector, list):
            deleted_ids = [str(p) for p in points_selector]
        else:
            # Filter-based delete: scan and match
            if hasattr(points_selector, "must") and points_selector.must:
                condition = points_selector.must[0]
                field = condition.key
                value = condition.match.value
                deleted_ids = [
                    pid for pid, payload in list(self.points.items())
                    if payload.get(field) == value
                ]
            else:
                deleted_ids = []
        self.delete_calls.append((collection_name, deleted_ids))
        for pid in deleted_ids:
            self.points.pop(pid, None)

    def get_collections(self):
        class FakeInfo:
            collections = []
        return FakeInfo()

    def get_collection(self, collection_name: str):
        class FakeCol:
            points_count = len(self.points)
            config = None
            payload_schema = {}
        return FakeCol()


class FakeQdrantStore:
    """Wraps FakeQdrantClient to mimic QdrantStore's interface."""

    def __init__(self, client: Optional[FakeQdrantClient] = None, fail_on: Optional[str] = None):
        self.client = client or FakeQdrantClient(fail_on=fail_on)
        self.collection_name = "test_collection"

    async def ensure_collection(self) -> None:
        pass

    async def upsert_points(
        self,
        document_id: str,
        dense_vectors: List[List[float]],
        sparse_vectors: List[Dict[str, Any]],
        payloads: List[Dict[str, Any]],
    ) -> None:
        batch_size = 64
        for start in range(0, len(payloads), batch_size):
            batch_payloads = payloads[start:start + batch_size]
            batch_dense = dense_vectors[start:start + batch_size]
            batch_sparse = sparse_vectors[start:start + batch_size]
            points = []
            for idx, payload in enumerate(batch_payloads):
                sparse = batch_sparse[idx]
                from qdrant_client.models import SparseVector
                point_id = stable_point_id(document_id, str(payload.get("chunk_id", idx)))
                points.append({
                    "id": point_id,
                    "vector": {
                        "dense": batch_dense[idx],
                        "sparse": SparseVector(indices=sparse.get("indices", []), values=sparse.get("values", [])),
                    },
                    "payload": payload,
                })
            self.client.upsert(collection_name=self.collection_name, points=points)


class FakeDocumentRegistry:
    """Minimal registry backed by FakeQdrantClient, supports delete-by-name."""

    def __init__(self, qdrant_store: FakeQdrantStore):
        self.qdrant_store = qdrant_store

    def get_document_state_by_name(self, document_name: str) -> Optional[Dict[str, Any]]:
        points = self._scroll_by_document_name(document_name)
        if not points:
            return None
        payload = points[0].payload or {}
        return {
            "document_id": payload.get("document_id"),
            "document_name": payload.get("document_name"),
            "source_type": payload.get("source_type"),
            "product_slug": payload.get("product_slug"),
            "product_slugs": payload.get("product_slugs"),
            "parent_product_slug": payload.get("parent_product_slug"),
            "sha256": payload.get("sha256") or payload.get("source_hash"),
            "storage_path": payload.get("storage_path"),
            "chunk_count": len(points),
        }

    def _scroll_by_document_name(self, document_name: str) -> List[Any]:
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        points = []
        offset = None
        while True:
            batch, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                scroll_filter=Filter(must=[FieldCondition(key="document_name", match=MatchValue(value=document_name))]),
                limit=200,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            points.extend(batch)
            if not offset:
                break
        return points

    def delete_document_points(self, document_id: str) -> int:
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        points = []
        offset = None
        while True:
            batch, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                scroll_filter=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]),
                limit=200,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            points.extend(batch)
            if not offset:
                break
        if not points:
            return 0
        point_ids = [p.id for p in points]
        self.qdrant_store.client.delete(
            collection_name=self.qdrant_store.collection_name,
            points_selector=point_ids,
        )
        return len(point_ids)

    def delete_document_points_by_name(self, document_name: str) -> int:
        """Delete all points matching document_name (safe across old/new doc IDs)."""
        points = self._scroll_by_document_name(document_name)
        if not points:
            return 0
        point_ids = [p.id for p in points]
        self.qdrant_store.client.delete(
            collection_name=self.qdrant_store.collection_name,
            points_selector=point_ids,
        )
        return len(point_ids)

    def list_indexed_documents(self) -> List[Dict[str, Any]]:
        documents: Dict[str, Dict[str, Any]] = {}
        offset = None
        while True:
            points, offset = self.qdrant_store.client.scroll(
                collection_name=self.qdrant_store.collection_name,
                limit=200,
                with_payload=True,
                with_vectors=False,
                offset=offset,
            )
            for point in points:
                payload = point.payload or {}
                doc_id = payload.get("document_id") or payload.get("document_name")
                if not doc_id:
                    continue
                if doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "document_name": payload.get("document_name"),
                        "source_type": payload.get("source_type"),
                        "product_slug": payload.get("product_slug"),
                        "sha256": payload.get("sha256") or payload.get("source_hash"),
                        "chunk_count": 0,
                    }
                documents[doc_id]["chunk_count"] = documents[doc_id].get("chunk_count", 0) + 1
            if not offset:
                break
        return list(documents.values())

    @staticmethod
    def create(qdrant_store=None) -> "FakeDocumentRegistry":
        return FakeDocumentRegistry(qdrant_store=qdrant_store)


class FakeDenseEmbeddingService:
    def __init__(self, dim: int = 384):
        self.dimension = dim
        self._call_count = 0

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        self._call_count += 1
        return [[float(i + 1) for i in range(self.dimension)] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return [float(i + 1) for i in range(self.dimension)]


class FakeSparseEmbeddingService:
    def __init__(self):
        self._call_count = 0

    def embed_documents(self, texts: List[str]) -> List[Dict[str, Any]]:
        self._call_count += 1
        return [{"indices": [0], "values": [1.0]} for _ in texts]

    def embed_query(self, text: str) -> Dict[str, Any]:
        return {"indices": [0], "values": [1.0]}


# ---------------------------------------------------------------------------
# Helpers to build seeded old points
# ---------------------------------------------------------------------------

def _seed_catalogue_points(
    document_name: str,
    document_id: str,
    num_chunks: int = 5,
    sha256: str = "old_sha_abc123",
) -> Dict[str, Dict[str, Any]]:
    """Create old-style points with a given document_id (simulating pre-existing data)."""
    points = {}
    for i in range(num_chunks):
        chunk_id = f"{document_id}::chunk::{i}"
        point_id = stable_point_id(document_id, chunk_id)
        points[point_id] = {
            "document_id": document_id,
            "document_name": document_name,
            "source_type": SOURCE_TYPE_CATALOGUE,
            "chunk_id": chunk_id,
            "product_slug": "tiger",
            "sha256": sha256,
            "text": f"Old chunk {i} content",
            "model": "30:150",
        }
    return points


# ---------------------------------------------------------------------------
# Test: A. Embedding preparation fails
# ---------------------------------------------------------------------------

def test_failure_a_embedding_fails_preserves_old_points(mock_pipeline):
    """When embedding preparation fails, old known-good points must remain."""
    doc_name = "Tiger.pdf"
    document_id = generate_document_id_for(doc_name, SOURCE_TYPE_CATALOGUE)
    old_points = _seed_catalogue_points(doc_name, document_id, num_chunks=5)
    client = FakeQdrantClient(points=old_points, fail_on="upsert")
    store = FakeQdrantStore(client=client)
    registry = FakeDocumentRegistry(qdrant_store=store)

    from app.rag.ingestion.ingestion_service import IngestionService
    service = IngestionService(
        qdrant_store=store,
        dense=FakeDenseEmbeddingService(),
        sparse=FakeSparseEmbeddingService(),
        document_registry=registry,
    )

    # Monkey-patch the pipeline steps to simulate embedding failure mid-way
    original_embed = FakeDenseEmbeddingService.embed_documents

    def fail_embedding(self, texts):
        raise RuntimeError("Embedding service unavailable")

    FakeDenseEmbeddingService.embed_documents = fail_embedding
    try:
        result = asyncio.run(service.ingest_catalogue(Path("Tiger.pdf")))
    finally:
        FakeDenseEmbeddingService.embed_documents = original_embed

    assert result["status"] == "failed"
    # Old points must still be present
    remaining = registry.list_indexed_documents()
    tiger_docs = [d for d in remaining if d.get("document_name") == doc_name]
    assert len(tiger_docs) == 1, "Old document points were lost!"
    assert tiger_docs[0]["chunk_count"] == 5, "Old chunk count changed!"


# ---------------------------------------------------------------------------
# Test: B. Payload construction fails
# ---------------------------------------------------------------------------

def test_failure_b_payload_construction_fails_preserves_old_points(mock_pipeline):
    """When payload construction fails, old known-good points must remain."""
    doc_name = "Tiger.pdf"
    document_id = generate_document_id_for(doc_name, SOURCE_TYPE_CATALOGUE)
    old_points = _seed_catalogue_points(doc_name, document_id, num_chunks=5)
    client = FakeQdrantClient(points=old_points)
    store = FakeQdrantStore(client=client)
    registry = FakeDocumentRegistry(qdrant_store=store)

    from app.rag.ingestion.ingestion_service import IngestionService
    service = IngestionService(
        qdrant_store=store,
        dense=FakeDenseEmbeddingService(),
        sparse=FakeSparseEmbeddingService(),
        document_registry=registry,
    )

    # Monkey-patch build_catalogue_metadata to fail
    import app.rag.ingestion.ingestion_service as ingestion_mod
    original_build = ingestion_mod.build_catalogue_metadata

    def fail_build(*args, **kwargs):
        raise RuntimeError("Payload construction failed")

    ingestion_mod.build_catalogue_metadata = fail_build
    try:
        result = asyncio.run(service.ingest_catalogue(Path("Tiger.pdf")))
    finally:
        ingestion_mod.build_catalogue_metadata = original_build

    assert result["status"] == "failed"
    remaining = registry.list_indexed_documents()
    tiger_docs = [d for d in remaining if d.get("document_name") == doc_name]
    assert len(tiger_docs) == 1, "Old document points were lost!"
    assert tiger_docs[0]["chunk_count"] == 5, "Old chunk count changed!"


# ---------------------------------------------------------------------------
# Test: C. Deleting old points fails
# ---------------------------------------------------------------------------

def test_failure_c_delete_fails_preserves_old_points(mock_pipeline):
    """When deletion fails, the ingest should abort without uploading new points."""
    doc_name = "Tiger.pdf"
    document_id = generate_document_id_for(doc_name, SOURCE_TYPE_CATALOGUE)
    old_doc_id = str(uuid.uuid4())  # Random, simulating production old points
    old_points = _seed_catalogue_points(doc_name, old_doc_id, num_chunks=5, sha256="old_sha_abc123")
    client = FakeQdrantClient(points=old_points, fail_on="delete")
    store = FakeQdrantStore(client=client)
    registry = FakeDocumentRegistry(qdrant_store=store)

    from app.rag.ingestion.ingestion_service import IngestionService
    service = IngestionService(
        qdrant_store=store,
        dense=FakeDenseEmbeddingService(),
        sparse=FakeSparseEmbeddingService(),
        document_registry=registry,
    )

    # Old points have sha256="old_sha_abc123", new file has "new_sha_def456" (from mock)
    # This triggers the "changed" path which will attempt deletion
    result = asyncio.run(service.ingest_catalogue(Path("Tiger.pdf")))

    assert result["status"] == "failed"
    # Old points should still be present (delete failed, so old points survive)
    remaining = registry.list_indexed_documents()
    tiger_docs = [d for d in remaining if d.get("document_name") == doc_name]
    assert len(tiger_docs) >= 1, "Old document points were lost!"
    # The old document (with random doc_id) must still be present
    old_docs = [d for d in tiger_docs if d.get("document_id") == old_doc_id]
    assert len(old_docs) == 1, "Old document points (random doc_id) were lost!"
    assert old_docs[0]["chunk_count"] == 5, "Old chunk count changed!"


# ---------------------------------------------------------------------------
# Test: D. Uploading new points fails AFTER old-point deletion
# ---------------------------------------------------------------------------

def test_failure_d_upload_after_delete_preserves_old_or_restores(mock_pipeline):
    """If upload fails after old-point deletion, old data must be restorable.

With the fixed implementation (upload-first-then-delete), old points are
preserved even when upload fails, because deletion happens only after
successful upload.
"""
    doc_name = "Tiger.pdf"
    old_doc_id = str(uuid.uuid4())  # Random, simulating production old points
    old_points = _seed_catalogue_points(doc_name, old_doc_id, num_chunks=5, sha256="old_sha_abc123")

    client = FakeQdrantClient(points=old_points, fail_on="upsert")
    store = FakeQdrantStore(client=client)
    registry = FakeDocumentRegistry(qdrant_store=store)

    from app.rag.ingestion.ingestion_service import IngestionService

    service = IngestionService(
        qdrant_store=store,
        dense=FakeDenseEmbeddingService(),
        sparse=FakeSparseEmbeddingService(),
        document_registry=registry,
    )

    result = asyncio.run(service.ingest_catalogue(Path("Tiger.pdf")))
    assert result["status"] == "failed"

    # Check: with fixed ordering (upload-first), old points survive even if upload fails
    remaining = registry.list_indexed_documents()
    tiger_docs = [d for d in remaining if d.get("document_name") == doc_name]

    if len(tiger_docs) == 0:
        print("DATA LOSS CONFIRMED: Old points were lost during failed ingestion")
        pytest.fail(
            "Data loss bug: IngestionService lost old points during failed ingestion. "
            "Old points must be preserved when upload fails."
        )
    elif len(tiger_docs) == 1:
        print("SAFE: Old points preserved despite upload failure")
        assert tiger_docs[0]["chunk_count"] == 5


# ---------------------------------------------------------------------------
# Test: E. Partial Qdrant upload
# ---------------------------------------------------------------------------

def test_failure_e_partial_upload_preserves_old_points(mock_pipeline):
    """If only some batches upload successfully, old points must remain intact."""
    doc_name = "Tiger.pdf"
    old_doc_id = str(uuid.uuid4())  # Random, simulating production old points
    old_points = _seed_catalogue_points(doc_name, old_doc_id, num_chunks=5, sha256="old_sha_abc123")
    client = FakeQdrantClient(points=old_points)
    store = FakeQdrantStore(client=client)
    registry = FakeDocumentRegistry(qdrant_store=store)

    from app.rag.ingestion.ingestion_service import IngestionService

    call_count = [0]
    original_upsert = client.upsert

    def partial_fail(collection_name, points):
        call_count[0] += 1
        if call_count[0] >= 2:
            raise RuntimeError("Partial upload failure on batch 2")
        original_upsert(collection_name, points)

    client.upsert = partial_fail

    service = IngestionService(
        qdrant_store=store,
        dense=FakeDenseEmbeddingService(),
        sparse=FakeSparseEmbeddingService(),
        document_registry=registry,
    )

    result = asyncio.run(service.ingest_catalogue(Path("Tiger.pdf")))

    # With safe ordering (upload-first-then-delete), old points should survive
    # even if partial upload fails, because deletion happens only after successful upload
    remaining = registry.list_indexed_documents()
    tiger_docs = [d for d in remaining if d.get("document_name") == doc_name]
    assert len(tiger_docs) >= 1, "Old points lost during partial upload failure"


# ---------------------------------------------------------------------------
# Test: F. Network timeout during replacement
# ---------------------------------------------------------------------------

def test_failure_f_timeout_preserves_old_points(mock_pipeline):
    """If a network timeout occurs during replacement, old points must be recoverable."""
    doc_name = "Tiger.pdf"
    old_doc_id = str(uuid.uuid4())  # Random, simulating production old points
    old_points = _seed_catalogue_points(doc_name, old_doc_id, num_chunks=5, sha256="old_sha_abc123")
    client = FakeQdrantClient(points=old_points, fail_on="upsert")
    store = FakeQdrantStore(client=client)
    registry = FakeDocumentRegistry(qdrant_store=store)

    from app.rag.ingestion.ingestion_service import IngestionService
    service = IngestionService(
        qdrant_store=store,
        dense=FakeDenseEmbeddingService(),
        sparse=FakeSparseEmbeddingService(),
        document_registry=registry,
    )

    result = asyncio.run(service.ingest_catalogue(Path("Tiger.pdf")))
    assert result["status"] == "failed"

    remaining = registry.list_indexed_documents()
    tiger_docs = [d for d in remaining if d.get("document_name") == doc_name]
    assert len(tiger_docs) >= 1, "Old points lost during timeout"
    assert tiger_docs[0]["chunk_count"] == 5


# ---------------------------------------------------------------------------
# Test: Verify safe ingestion preserves old points even on failure
# ---------------------------------------------------------------------------

def test_ingestion_failure_never_drops_old_points(mock_pipeline):
    """Comprehensive: any failure during ingestion must not delete old points."""
    doc_name = "Tiger.pdf"
    old_doc_id = str(uuid.uuid4())  # Random, simulating production old points
    old_points = _seed_catalogue_points(doc_name, old_doc_id, num_chunks=5, sha256="old_sha_abc123")

    for fail_on in ["upsert", "delete", "scroll"]:
        client = FakeQdrantClient(points=copy.deepcopy(old_points), fail_on=fail_on)
        store = FakeQdrantStore(client=client)
        registry = FakeDocumentRegistry(qdrant_store=store)

        from app.rag.ingestion.ingestion_service import IngestionService
        service = IngestionService(
            qdrant_store=store,
            dense=FakeDenseEmbeddingService(),
            sparse=FakeSparseEmbeddingService(),
            document_registry=registry,
        )

        try:
            asyncio.run(service.ingest_catalogue(Path(doc_name)))
        except Exception:
            pass  # Expected to fail

        # Check old points survive by comparing point IDs directly (avoids scroll
        # which may also be failing if fail_on="scroll")
        expected_ids = set(old_points.keys())
        actual_ids = set(client.points.keys())
        lost = expected_ids - actual_ids
        assert not lost, f"Old points lost when fail_on={fail_on}: {lost}"
