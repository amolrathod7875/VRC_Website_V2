"""Offline Qdrant data-quality audit for Phase 10.2.

Compares filesystem catalogue PDFs against Qdrant collection metadata and
dumps the OCR text stored per document so root causes of evaluation failures
can be diagnosed without mutating production Qdrant.

Read-only: only scrolls Qdrant payloads; never writes or deletes points.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from app.rag.vectorstore.qdrant_store import QdrantStore

CATALOGUE_DIR = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues")
TARGET_DOCS = [
    "Tiger_mini.pdf",
    "AUTOMATIC_gun.pdf",
    "manual_GUNS.pdf",
    "Electric_pump.pdf",
    "leopard.pdf",
    "Elephant.pdf",
    "rhino.pdf",
    "VRC - MIX HP.pdf",
    "VRC MIX (LOW - MEDIUM) PRESSURE.pdf",
    "Paint Preparation Unit.pdf",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> dict:
    vs = QdrantStore()
    all_points = []
    offset = None
    while True:
        batch, offset = vs.client.scroll(
            collection_name=vs.collection_name,
            limit=1000,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        all_points.extend(batch)
        if offset is None:
            break

    doc_names: Counter[str] = Counter()
    product_slugs: Counter[str] = Counter()
    doc_to_points: dict[str, list] = defaultdict(list)
    doc_to_slugs: dict[str, set] = defaultdict(set)
    slug_to_docs: dict[str, set] = defaultdict(set)
    missing_document_id = 0
    sample_payloads: dict[str, dict] = {}

    for p in all_points:
        pl = p.payload or {}
        dn = pl.get("document_name")
        ps = pl.get("product_slug")
        di = pl.get("document_id")
        key = dn if dn else "<NONE>"
        doc_names[key] += 1
        doc_to_points[key].append(str(p.id))
        if dn and dn not in sample_payloads:
            sample_payloads[dn] = pl
        if ps is None:
            product_slugs["<NONE>"] += 1
        else:
            product_slugs[ps] += 1
        if dn and ps:
            doc_to_slugs[dn].add(ps)
            slug_to_docs[ps].add(dn)
        if di is None:
            missing_document_id += 1

    fs_docs: dict[str, dict] = {}
    for f in sorted(CATALOGUE_DIR.iterdir()):
        if f.is_file() and f.suffix.lower() == ".pdf":
            fs_docs[f.name] = {
                "size_bytes": f.stat().st_size,
                "sha256": sha256_file(f),
            }

    inventory = {
        "qdrant_point_count": len(all_points),
        "qdrant_document_names": dict(doc_names),
        "qdrant_product_slugs": dict(product_slugs),
        "missing_document_id_count": missing_document_id,
        "doc_to_slugs": {k: sorted(v) for k, v in doc_to_slugs.items()},
        "slug_to_docs": {k: sorted(v) for k, v in slug_to_docs.items()},
        "filesystem": fs_docs,
        "sample_payloads": {
            k: v for k, v in sample_payloads.items() if k in TARGET_DOCS
        },
    }

    print(json.dumps(inventory, indent=2, default=str))
    return inventory


if __name__ == "__main__":
    main()
