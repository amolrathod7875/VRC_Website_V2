# Phase 10.2 — Qdrant Data Quality Audit Report

## A. Starting Git branch and commit

- Branch: `phase10-2-data-quality`
- Start commit: `c58247c` (Merge pull request #1 from amolrathod7875/phase10r-postgresql-free-rag)
- Previous Phase 10 branch (`phase10r-postgresql-free-rag`) merged into `main` via PR #1 at `c58247c`.
- Local `main` was fast-forwarded to `origin/main` (`c58247c`) before branching.

## B. New branch created

- `phase10-2-data-quality` created from verified `main` (`c58247c`), working tree clean.
- Not pushed, not merged.

## C. Merged application's regression results

- Fast unit tests (88): **88 passed**
  - `test_conversation_validation`, `test_chat_greeting`, `test_chat_general`, `test_chat_api_no_db`, `test_rag_conversation_service`, `test_rag_evidence_guard`, `test_rag_generation`, `test_domain_guard`
- FastAPI verified working without PostgreSQL (all chat/no-db tests pass; PostgreSQL infrastructure removed in Phase 10R).
- Phase 10 evaluation code present under `backend/evals/` (`run_phase10.py`, `runner.py`, `evaluator.py`, `assertions.py`, `cases_basic.py`, `case_schema.py`, `mock_generation.py`, `report.py`, `sanity.py`, `staged_evaluator.py`).
- Targeted eval on the 10 known failing cases: **1 passed / 9 failed** (`disc-10` now passes; retrieval shows non-determinism across runs).
- Adjacent passing cases run for stability: `identity-06`, `mp-09`, `mp-10`, `technical-22`, `technical-23`, `technical-24` pass; `mp-08` flaky (forbidden Elephant ratios leak — related to cmp-01 root cause).
- Frontend build: not executed in this phase (no frontend changes).

## D. Qdrant point count

- Collection: `vr_coatings_knowledge`
- URL: `https://37832e36-65aa-4fc2-817c-35e534ab5ddb.sa-east-1-0.aws.cloud.qdrant.io`
- **Point count: 5,433** (matches expected historical count)
- Status: green
- 5,185 points are in `VR_Coatings_RAG_Monolithic_Knowledge_Base.txt` (no product_slug, no document_name).
- 248 points across 29 catalogue PDFs.
- 8 points have missing `document_id`.

## E. Inventory of catalogue documents

Full filesystem vs Qdrant inventory saved by `backend/scripts/phase10_2_qdrant_audit.py` (run-only diagnostic; output in `/tmp/kilo/qdrant_inventory.json`).

Relevant target documents (all present on filesystem AND indexed in Qdrant):

| Document | FS bytes | Qdrant points | Qdrant product_slug(s) |
|---|---|---|---|
| Tiger_mini.pdf | 4,014,261 | 8 | tiger-mini |
| AUTOMATIC_gun.pdf | 3,819,494 | 7 | 400b, flamingo, hotmelt, vria, vriad |
| manual_GUNS.pdf | 4,594,954 | 10 | am250, eagle, ext-i, falcon, flamingo, hawk, pole, vrid, vril, wax-spray-gun |
| Electric_pump.pdf | 5,522,897 | 7 | leopard |
| Elephant.pdf | 3,981,529 | 8 | elephant |
| rhino.pdf | 5,365,690 | 17 | rhino |
| VRC - MIX HP.pdf | 6,317,417 | 7 | vrc-mix-hp |
| VRC MIX (LOW - MEDIUM) PRESSURE.pdf | 4,854,938 | 6 | vrc-mix-low-medium-pressure |
| Paint Preparation Unit.pdf | 4,667,189 | 4 | paint-preparation-unit |

Notable metadata observations:
- `leopard.pdf` does NOT exist on filesystem or in Qdrant. Leopard is indexed as `Electric_pump.pdf` (slug `leopard`).
- `Tiger_mini.pdf` points have payload `{document_name, product_slug}` only — **no text field, no chunk_id** (ingestion defect).
- `AUTOMATIC_gun.pdf` has NO `automatic-spray-guns` slug (family slug missing).
- `manual_GUNS.pdf` has NO `manual-spray-guns` slug (family slug missing).

## F. Root cause for each of the 10 failing cases

Eval assertion semantics (`backend/evals/assertions.py`): `assert_required_facts` normalizes text (lowercase, collapse whitespace) and requires each expected fact as a substring (multi-token) or whole-token (single-token). `assert_documents` requires each expected `document_name` (lowercased) to appear among retrieved chunks.

| Case | Question | Root cause | Repair type |
|---|---|---|---|
| disc-08 | Which product is suitable for water based paints? | Eval expects document `leopard.pdf`, but no such file exists. Leopard is indexed as `Electric_pump.pdf` (slug `leopard`) and **is retrieved**. identity-06 already uses `Electric_pump.pdf` for Leopard. | E — evaluator fixture inconsistency (`leopard.pdf` → `Electric_pump.pdf`) |
| disc-10 | Which product is suitable for oil and gas applications? | **Now passes.** Rhino indexed (17 pts, slug `rhino`) and retrieved. Likely flaky/non-deterministic retrieval in the baseline run. | None (data OK) |
| cmp-01 | Compare Rhino and Elephant | Required fact `3:1` missing. Elephant.pdf OCR text (chunk 6) shows `Pressure ratio 2.5:1 2:1 3:] 2:1 2:1` — the `3:]` is an **OCR misread of `3:1`** (type row `3:2000` corresponds to ratio `3:1`). Both docs indexed and retrieved. | C — OCR correction (re-ingest Elephant.pdf) |
| identity-29 | What is Tiger Mini? | `Tiger_mini.pdf` IS indexed (8 pts, slug `tiger-mini`) but points have **no text content** (payload only `document_name`+`product_slug`). Retrieval returns nothing. | B — controlled reingestion of Tiger_mini.pdf |
| identity-30 | What are automatic spray guns? | `AUTOMATIC_gun.pdf` IS indexed (7 pts) but slugs are `[400b, flamingo, hotmelt, vria, vriad]` — **no `automatic-spray-guns` family slug**. Query classifier did not resolve a product slug; semantic search did not surface the doc. | A — metadata correction (add family slug) + identity registry support |
| identity-31 | What are manual spray guns? | `manual_GUNS.pdf` IS indexed (10 pts) but slugs are `[am250, eagle, ext-i, falcon, flamingo, hawk, pole, vrid, vril, wax-spray-gun]` — **no `manual-spray-guns` family slug**. | A — metadata correction (add family slug) + identity registry support |
| technical-21 | What is the pressure ratio of Tiger Mini? | Same as identity-29: `Tiger_mini.pdf` points have no text; fact `Tiger Mini` absent. | B — controlled reingestion of Tiger_mini.pdf |
| app-16 | What is HAWK used for? | `manual_GUNS.pdf` retrieved (HAWK chunk) but text contains only pressure/port specs (`MAXIMUM WORKING PRESSURE (AM250):...`). Phrase `Manual Spray Gun` **does not appear** anywhere in the 10 chunks. | F — evidence genuinely unavailable in source (flag for source review) |
| app-19 | What is VRC MIX HP used for? | `VRC - MIX HP.pdf` retrieved but text says `two component paints` / `two component` — expected fact `Two-component plural` (hyphenated + "plural") **does not match** verbatim. | E — evaluator fixture (fact wording doesn't match source) or F |
| app-20 | What is VRC MIX Low-Medium used for? | `VRC MIX (LOW - MEDIUM) PRESSURE.pdf` retrieved but text says `ELECTRONIC TWO COMPONENT SYSTEM` — expected `Two-component plural` does not match verbatim. | E — evaluator fixture or F |

## G. Original PDF evidence verification

All catalogue PDFs are **scanned/image-based** (no extractable text layer via `pdftotext` — 2 bytes output). Qdrant text is OCR output from ingestion.

- **Elephant.pdf OCR error confirmed**: Chunk 6 table row reads `Type ... 3:2000 ... Pressure ratio ... 3:]` where the source pattern (type `3:2000` → ratio starting with `3`) and sibling rows (`2:1000`→`2.5:1`, `2:2000`→`2:1`) indicate the intended value is `3:1`. Classified as **OCR defect** (type C). Original PDF visibly supports `3:1` by column-alignment pattern, but cannot be re-read without re-OCR since no text layer exists.
- **manual_GUNS.pdf**: No `Manual Spray Gun` phrase in any of the 10 chunks (all pressure/port specifications). app-16's expected fact is genuinely unsupported by the source.
- **VRC - MIX HP.pdf** / **VRC MIX (LOW - MEDIUM) PRESSURE.pdf**: Both contain `two component` / `TWO COMPONENT` but not the hyphenated `Two-component plural`. Source supports the *concept* (two-component system) but not the exact expected string.

Per task guidance: where the PDF does not support the evaluation expectation (app-16, app-19, app-20), these are flagged for **source review** rather than fabricating evidence.

## H. Metadata defects found

1. **Tiger_mini.pdf** — 8 points indexed with `document_name` + `product_slug=tiger-mini` but **no text content** (ingestion/text-extraction failure). Affects identity-29, technical-21.
2. **AUTOMATIC_gun.pdf** — missing family product_slug `automatic-spray-guns`; only model-level slugs `[400b, flamingo, hotmelt, vria, vriad]`. Affects identity-30.
3. **manual_GUNS.pdf** — missing family product_slug `manual-spray-guns`; only model-level slugs. Affects identity-31.
4. **Naming inconsistency** — Leopard indexed as `Electric_pump.pdf` (slug `leopard`) but eval fixture disc-08 expects `leopard.pdf` (no such file). identity-06 correctly uses `Electric_pump.pdf`.

## I. OCR defects found

1. **Elephant.pdf** — table pressure-ratio cell reads `3:]` instead of `3:1` (type row `3:2000`). Affects cmp-01 (missing required fact `3:1`).
   - Pattern evidence: types `[2:1000, 2:2000, 3:2000, 2:4000, 2:6500]` map to ratios `[2.5:1, 2:1, 3:], 2:1, 2:1]`; the `3:2000` row's ratio should begin with `3`, confirming `3:1`.

## J. Missing-document findings

- **No catalogue PDF is missing from the filesystem** — all 29 expected PDFs are present.
- **No target document is absent from Qdrant** — all target docs are indexed.
- The only "missing document" is `leopard.pdf`, which never existed (Leopard = `Electric_pump.pdf`).
- Tiger_mini.pdf points exist but are **text-empty** (functional equivalent of missing content).

## K. Incorrect evaluation expectations, if any

1. **disc-08** — expects `leopard.pdf`; no such file exists. Should be `Electric_pump.pdf` (matches identity-06).
2. **app-19 / app-20** — expect fact `Two-component plural`; source says `two component` / `TWO COMPONENT`. The exact string does not appear. Either the fixture wording is wrong, or the concept is present but not verbatim.
3. **app-16** — expects fact `Manual Spray Gun`; source does not contain it. Genuinely unsupported — flag for source review (type F).
4. **disc-10** — was in the original failing list but now passes; retrieval non-determinism means the failing set is fluid across runs.

## L. Recommended changes for each case

| Case | Recommended change | Type | Risk |
|---|---|---|---|
| disc-08 | Change eval fixture `expected_document_names` from `['Paint Preparation Unit.pdf', 'leopard.pdf']` to `['Paint Preparation Unit.pdf', 'Electric_pump.pdf']` | E | Low |
| disc-10 | No change (passes; likely flaky baseline) | — | — |
| cmp-01 | Re-ingest Elephant.pdf with corrected OCR (`3:]` → `3:1`) OR relax eval to accept `3:]` | C / E | Medium (Qdrant write) |
| identity-29 | Re-ingest Tiger_mini.pdf so points include extracted text | B | Medium (Qdrant write) |
| identity-30 | Add `automatic-spray-guns` product_slug to AUTOMATIC_gun.pdf points; ensure identity registry resolves "automatic spray guns" → that slug | A | Medium (Qdrant write + code) |
| identity-31 | Add `manual-spray-guns` product_slug to manual_GUNS.pdf points; ensure identity registry resolves "manual spray guns" → that slug | A | Medium (Qdrant write + code) |
| technical-21 | Same as identity-29 (re-ingest Tiger_mini.pdf) | B | Medium |
| app-16 | Flag for source review: `Manual Spray Gun` not in manual_GUNS.pdf. Do not fabricate. | F | — |
| app-19 | Flag for review: source says `two component`, fixture expects `Two-component plural`. Correct fixture or accept source wording. | E / F | Low |
| app-20 | Flag for review: source says `TWO COMPONENT`, fixture expects `Two-component plural`. Correct fixture or accept source wording. | E / F | Low |

## M. Safe repair and rollback strategy

For any future Qdrant mutation (types A, B, C):

1. **Before-state backup/export**: Scroll and export all points for the affected document (document_name filter) to a JSON snapshot including IDs, payloads, and vectors.
2. **Exact document IDs and point IDs**: Capture from scroll output before mutation (e.g., Tiger_mini.pdf point IDs, Elephant.pdf point IDs).
3. **Expected point-count impact**:
   - Tiger_mini.pdf reingestion: same 8 points, payloads gain text (point count unchanged).
   - Elephant.pdf reingestion: same 8 points, payload text corrected (point count unchanged).
   - AUTOMATIC_gun.pdf / manual_GUNS.pdf metadata correction: `update_payloads_by_document_id` to add family slug (point count unchanged).
4. **SHA/idempotency handling**: Re-ingestion should be keyed on document SHA256; skip if unchanged. Use `delete_by_document_id` + re-upsert only when content changed.
5. **Parent/child metadata preservation**: For AUTOMATIC_gun.pdf / manual_GUNS.pdf, preserve existing model-level slugs while *adding* family slugs (do not overwrite).
6. **Dry-run verification**: Run `phase10_2_qdrant_audit.py` and `phase10_2_dump_qdrant_text.py` against a staging/Qdrant copy before production; compare before/after inventories.
7. **Rollback procedure**: Re-import the pre-mutation JSON snapshot via `delete_by_document_id` + `upsert_points` with original payloads/vectors.
8. **Verification**: Re-run targeted `python -m evals.run_phase10 --case <id>` for affected cases plus adjacent passing cases to confirm no regression.

Production Qdrant is **safe to repair** (read-only audit performed; no mutations executed). Repairs should be staged and reviewed before execution.

## N. Targeted test results

Failing-case targeted run (`--case disc-08 disc-10 cmp-01 identity-29 identity-30 identity-31 technical-21 app-16 app-19 app-20`):
- **1 passed / 9 failed** (`disc-10` passes; the other 9 fail as analyzed above).

Adjacent stability run (`--case identity-06 mp-08 mp-09 mp-10 technical-22 technical-23 technical-24`):
- **6 passed / 1 failed** (`mp-08` flaky — forbidden Elephant ratios `2.5:1`, `2:1` leak; related to cmp-01 Elephant multi-ratio table).

Full baseline (from prior Phase 10 completion): **207/217 (95.39%)**.

## O. Files changed

New files (diagnostic tooling + documentation):
- `backend/scripts/phase10_2_qdrant_audit.py` — Qdrant metadata vs filesystem audit
- `backend/scripts/phase10_2_dump_qdrant_text.py` — Qdrant OCR text dump per document
- `backend/scripts/PHASE10_2_DATA_QUALITY_REPORT.md` — this report

No production source files modified. No production Qdrant writes performed. No `.env`, API keys, generated reports, or large OCR outputs committed.

## P. Commit hash

Pending commit on branch `phase10-2-data-quality` (not yet committed at report time).

## Q. Exact changes requiring user approval

1. **Commit** the three new files above to `phase10-2-data-quality`.
2. **Do NOT push or merge** (per task instructions).
3. **Future Qdrant repairs** (types A/B/C) require explicit user approval before execution:
   - Re-ingest `Tiger_mini.pdf` (add text to 8 points)
   - Add `automatic-spray-guns` slug to `AUTOMATIC_gun.pdf` points
   - Add `manual-spray-guns` slug to `manual_GUNS.pdf` points
   - Correct Elephant.pdf OCR (`3:]` → `3:1`)
4. **Eval fixture corrections** (type E: disc-08, app-19, app-20) require user approval before changing `backend/evals/cases_basic.py`.

## R. Whether production data is safe to repair

**Yes.** The production Qdrant collection (5,433 points, green status) is intact — this phase performed read-only diagnostics only. No mutations, writes, or deletions were executed. All identified defects are documented with before-state capture guidance and rollback procedures. Repairs should be executed only after explicit user approval, preferably against a staging copy first.

## Recommended next steps (not executed)

1. Commit diagnostic tooling + report to `phase10-2-data-quality`.
2. Review and approve eval fixture corrections (disc-08, app-19, app-20) in `backend/evals/cases_basic.py`.
3. Approve and stage Qdrant metadata repairs (Tiger_mini reingestion, AUTOMATIC_gun/manual_GUNS family slugs, Elephant OCR correction).
4. Re-run targeted eval on the 10 cases after repairs to confirm improvement toward the 207/217 gate.
5. Do not push or merge `phase10-2-data-quality` without separate approval.
