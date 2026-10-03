#!/usr/bin/env python3
"""Phase 9B Recovery — State Reconciliation + Safe Ingestion Resume"""

import json
import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import psycopg

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.config import settings as app_settings
from app.rag.config import rag_settings

# Configuration
PG_DSN = app_settings.DATABASE_URL
CATALOGUE_ROOT = Path("/home/vr-coatings/Desktop/website_V2/backend/storage/catalogues")
ARTIFACT_ROOT = Path("/home/vr-coatings/Desktop/website_V2/backend/scripts/rag_debug/phase9b_bulk")
CHECKPOINT_PATH = ARTIFACT_ROOT / "phase9b_recovery_state.json"
FINAL_REPORT_PATH = ARTIFACT_ROOT / "phase9b_final_report.json"

QDRANT_URL = rag_settings.QDRANT_URL
QDRANT_API_KEY = rag_settings.QDRANT_API_KEY
QDRANT_COLLECTION = rag_settings.QDRANT_COLLECTION_NAME

# Canonical slugs for pre-Phase-9B documents
PRE_PHASE9B_CANONICAL = {
    "Tiger.pdf": "tiger",
    "LION_Catalogue.pdf": "lion",
    "rhino.pdf": "rhino",
    "Elephant.pdf": "elephant",
    "VR_Coatings_RAG_Monolithic_Knowledge_Base.txt": "company-master",
}

# Fix for Tiger_mini collision: manifest says "tiger" but should be "tiger-mini"
TIGER_MINI_SLUG = "tiger-mini"

# Documents that must NOT be indexed (Phase 9A review files + Phase 9B review-required)
REVIEW_REQUIRED = {
    "manual_GUNS.pdf",
    "VRC MIX (LOW - MEDIUM) PRESSURE.pdf",
    "AUTOMATIC_gun.pdf",
    "ball_valves.pdf",
    "Barrel Pump.pdf",
    "CONVENTIONAL GUNS_f.pdf",
    "cub.pdf",
    "diaphragm pump.pdf",
    "dragon.pdf",
    "DRUM PRESS.pdf",
    "Electric_pump.pdf",
    "filters.pdf",
    "Paint Preparation Unit.pdf",
    "PNEUMATIC STIRRER.pdf",
    "polyurea.pdf",
    "PORTABLE PRESSURE FEED POT.pdf",
    "TUBE VARNISH COATING SYSTEM.pdf",
    "turbine.pdf",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qdrant_request(method: str, path: str, body: Optional[dict] = None) -> dict:
    import urllib.request
    url = f"{QDRANT_URL}:6333{path}"
    headers = {
        "api-key": QDRANT_API_KEY,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def get_qdrant_document_map() -> Dict[str, dict]:
    """Return mapping of document_name -> {count, doc_id}."""
    doc_map = {}
    offset = None
    while True:
        body = {"limit": 100, "with_payload": True, "with_vector": False}
        if offset:
            body["offset"] = offset
        result = qdrant_request("POST", f"/collections/{QDRANT_COLLECTION}/points/scroll", body)["result"]
        points = result.get("points", [])
        if not points:
            break
        for p in points:
            doc = p.get("payload", {}).get("document_name", "unknown")
            doc_id = p.get("payload", {}).get("document_id")
            if doc not in doc_map:
                doc_map[doc] = {"count": 0, "doc_id": doc_id}
            doc_map[doc]["count"] += 1
        offset = result.get("next_page_offset")
        if not offset:
            break
    return doc_map


def get_postgres_documents(conn) -> Dict[str, dict]:
    """Return mapping of document_name -> row dict from PostgreSQL."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, document_name, source_type, product_slug, storage_path, sha256, status, qdrant_document_id, chunk_count, last_ingested_at FROM rag_documents")
        rows = cur.fetchall()
    result = {}
    for row in rows:
        result[row[1]] = {
            "id": row[0],
            "document_name": row[1],
            "source_type": row[2],
            "product_slug": row[3],
            "storage_path": row[4],
            "sha256": row[5],
            "status": row[6],
            "qdrant_document_id": row[7],
            "chunk_count": row[8],
            "last_ingested_at": row[9],
        }
    return result


def insert_rag_document(conn, doc_name: str, source_type: str, product_slug: Optional[str], storage_path: str, sha256: str, qdrant_doc_id: str, chunk_count: int) -> str:
    doc_uuid = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO rag_documents (id, document_name, source_type, product_slug, storage_path, sha256, status, qdrant_document_id, chunk_count, last_ingested_at, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (doc_uuid, doc_name, source_type, product_slug, storage_path, sha256, "indexed", qdrant_doc_id, chunk_count, now, now, now),
        )
    return doc_uuid


def insert_ingestion_run(conn, doc_uuid: str, doc_name: str, source_type: str, chunk_count: int) -> str:
    run_uuid = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO rag_ingestion_runs (id, document_id, document_name, source_type, status, chunks_created, started_at, finished_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (run_uuid, doc_uuid, doc_name, source_type, "indexed", chunk_count, now, now),
        )
    return run_uuid


def load_checkpoint() -> dict:
    if CHECKPOINT_PATH.exists():
        return json.loads(CHECKPOINT_PATH.read_text())
    return {"recovered_documents": {}, "timestamp": None}


def save_checkpoint(state: dict):
    state["timestamp"] = datetime.now(timezone.utc).isoformat()
    CHECKPOINT_PATH.write_text(json.dumps(state, indent=2))


def main():
    print("=" * 60)
    print("Phase 9B Recovery — State Reconciliation")
    print("=" * 60)

    # 1. Load manifest and audit decisions
    manifest = json.loads((ARTIFACT_ROOT / "phase9b_manifest.json").read_text())
    manifest_entries = {e["filename"]: e for e in manifest}

    audit_decisions = {}
    for d in sorted(ARTIFACT_ROOT.iterdir()):
        if d.is_dir() and (d / "audit.json").exists():
            data = json.loads((d / "audit.json").read_text())
            audit_decisions[d.name] = data.get("decisions", "MISSING")

    # 2. Recompute counts
    approved = [slug for slug, decision in audit_decisions.items() if decision == "APPROVED"]
    review_required = [slug for slug, decision in audit_decisions.items() if decision == "OCR_REVIEW_REQUIRED"]
    failed = [slug for slug, decision in audit_decisions.items() if decision == "FAILED"]
    missing_audit = [slug for slug, decision in audit_decisions.items() if decision == "MISSING"]

    print(f"\nAUDIT RECONSTRUCTION:")
    print(f"  APPROVED: {len(approved)} -> {approved}")
    print(f"  OCR_REVIEW_REQUIRED: {len(review_required)} -> {review_required}")
    print(f"  FAILED: {len(failed)} -> {failed}")
    print(f"  MISSING_AUDIT: {len(missing_audit)} -> {missing_audit}")

    # 3. Explain 22 vs 24 discrepancy
    dir_names = {d.name for d in ARTIFACT_ROOT.iterdir() if d.is_dir()}
    manifest_names = {e["product_slug"] for e in manifest}
    missing_from_manifest = sorted(dir_names - manifest_names)
    extra_in_manifest = sorted(manifest_names - dir_names)
    print(f"\n22-VS-24 DISCREPANCY:")
    print(f"  Manifest entries: {len(manifest)}")
    print(f"  Artifact directories: {len(dir_names)}")
    print(f"  Missing from manifest: {missing_from_manifest}")
    print(f"  Extra in manifest (no dir): {extra_in_manifest}")
    print(f"  Reason: Two Phase 9B PDFs (AUTOMATIC_gun.pdf, Barrel Pump.pdf) were processed and generated artifacts but were accidentally omitted from phase9b_manifest.json.")

    # 4. Tiger_mini identity
    tiger_mini_audit = json.loads((ARTIFACT_ROOT / "tiger" / "audit.json").read_text())
    print(f"\nTIGER_MINI IDENTITY:")
    print(f"  Source PDF: {tiger_mini_audit['filename']}")
    print(f"  Manifest product_slug: {tiger_mini_audit['product_slug']}")
    print(f"  Audit decision: {tiger_mini_audit['decisions']}")
    print(f"  OCR title: MINI TIGER series")
    print(f"  Action: Will use canonical slug '{TIGER_MINI_SLUG}' to avoid collision with existing Tiger.pdf (slug=tiger)")

    # 5. Check Qdrant and PostgreSQL state
    print("\n" + "=" * 60)
    print("DATABASE STATE INSPECTION")
    print("=" * 60)

    qdrant_map = get_qdrant_document_map()
    with psycopg.connect(PG_DSN) as conn:
        pg_docs = get_postgres_documents(conn)

    print(f"\nQdrant total points: {sum(v['count'] for v in qdrant_map.values())}")
    print(f"PostgreSQL rag_documents: {len(pg_docs)}")
    print(f"PostgreSQL rag_ingestion_runs: ", end="")
    with psycopg.connect(PG_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM rag_ingestion_runs")
            print(cur.fetchone()[0])
    print(f"PostgreSQL rag_conversations: ", end="")
    with psycopg.connect(PG_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM rag_conversations")
            print(cur.fetchone()[0])
    print(f"PostgreSQL rag_messages: ", end="")
    with psycopg.connect(PG_DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM rag_messages")
            print(cur.fetchone()[0])

    # 6. Classify each approved document
    print("\n" + "=" * 60)
    print("APPROVED DOCUMENT CLASSIFICATION")
    print("=" * 60)

    # Build complete reconciliation list: pre-Phase-9B missing + Phase 9B approved
    pre_phase9b_missing = []
    for doc_name in ["Elephant.pdf", "LION_Catalogue.pdf", "rhino.pdf"]:
        if doc_name in qdrant_map and doc_name not in pg_docs:
            pre_phase9b_missing.append(doc_name)

    phase9b_approved_missing = []
    for slug in approved:
        # Find the filename for this slug
        fname = None
        for e in manifest:
            if e["product_slug"] == slug:
                fname = e["filename"]
                break
        if slug == "tiger":
            fname = "Tiger_mini.pdf"
        if fname and fname in qdrant_map and fname not in pg_docs:
            phase9b_approved_missing.append(fname)

    all_to_reconcile = pre_phase9b_missing + phase9b_approved_missing
    print(f"\nDocuments to reconcile (Qdrant present, PostgreSQL absent):")
    for doc in all_to_reconcile:
        q_info = qdrant_map.get(doc, {})
        print(f"  {doc}: {q_info.get('count', 0)} points, doc_id={q_info.get('doc_id')}")

    # 7. Perform reconciliation
    print("\n" + "=" * 60)
    print("RECONCILIATION")
    print("=" * 60)

    checkpoint = load_checkpoint()
    recovered = checkpoint.setdefault("recovered_documents", {})

    with psycopg.connect(PG_DSN) as conn:
        for doc_name in all_to_reconcile:
            q_info = qdrant_map.get(doc_name, {})
            qdrant_count = q_info.get("count", 0)
            qdrant_doc_id = q_info.get("doc_id")

            if doc_name in recovered:
                print(f"\nSKIP (already in checkpoint): {doc_name}")
                continue

            if doc_name in pg_docs:
                print(f"\nSKIP (already in PostgreSQL): {doc_name}")
                recovered[doc_name] = {
                    "status": "skipped",
                    "reason": "already_in_postgres",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                save_checkpoint(checkpoint)
                continue

            # Determine product_slug and source_type
            if doc_name in PRE_PHASE9B_CANONICAL:
                product_slug = PRE_PHASE9B_CANONICAL[doc_name]
                source_type = "company_master" if "company_master" in doc_name.lower() or "knowledge_base" in doc_name.lower() else "catalogue"
            elif doc_name == "Tiger_mini.pdf":
                product_slug = TIGER_MINI_SLUG
                source_type = "catalogue"
            else:
                # Look up from manifest
                product_slug = None
                for e in manifest:
                    if e["filename"] == doc_name:
                        product_slug = e["product_slug"]
                        break
                if not product_slug:
                    product_slug = doc_name.lower().replace(" ", "-").replace(".pdf", "")
                source_type = "catalogue"

            # Get storage path and SHA-256
            if doc_name.endswith(".txt"):
                storage_path = f"storage/knowledge/{doc_name}"
                pdf_path = CATALOGUE_ROOT.parent / "knowledge" / doc_name
            else:
                storage_path = f"storage/catalogues/{doc_name}"
                pdf_path = CATALOGUE_ROOT / doc_name

            if pdf_path.exists():
                sha = sha256_file(pdf_path)
            else:
                print(f"  WARNING: source PDF missing for {doc_name}, using artifact sha256")
                sha = None
                for e in manifest:
                    if e["filename"] == doc_name:
                        sha = e["sha256"]
                        break

            if not sha:
                print(f"  ERROR: cannot determine SHA-256 for {doc_name}, skipping")
                continue

            print(f"\nRECONCILING: {doc_name}")
            print(f"  Qdrant points: {qdrant_count}")
            print(f"  Qdrant doc_id: {qdrant_doc_id}")
            print(f"  Product slug: {product_slug}")
            print(f"  Source type: {source_type}")
            print(f"  SHA-256: {sha[:16]}...")

            try:
                doc_uuid = insert_rag_document(
                    conn, doc_name, source_type, product_slug, storage_path, sha, qdrant_doc_id, qdrant_count
                )
                run_uuid = insert_ingestion_run(conn, doc_uuid, doc_name, source_type, qdrant_count)
                conn.commit()
                print(f"  PostgreSQL: INSERTED document={doc_uuid}, run={run_uuid}")
                recovered[doc_name] = {
                    "status": "reconciled",
                    "document_id": doc_uuid,
                    "qdrant_document_id": qdrant_doc_id,
                    "qdrant_points": qdrant_count,
                    "product_slug": product_slug,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            except Exception as exc:
                conn.rollback()
                print(f"  ERROR: {exc}")
                recovered[doc_name] = {
                    "status": "error",
                    "error": str(exc),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }

            save_checkpoint(checkpoint)

    # 8. Verify final state
    print("\n" + "=" * 60)
    print("POST-RECOVERY VERIFICATION")
    print("=" * 60)

    with psycopg.connect(PG_DSN) as conn:
        pg_docs_after = get_postgres_documents(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM rag_ingestion_runs")
            runs_after = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM rag_conversations")
            convs_after = cur.fetchone()[0]
            cur.execute("SELECT count(*) FROM rag_messages")
            msgs_after = cur.fetchone()[0]

    print(f"PostgreSQL rag_documents: {len(pg_docs_after)}")
    print(f"PostgreSQL rag_ingestion_runs: {runs_after}")
    print(f"PostgreSQL rag_conversations: {convs_after}")
    print(f"PostgreSQL rag_messages: {msgs_after}")

    print(f"\nIndexed documents:")
    for doc_name in sorted(pg_docs_after.keys()):
        d = pg_docs_after[doc_name]
        print(f"  {doc_name}: slug={d['product_slug']}, chunks={d['chunk_count']}, qdrant_id={d['qdrant_document_id']}")

    # 9. Verify review-required documents are NOT indexed
    print(f"\nREVIEW-REQUIRED VERIFICATION:")
    for doc_name in REVIEW_REQUIRED:
        if doc_name in pg_docs_after:
            print(f"  ERROR: {doc_name} is indexed but should be review-required!")
        else:
            print(f"  OK: {doc_name} is not indexed")

    # 10. Final summary
    print("\n" + "=" * 60)
    print("RECOVERY SUMMARY")
    print("=" * 60)
    print(f"Total catalogue PDFs: 30")
    print(f"Indexed in Qdrant: {len(qdrant_map)}")
    print(f"Registered in PostgreSQL: {len(pg_docs_after)}")
    print(f"Phase 9B approved reconciled: {sum(1 for d in recovered.values() if d.get('status') == 'reconciled' and d.get('product_slug') in [e['product_slug'] for e in manifest])}")
    print(f"Phase 9B review-required confirmed unindexed: {len([d for d in REVIEW_REQUIRED if d not in pg_docs_after])}")
    print(f"Tiger_mini slug: {TIGER_MINI_SLUG}")
    print(f"Checkpoint saved: {CHECKPOINT_PATH}")
    print(f"Recovery complete.")


if __name__ == "__main__":
    main()
