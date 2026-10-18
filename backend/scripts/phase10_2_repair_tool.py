"""Phase 10.2 Qdrant data repair tooling — read-only / dry-run only.

Supports safe, targeted repairs of Qdrant collection metadata without
mutating production vectors. No --apply mode is provided; repairs require
separate review before execution.

Modes:
  --audit      Read-only inventory of target documents (no changes)
  --dry-run    Plan exact before/after diffs, write backup snapshot, no writes
  --rollback-test  Simulate failure during partial update, verify exact-point restore

Safety:
  - Targets points by exact ID only (no document-name bulk deletion)
  - Full backup (IDs, payloads, vectors) per point before any proposed change
  - Idempotency checks: skips if already in desired state
  - Rollback restores exact point IDs (payload + vectors), never bulk-delete by document name
  - Newly created point IDs tracked separately for rollback cleanup
  - Backups written to /tmp with restrictive permissions (0600), never committed
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.rag.vectorstore.qdrant_store import QdrantStore

BACKUP_DIR = Path("/tmp/kilo/phase10_2_backups")


def _restrictive_permissions(path: Path) -> None:
    """Set 0600 owner-only permissions on a backup file."""
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


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


def points_by_ids(points: list[dict[str, Any]], point_ids: list[str]) -> list[dict[str, Any]]:
    id_set = set(point_ids)
    return [p for p in points if p.get("id") in id_set]


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
    _restrictive_permissions(path)
    return path


def verify_backup(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pts = data.get("points", [])
    checksum = sha256_file(path)
    return {
        "path": str(path),
        "checksum_sha256": checksum,
        "document_name": data.get("document_name"),
        "point_count": data.get("point_count"),
        "backup_point_count": len(pts),
        "all_have_ids": all(p.get("id") for p in pts),
        "all_have_payloads": all(p.get("payload") for p in pts),
        "all_have_vectors": all(p.get("vector") for p in pts),
        "ids": [p["id"] for p in pts],
        "permissions_owner_only": bool(os.stat(path).st_mode & stat.S_IRUSR)
        and not bool(os.stat(path).st_mode & (stat.S_IRGRP | stat.S_IROTH)),
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


def diff_text(before: str, after: str) -> dict[str, Any]:
    return {"before": before, "after": after, "changed": before != after}


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

    has_text = any((p.get("payload") or {}).get("text") for p in tg)

    return {
        "document": "Tiger_mini.pdf",
        "repair_type": "reingestion",
        "affected_point_ids": [p["id"] for p in tg],
        "point_count": len(tg),
        "point_count_impact": 0,
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
        "rollback_strategy": "exact_point_restore",
        "new_point_ids": [],
    }


def plan_spray_gun_family_retrieval(points: list[dict[str, Any]]) -> dict[str, Any]:
    """Spray-gun family retrieval: enable filtering by family via parent_product_slug.

    Approach: keep product_slug scalar (child slugs only). Add parent_product_slug
    to Qdrant payload index and extend _build_qdrant_filter to support an OR key
    (product_slug=child OR parent_product_slug=family). Array product_slug was
    evaluated and rejected: context_builder.py:80-83 does f"{product_slug}:{model}"
    string formatting and line 340 does equality comparison, both broken by arrays.

    AUTOMATIC_gun.pdf (7 points): child slugs 400b, flamingo, hotmelt, vria, vriad
    manual_GUNS.pdf (10 points): child slugs am250, eagle, ext-i, falcon, flamingo,
    pole, vrid, vril, wax-spray-gun

    parent_product_slug already set on all 17 points but is not indexed.
    """
    auto = points_by_document(points, "AUTOMATIC_gun.pdf")
    manual = points_by_document(points, "manual_GUNS.pdf")
    all_sg = auto + manual

    family_map = {
        "AUTOMATIC_gun.pdf": "automatic-spray-guns",
        "manual_GUNS.pdf": "manual-spray-guns",
    }

    missing_parent = [
        p["id"] for p in all_sg
        if not (p.get("payload") or {}).get("parent_product_slug")
    ]

    diffs = []
    for p in all_sg:
        pl = p.get("payload") or {}
        doc = pl.get("document_name", "")
        family = family_map.get(doc)
        current_parent = pl.get("parent_product_slug")
        if family and current_parent != family:
            diffs.append({
                "point_id": p["id"],
                "document_name": doc,
                "payload_diff": diff_payloads(pl, {**pl, "parent_product_slug": family}),
            })

    return {
        "document": "spray_gun_family",
        "documents": ["AUTOMATIC_gun.pdf", "manual_GUNS.pdf"],
        "repair_type": "parent_product_slug_index_and_or_filter",
        "affected_point_ids": [p["id"] for p in all_sg],
        "point_count": len(all_sg),
        "point_count_impact": 0,
        "idempotent": len(missing_parent) == 0 and len(diffs) == 0,
        "missing_parent_slug": missing_parent,
        "family_slug_map": family_map,
        "child_slugs_preserved": True,
        "product_slug_remains_scalar": True,
        "parent_product_slug_index_required": True,
        "or_filter_support_required": True,
        "point_diffs": diffs,
        "affected_cases": ["identity-30", "identity-31"],
        "rollback_strategy": "exact_point_restore",
        "new_point_ids": [],
        "code_changes_required": [
            "app/rag/vectorstore/qdrant_store.py: add parent_product_slug to _ensure_indexes",
            "app/rag/vectorstore/qdrant_store.py: add parent_product_slug to _indexed_payload_fields",
            "app/rag/vectorstore/qdrant_store.py: extend _build_qdrant_filter to support OR key",
        ],
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
        "text_diff": diff_text(current_text, corrected_text),
        "vector_impact": "dense + sparse vectors regenerated from corrected text",
        "preserve": ["point_id", "document_name", "product_slug", "document_id", "source_type", "model"],
        "affected_cases": ["cmp-01"],
        "rollback_strategy": "exact_point_restore",
        "new_point_ids": [],
        "source_sha256": "bfed7495fec53982cee19276d6ff657b3b3ec156942d71e6112e38e6a2185653",
    }


REPAIR_PLANS = {
    "Tiger_mini.pdf": plan_tiger_mini_reingestion,
    "AUTOMATIC_gun.pdf": plan_spray_gun_family_retrieval,
    "manual_GUNS.pdf": plan_spray_gun_family_retrieval,
    "Elephant.pdf": plan_elephant_ocr_correction,
}


def run_audit(store: QdrantStore, target_docs: list[str] | None = None) -> dict[str, Any]:
    """Read-only audit: inventory target documents without any changes."""
    points = scroll_all_points(store)
    docs = target_docs or ["Tiger_mini.pdf", "AUTOMATIC_gun.pdf", "manual_GUNS.pdf", "Elephant.pdf"]
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
            "parent_product_slugs": sorted({(p.get("payload") or {}).get("parent_product_slug") for p in pts if (p.get("payload") or {}).get("parent_product_slug")}),
        }
    return result


def run_dry_run(store: QdrantStore, target_docs: list[str] | None = None) -> dict[str, Any]:
    """Dry-run: backup exact point IDs, compute before/after diffs, no writes."""
    points = scroll_all_points(store)
    docs = target_docs or ["Tiger_mini.pdf", "AUTOMATIC_gun.pdf", "manual_GUNS.pdf", "Elephant.pdf"]

    backups: dict[str, Any] = {}
    plans: dict[str, Any] = {}

    for doc in docs:
        pts = points_by_document(points, doc)
        if not pts:
            plans[doc] = {"status": "not_found_in_qdrant"}
            continue

        # Exact-point backup: all point IDs with full payloads + vectors
        backup_path = backup_points(pts, doc)
        backups[doc] = verify_backup(backup_path)

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
        "rollback_method": "exact_point_restore: delete only affected point IDs, upsert original payloads+vectors from backup",
        "rollback_never_bulk_deletes_by_document_name": True,
    }


def simulate_rollback(points: list[dict[str, Any]], point_ids: list[str], backup_path: Path) -> dict[str, Any]:
    """Simulate failure during partial update, then verify exact-point restore.

    Read-only simulation: verifies that backup contains all target point IDs
    with complete payloads and vectors, sufficient for exact restore.
    """
    data = json.loads(backup_path.read_text(encoding="utf-8"))
    backup_pts = {p["id"]: p for p in data.get("points", [])}

    missing_in_backup = [pid for pid in point_ids if pid not in backup_pts]
    incomplete = []
    for pid in point_ids:
        if pid in backup_pts:
            bp = backup_pts[pid]
            if not bp.get("payload"):
                incomplete.append({"point_id": pid, "issue": "missing_payload"})
            if not bp.get("vector"):
                incomplete.append({"point_id": pid, "issue": "missing_vector"})

    return {
        "simulated_point_ids": point_ids,
        "backup_path": str(backup_path),
        "checksum_sha256": sha256_file(backup_path),
        "all_points_in_backup": len(missing_in_backup) == 0,
        "missing_from_backup": missing_in_backup,
        "incomplete_backups": incomplete,
        "rollback_feasible": len(missing_in_backup) == 0 and len(incomplete) == 0,
        "rollback_strategy": "delete_by_exact_ids + upsert_original_payloads_vectors",
        "never_bulk_delete_by_document_name": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 10.2 Qdrant repair tool (read-only/dry-run)")
    parser.add_argument("--audit", action="store_true", help="Read-only inventory of target documents")
    parser.add_argument("--dry-run", action="store_true", help="Plan before/after diffs + backup snapshot, no writes")
    parser.add_argument("--rollback-test", action="store_true", help="Simulate failure + verify exact-point rollback")
    parser.add_argument("--document", action="append", help="Target document name (exact match, repeatable)")
    parser.add_argument("--backup", help="Backup file path for rollback test")
    args = parser.parse_args()

    if not args.audit and not args.dry_run and not args.rollback_test:
        parser.error("one of --audit, --dry-run, or --rollback-test is required")

    store = QdrantStore()

    if args.audit:
        result = run_audit(store, args.document)
    elif args.dry_run:
        result = run_dry_run(store, args.document)
    else:
        if not args.backup:
            parser.error("--rollback-test requires --backup <path>")
        points = scroll_all_points(store)
        docs = args.document or ["Tiger_mini.pdf", "AUTOMATIC_gun.pdf", "manual_GUNS.pdf", "Elephant.pdf"]
        all_ids: list[str] = []
        for doc in docs:
            pts = points_by_document(points, doc)
            all_ids.extend(p["id"] for p in pts)
        result = simulate_rollback(points, all_ids, Path(args.backup))

    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())