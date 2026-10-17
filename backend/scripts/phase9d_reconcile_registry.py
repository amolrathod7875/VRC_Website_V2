"""
Phase 9D — PostgreSQL Registry Reconciliation (Optimized)
Uses pre-computed Qdrant stats to avoid index issues.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.core.config import settings
from app.core.database import async_session_factory
from app.models.rag_document import RagDocument
from app.rag.catalogue_resolver import _FILENAME_FALLBACK
from app.rag.utils.hashing import calculate_sha256
from sqlalchemy import select, func

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATALOGUE_DIR = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues")

# Canonical product slugs
DOCUMENT_TO_SLUG = {
    **{k.lower(): v for k, v in _FILENAME_FALLBACK.items()},
    "dragon.pdf": "dragon",
    "polyurea.pdf": "polyurea",
    "tube varnish coating system.pdf": "tube-varnish-coating-system",
    "vrc mix (low - medium) pressure.pdf": "vrc-mix-low-medium-pressure",
    "vrc - mix hp.pdf": "vrc-mix-hp",
    "barrel pump.pdf": "barrel-pump",
}

# Multi-product documents
MULTI_PRODUCT_DOCS = {
    "manual_GUNS.pdf": ["manual-spray-guns", "kingfisher"],
    "AUTOMATIC_gun.pdf": ["automatic-spray-guns", "automatic-spray-guns-2"],
    "CONVENTIONAL GUNS_f.pdf": ["kingfisher", "conventional-guns"],
    "diaphragm pump.pdf": ["hippo"],
    "filters.pdf": ["filters"],
    "Valves.pdf": ["ball-valves", "valves"],
    "regulator.pdf": ["regulator"],
    "Other Accessories.pdf": ["other-accessories"],
    "PULSATION DAMPNER.pdf": ["pulsation-dampner"],
    "PORTABLE PRESSURE FEED POT.pdf": ["portable-pressure-feed-pot"],
    "Paint Preparation Unit.pdf": ["paint-preparation-unit"],
    "Electric_pump.pdf": ["leopard"],
    "LION_Catalogue.pdf": ["lion"],
    "Tiger.pdf": ["tiger"],
    "Tiger_mini.pdf": ["tiger-mini"],
    "rhino.pdf": ["rhino"],
    "Elephant.pdf": ["elephant"],
    "Hippo.pdf": ["hippo"],
    "Cheetah.pdf": ["cheetah"],
    "cub.pdf": ["cub"],
    "DRUM PRESS.pdf": ["drum-press"],
    "PNEUMATIC STIRRER.pdf": ["pneumatic-stirrer"],
    "turbine.pdf": ["turbine"],
    "ball_valves.pdf": ["ball-valves"],
}

# Company Master
COMPANY_MASTER_FILE = "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt"
COMPANY_MASTER_PATH = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/knowledge") / COMPANY_MASTER_FILE

def _qdrant_stats() -> Dict[str, Dict[str, Any]]:
    """Live Qdrant reconciliation: count points and collect product slugs per document_name.

    Computed at runtime from Qdrant rather than read from a static dict, so a newly
    ingested document is reconciled automatically without a manual table edit.
    """
    try:
        from qdrant_client import QdrantClient
        from app.rag.config import rag_settings
        client = QdrantClient(
            url=rag_settings.QDRANT_URL,
            api_key=rag_settings.QDRANT_API_KEY or None,
            check_compatibility=False,
        )
        collection = rag_settings.QDRANT_COLLECTION_NAME
        total = client.count(collection_name=collection).count

        per_doc: Dict[str, Dict[str, Any]] = {}
        nxt = None
        while True:
            r = client.scroll(
                collection_name=collection,
                scroll_filter=None,
                limit=2000,
                offset=nxt,
                with_payload=["document_name", "product_slug", "source_type"],
                with_vectors=False,
            )
            pts, nxt = r[0], r[1]
            if not pts:
                break
            for p in pts:
                pl = p.payload or {}
                nm = pl.get("document_name")
                slug = pl.get("product_slug")
                key = nm if nm else "<no_document_name>"
                entry = per_doc.setdefault(key, {"count": 0, "slugs": []})
                entry["count"] += 1
                if slug and slug not in entry["slugs"]:
                    entry["slugs"].append(slug)
            if nxt is None:
                break

        per_doc["__total__"] = {"count": total, "slugs": []}
        return per_doc
    except Exception as exc:
        logger.warning(f"Qdrant live reconciliation unavailable, falling back to static table: {exc}")
        result: Dict[str, Dict[str, Any]] = {"__total__": {"count": 0, "slugs": []}}
        for doc_name, count in QDRANT_CHUNK_COUNTS.items():
            result[doc_name] = {"count": count, "slugs": list(QDRANT_SLUGS.get(doc_name, []))}
        return result


def _qdrant_chunk_count(doc_name: str, stats: Dict[str, Dict[str, Any]]) -> int:
    entry = stats.get(doc_name)
    if entry is None:
        return 0
    return entry.get("count", 0)


def _qdrant_slugs(doc_name: str, stats: Dict[str, Dict[str, Any]]) -> List[str]:
    entry = stats.get(doc_name)
    if not entry:
        return []
    return list(entry.get("slugs", []))


async def reconcile_registry() -> Dict[str, Any]:
    catalogue_files = sorted([f for f in CATALOGUE_DIR.iterdir() if f.suffix.lower() == ".pdf"])
    logger.info(f"Filesystem catalogues: {len(catalogue_files)}")

    async with async_session_factory() as db:
        result = await db.execute(select(RagDocument))
        existing_docs = {d.document_name: d for d in result.scalars().all()}
        logger.info(f"PostgreSQL existing RagDocuments: {len(existing_docs)}")

        reconciled = 0
        created = 0
        updated = 0
        mismatches = []

        # Live Qdrant reconciliation (computed at runtime, not a static table).
        qdrant_stats = _qdrant_stats()
        qdrant_total = qdrant_stats.get("__total__", {}).get("count", 0)
        logger.info(f"Qdrant live total points: {qdrant_total}")

        for pdf_file in catalogue_files:
            doc_name = pdf_file.name
            doc_name_lower = doc_name.lower()

            sha256 = calculate_sha256(pdf_file)
            primary_slug = DOCUMENT_TO_SLUG.get(doc_name_lower)
            additional_slugs = MULTI_PRODUCT_DOCS.get(doc_name, [])
            all_slugs = list(set([primary_slug] + additional_slugs)) if primary_slug else additional_slugs

            # Live Qdrant stats for this document.
            qdrant_chunk_count = _qdrant_chunk_count(doc_name, qdrant_stats)
            qdrant_slugs = _qdrant_slugs(doc_name, qdrant_stats)

            if qdrant_slugs:
                primary_slug = primary_slug or qdrant_slugs[0]
                all_slugs = list(set(all_slugs + qdrant_slugs))

            existing = existing_docs.get(doc_name)

            classification = "POSTGRES_MISSING" if not existing else "MATCHED"
            if existing:
                if existing.sha256 != sha256:
                    mismatches.append(f"{doc_name}: SHA mismatch")
                    classification = "METADATA_MISMATCH"
                if existing.chunk_count != qdrant_chunk_count and qdrant_chunk_count > 0:
                    mismatches.append(f"{doc_name}: chunk_count mismatch (DB={existing.chunk_count} vs Qdrant={qdrant_chunk_count})")
                    classification = "METADATA_MISMATCH"
                if existing.product_slug != primary_slug:
                    mismatches.append(f"{doc_name}: product_slug mismatch (DB={existing.product_slug} vs expected={primary_slug})")
                    classification = "METADATA_MISMATCH"

            logger.info(f"  {doc_name}: {classification} | slug={primary_slug} | slugs={all_slugs} | chunks={qdrant_chunk_count} | sha={sha256[:16]}...")

            if not existing:
                doc = RagDocument(
                    document_name=doc_name,
                    source_type="catalogue",
                    storage_path=str(pdf_file),
                    sha256=sha256,
                    status="indexed",
                    qdrant_document_id=sha256[:32],
                    product_slug=primary_slug,
                    product_slugs=all_slugs if len(all_slugs) > 1 else None,
                    chunk_count=qdrant_chunk_count,
                    last_ingested_at=datetime.now(timezone.utc),
                )
                db.add(doc)
                created += 1
            else:
                existing.sha256 = sha256
                existing.product_slug = primary_slug
                existing.product_slugs = all_slugs if len(all_slugs) > 1 else None
                # Set chunk_count to the ACTUAL Qdrant count, not max(existing, qdrant):
                # the old registry held stale hardcoded values that disagreed with Qdrant.
                existing.chunk_count = qdrant_chunk_count
                existing.status = "indexed"
                existing.last_ingested_at = datetime.now(timezone.utc)
                updated += 1

            reconciled += 1

        # Company Master
        if COMPANY_MASTER_PATH.exists():
            master_sha = calculate_sha256(COMPANY_MASTER_PATH)
            qdrant_chunk_count = _qdrant_chunk_count(COMPANY_MASTER_FILE, qdrant_stats)

            existing = existing_docs.get(COMPANY_MASTER_FILE)
            if not existing:
                master_doc = RagDocument(
                    document_name=COMPANY_MASTER_FILE,
                    source_type="company_kb",
                    storage_path=str(COMPANY_MASTER_PATH),
                    sha256=master_sha,
                    status="indexed",
                    qdrant_document_id=master_sha[:32],
                    product_slug=None,
                    product_slugs=None,
                    chunk_count=qdrant_chunk_count,
                    last_ingested_at=datetime.now(timezone.utc),
                )
                db.add(master_doc)
                created += 1
                logger.info(f"  {COMPANY_MASTER_FILE}: CREATED | chunks={qdrant_chunk_count}")
            else:
                existing.sha256 = master_sha
                existing.chunk_count = qdrant_chunk_count
                existing.status = "indexed"
                existing.last_ingested_at = datetime.now(timezone.utc)
                updated += 1
                logger.info(f"  {COMPANY_MASTER_FILE}: UPDATED | chunks={qdrant_chunk_count}")
        else:
            logger.warning(f"Company Master file not found")

        await db.commit()
        logger.info(f"Reconciliation complete: {created} created, {updated} updated, {reconciled} catalogues")

        if mismatches:
            logger.warning(f"Mismatches ({len(mismatches)}):")
            for m in mismatches:
                logger.warning(f"  {m}")
        else:
            logger.info("No metadata mismatches")

        # Final counts
        result = await db.execute(select(func.count(RagDocument.id)).where(RagDocument.source_type == "catalogue"))
        catalogue_count = result.scalar_one() or 0
        result = await db.execute(select(func.count(RagDocument.id)).where(RagDocument.source_type == "company_kb"))
        company_count = result.scalar_one() or 0
        result = await db.execute(select(func.count(RagDocument.id)))
        total_count = result.scalar_one() or 0

        logger.info(f"Final: catalogue={catalogue_count}, company_kb={company_count}, total={total_count}")

        return {
            "catalogue_count": catalogue_count,
            "company_count": company_count,
            "total_count": total_count,
            "created": created,
            "updated": updated,
            "mismatches": mismatches,
        }


async def main():
    result = await reconcile_registry()
    report = {"timestamp": datetime.now(timezone.utc).isoformat(), "result": result}
    report_path = Path("/home/vr-coatings/Desktop/website_V2/backend/rag_debug/phase9d_reconciliation_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    logger.info(f"Report saved to {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
