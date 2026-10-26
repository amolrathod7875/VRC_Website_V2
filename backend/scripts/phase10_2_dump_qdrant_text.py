"""Dump Qdrant payload text for target documents to inspect OCR content.

Read-only: scrolls Qdrant payloads; never writes or deletes points.
"""
from __future__ import annotations

import json
from collections import defaultdict

from app.rag.vectorstore.qdrant_store import QdrantStore

TARGET_DOCS = [
    "Elephant.pdf",
    "Tiger_mini.pdf",
    "AUTOMATIC_gun.pdf",
    "manual_GUNS.pdf",
    "VRC - MIX HP.pdf",
    "VRC MIX (LOW - MEDIUM) PRESSURE.pdf",
    "Electric_pump.pdf",
    "Paint Preparation Unit.pdf",
    "rhino.pdf",
]


def main() -> dict:
    vs = QdrantStore()
    by_doc: dict[str, list] = defaultdict(list)
    offset = None
    while True:
        batch, offset = vs.client.scroll(
            collection_name=vs.collection_name,
            limit=500,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for p in batch:
            pl = p.payload or {}
            dn = pl.get("document_name")
            if dn in TARGET_DOCS:
                by_doc[dn].append(
                    {
                        "id": str(p.id),
                        "product_slug": pl.get("product_slug"),
                        "document_id": pl.get("document_id"),
                        "chunk_id": pl.get("chunk_id"),
                        "text": pl.get("text") or pl.get("content") or "",
                        "source_type": pl.get("source_type"),
                        "model": pl.get("model"),
                        "payload_keys": sorted(pl.keys()),
                    }
                )
        if offset is None:
            break

    out: dict[str, dict] = {}
    for dn in TARGET_DOCS:
        pts = by_doc.get(dn, [])
        out[dn] = {
            "point_count": len(pts),
            "slugs": sorted({p["product_slug"] for p in pts if p["product_slug"]}),
            "has_text": sum(1 for p in pts if p["text"].strip()),
            "sample_texts": [],
            "all_text_concatenated": "\n".join(p["text"] for p in pts),
        }
        for p in pts:
            out[dn]["sample_texts"].append(
                {
                    "id": p["id"],
                    "slug": p["product_slug"],
                    "chunk": p["chunk_id"],
                    "text": p["text"],
                }
            )

    print(json.dumps(out, indent=2, default=str))
    return out


if __name__ == "__main__":
    main()
