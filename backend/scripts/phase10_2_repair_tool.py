"""Phase 10.2 Qdrant data repair tooling — read-only / dry-run only.

Supports safe, targeted repairs of Qdrant collection metadata without
mutating production vectors. No --apply mode is provided; repairs require
separate review before execution.

Modes:
  --audit      Read-only inventory of target documents (no changes)
  --dry-run    Plan exact before/after diffs, write backup snapshot, no writes

Safety:
  - Targets points by exact document_name only (no fuzzy/ambiguous matching)
  - Never overwrites a point merely because its document name matches
  - Full backup (IDs, payloads, vectors) before any proposed change
  - Idempotency checks: skips if already in desired state
  - Rollback snapshot included in dry-run output
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.rag.vectorstore.qdrant_store import QdrantStore

BACKUP_DIR = Path("/tmp/kilo/phase10_2_backups")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def scroll_all_points(store: QdrantStore) -> list[dict[str, Any]]:
    """Scroll every point with payload + vectors. Read-only."""
    all_points: list[dict[str, Any]] = []
    offset = None
    while True:
        batch, offset = store.client.scroll(
            collection_name=store.collection_name,
            limit=1000,
            offset=offset,
            with_payload=True,
            with_vectors=True,
        )
        for p in batch:
            vec = p.vector
            all_points.append({
                "id": str(p.id),
                "payload": dict(p.payload or {}),
                "vector": {
                    "dense": list(vec["dense"]) if vec and "dense" in vec else None,
                    "sparse": {
                        "indices": list(vec["sparse"].indices) if vec and "sparse" in vec else [],
                        "values": [float(v) for v in vec["sparse"].values] if vec and "sparse" in vec else [],
                    },
                } if vec else None,
            })
        if offset is None:
            break
    return all_points


def points_by_document(points: list[dict[str, Any]], document_name: str) -> list[dict[str, Any]]:
    return [p for p in points if (p.get("payload") or {}).get("document_name") == document_name]


def backup_points(points: list[dict[str, Any]], document_name: str) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    safe_name = document_name.replace(" ", "_").replace("/", "_")
    path = BACKUP_DIR / f"{safe_name}_{ts}.json"
    snapshot = {
        "generated_at": ts,
        "document_name": document_name,
        "point_count": len(points),
        "points": points,
    }
    path.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
    return path


def verify_backup(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pts = data.get("points", [])
    return {
        "path": str(path),
        "document_name": data.get("document_name"),
        "point_count": data.get("point_count"),
        "backup_point_count": len(pts),
        "all_have_ids": all(p.get("id") for p in pts),
        "all_have_payloads": all(p.get("payload") for p in pts),
        "ids": [p["id"] for p in pts],
    }


def diff_payloads(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Produce a before/after payload diff."""
    changed: dict[str, Any] = {}
    all_keys = set(before.keys()) | set(after.keys())
    for k in sorted(all_keys):
        bv = before.get(k)
        av = after.get(k)
        if bv != av:
            changed[k] = {"before": bv, "after": av}
    return changed


# ---------------------------------------------------------------------------
# Repair plans (read-only definitions; no execution)
# ---------------------------------------------------------------------------

def plan_tiger_mini_reingestion(points: list[dict[str, Any]]) -> dict[str, Any]:
    """Tiger_mini.pdf: 8 points exist with no text. Plan reingestion.

    Desired after-state: same 8 point IDs, payload gains text + chunk_id +
    document_id + source_type + model. Vectors regenerated from OCR text.
    """
    tg = points_by_document(points, "Tiger_mini.pdf")
    if not tg:
        return {"document": "Tiger_mini.pdf", "status": "not_found", "points": 0}

    # Idempotency: check if any point already has text
    has_text = any((p.get("payload") or {}).get("text") for p in tg)

    plan = {
        "document": "Tiger_mini.pdf",
        "repair_type": "reingestion",
        "affected_point_ids": [p["id"] for p in tg],
        "point_count": len(tg),
        "point_count_impact": 0,  # same IDs, payload+vector update only
        "idempotent": has_text,
        "already_has_text": has_text,
        "current_payload_sample": copy.deepcopy(tg[0]["payload"]) if tg else {},
        "desired_payload_changes": {
            "add": ["text", "chunk_id", "document_id", "source_type", "model"],
            "preserve": ["document_name", "product_slug"],
        },
        "vector_impact": "dense + sparse vectors regenerated from OCR text",
        "source_sha256": "a46dd4cdcb9c4b84614e9c51500933e24f72bd2436e28562937ceb522edbbd24",
        "affected_cases": ["identity-29", "technical-21"],
    }
    return plan


def plan_automatic_gun_family_slug(points: list[dict[str, Any]]) -> dict[str, Any]:
    """AUTOMATIC_gun.pdf: add automatic-spray-guns family slug to product_slug.

    Converts product_slug from string to array, appending family slug.
    Child-product slugs (400b, flamingo, hotmelt, vria, vriad) preserved.
    """
    ag = points_by_document(points, "AUTOMATIC_gun.pdf")
    if not ag:
        return {"document": "AUTOMATIC_gun.pdf", "status": "not_found", "points": 0}

    family_slug = "automatic-spray-guns"
    already_has = all(
        family_slug in ((p.get("payload") or {}).get("product_slug") or [])
        if isinstance((p.get("payload") or {}).get("product_slug"), list)
        else (p.get("payload") or {}).get("product_slug") == family_slug
        for p in ag
    )

    diffs = []
    for p in ag:
        pl = p.get("payload") or {}
        current = pl.get("product_slug")
        if isinstance(current, list):
            new_val = list(current)
            if family_slug not in new_val:
                new_val.append(family_slug)
        else:
            new_val = [current, family_slug] if current else [family_slug]
        if new_val != current:
            diffs.append({
                "point_id": p["id"],
                "payload_diff": diff_payloads(pl, {**pl, "product_slug": new_val}),
            })

    return {
        "document": "AUTOMATIC_gun.pdf",
        "repair_type": "metadata_add_family_slug",
        "affected_point_ids": [p["id"] for p in ag],
        "point_count": len(ag),
        "point_count_impact": 0,
        "idempotent": already_has,
        "already_has_family_slug": already_has,
        "family_slug": family_slug,
        "child_slugs_preserved": ["400b", "flamingo", "hotmelt", "vria", "vriad"],
        "point_diffs": diffs,
        "affected_cases": ["identity-30"],
    }


def plan_manual_guns_family_slug(points: list[dict[str, Any]]) -> dict[str, Any]:
    """manual_GUNS.pdf: add manual-spray-guns family slug to product_slug.

    Converts product_slug from string to array, appending family slug.
    Child-product slugs (am250, eagle, ext-i, falcon, flamingo, hawk, pole,
    vrid, vril, wax-spray-gun) preserved.
    """
    mg = points_by_document(points, "manual_GUNS.pdf")
    if not mg:
        return {"document": "manual_GUNS.pdf", "status": "not_found", "points": 0}

    family_slug = "manual-spray-guns"
    already_has = all(
        family_slug in ((p.get("payload") or {}).get("product_slug") or [])
        if isinstance((p.get("payload") or {}).get("product_slug"), list)
        else (p.get("payload") or {}).get("product_slug") == family_slug
        for p in mg
    )

    diffs = []
    for p in mg:
        pl = p.get("payload") or {}
        current = pl.get("product_slug")
        if isinstance(current, list):
            new_val = list(current)
            if family_slug not in new_val:
                new_val.append(family_slug)
        else:
            new_val = [current, family_slug] if current else [family_slug]
        if new_val != current:
            diffs.append({
                "point_id": p["id"],
                "payload_diff": diff_payloads(pl, {**pl, "product_slug": new_val}),
            })

    return {
        "document": "manual_GUNS.pdf",
        "repair_type": "metadata_add_family_slug",
        "affected_point_ids": [p["id"] for p in mg],
        "point_count": len(mg),
        "point_count_impact": 0,
        "idempotent": already_has,
        "already_has_family_slug": already_has,
        "family_slug": family_slug,
        "child_slugs_preserved": ["am250", "eagle", "ext-i", "falcon", "flamingo", "hawk", "pole", "vrid", "vril", "wax-spray-gun"],
        "point_diffs": diffs,
        "affected_cases": ["identity-31"],
    }


def plan_elephant_ocr_correction(points: list[dict[str, Any]]) -> dict[str, Any]:
    """Elephant.pdf: correct OCR error 3:] -> 3:1 in chunk 6.

    Only the specific point with chunk_id ending ::chunk::6 is changed.
    Dense + sparse vectors regenerated from corrected text.
    """
    el = points_by_document(points, "Elephant.pdf")
    if not el:
        return {"document": "Elephant.pdf", "status": "not_found", "points": 0}

    target_chunk_suffix = "::chunk::6"
    target = None
    for p in el:
        cid = (p.get("payload") or {}).get("chunk_id") or ""
        if cid.endswith(target_chunk_suffix):
            target = p
            break

    if target is None:
        return {
            "document": "Elephant.pdf",
            "repair_type": "ocr_correction",
            "status": "target_chunk_not_found",
            "point_count": len(el),
            "affected_cases": ["cmp-01"],
        }

    current_text = (target.get("payload") or {}).get("text", "")
    corrected_text = current_text.replace("3:]", "3:1")

    return {
        "document": "Elephant.pdf",
        "repair_type": "ocr_correction",
        "affected_point_ids": [target["id"]],
        "point_count": 1,
        "total_elephant_points": len(el),
        "point_count_impact": 0,
        "target_chunk_id": target.get("payload", {}).get("chunk_id"),
        "idempotent": "3:]" not in current_text,
        "already_corrected": "3:]" not in current_text,
        "text_diff": {
            "before": current_text,
            "after": corrected_text,
            "changed": current_text != corrected_text,
        },
        "vector_impact": "dense + sparse vectors regenerated from corrected text",
        "preserve": ["point_id", "document_name", "product_slug", "source_attribution", "model", "units"],
        "affected_cases": ["cmp-01"],
    }


REPAIR_PLANS = {
    "Tiger_mini.pdf": plan_tiger_mini_reingestion,
    "AUTOMATIC_gun.pdf": plan_automatic_gun_family_slug,
    "manual_GUNS.pdf": plan_manual_guns_family_slug,
    "Elephant.pdf": plan_elephant_ocr_correction,
}


def run_audit(store: QdrantStore, target_docs: list[str] | None = None) -> dict[str, Any]:
    """Read-only audit: inventory target documents without any changes."""
    points = scroll_all_points(store)
    docs = target_docs or list(REPAIR_PLANS.keys())
    result: dict[str, Any] = {
        "mode": "audit",
        "collection": store.collection_name,
        "total_points": len(points),
        "generated_at": datetime.now(UTC).isoformat(),
        "documents": {},
    }
    for doc in docs:
        pts = points_by_document(points, doc)
        result["documents"][doc] = {
            "point_count": len(pts),
            "point_ids": [p["id"] for p in pts],
            "sample_payload": copy.deepcopy(pts[0]["payload"]) if pts else {},
            "has_text": any(bool((p.get("payload") or {}).get("text")) for p in pts),
            "product_slugs": sorted({(p.get("payload") or {}).get("product_slug") for p in pts if (p.get("payload") or {}).get("product_slug")}),
        }
    return result


def run_dry_run(store: QdrantStore, target_docs: list[str] | None = None) -> dict[str, Any]:
    """Dry-run: backup all target points, compute before/after diffs, no writes."""
    points = scroll_all_points(store)
    docs = target_docs or list(REPAIR_PLANS.keys())

    backups: dict[str, Any] = {}
    plans: dict[str, Any] = {}

    for doc in docs:
        pts = points_by_document(points, doc)
        if not pts:
            plans[doc] = {"status": "not_found_in_qdrant"}
            continue

        # Backup before any proposed change
        backup_path = backup_points(pts, doc)
        backups[doc] = verify_backup(backup_path)

        # Compute repair plan
        plan_fn = REPAIR_PLANS.get(doc)
        if plan_fn:
            plans[doc] = plan_fn(points)
        else:
            plans[doc] = {"status": "no_repair_plan"}

    return {
        "mode": "dry-run",
        "collection": store.collection_name,
        "total_points": len(points),
        "generated_at": datetime.now(UTC).isoformat(),
        "backups": backups,
        "repair_plans": plans,
        "rollback_available": True,
        "rollback_method": "re-import backup JSON via delete_by_document_name + upsert with original payloads/vectors",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 10.2 Qdrant repair tool (read-only/dry-run)")
    parser.add_argument("--audit", action="store_true", help="Read-only inventory of target documents")
    parser.add_argument("--dry-run", action="store_true", help="Plan before/after diffs + backup snapshot, no writes")
    parser.add_argument("--document", action="append", help="Target document name (exact match, repeatable)")
    args = parser.parse_args()

    if not args.audit and not args.dry_run:
        parser.error("one of --audit or --dry-run is required")

    store = QdrantStore()

    if args.audit:
        result = run_audit(store, args.document)
    else:
        result = run_dry_run(store, args.document)

    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
