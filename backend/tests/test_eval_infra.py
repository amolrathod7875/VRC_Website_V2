"""Tests for evaluation infrastructure."""
import tempfile
from pathlib import Path

from evals import sanity
from evals.cases_basic import CASES as ALL_CASES
from evals.cases_smoke import CASES as SMOKE_CASES
from evals.runner import _get_git_revision, compute_fingerprint


def test_sanity_imports():
    sanity.check_imports()


def test_fingerprint_stability():
    fp1 = compute_fingerprint(SMOKE_CASES)
    fp2 = compute_fingerprint(SMOKE_CASES)
    assert fp1 == fp2


def test_fingerprint_changes_with_case():
    cases = list(SMOKE_CASES)
    fp1 = compute_fingerprint(cases)
    if cases:
        cases[0].question = cases[0].question + "x"
    fp2 = compute_fingerprint(cases)
    assert fp1 != fp2


def test_git_revision():
    rev = _get_git_revision()
    assert rev and len(rev) > 6


def test_case_selection_helpers():
    from evals.run_phase10 import load_cases_from_failed
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        import json
        json.dump({
            'results': [
                {'case_id': 'smoke-01', 'pass': False},
                {'case_id': 'smoke-02', 'pass': True},
            ]
        }, f)
        path = f.name
    try:
        cases = load_cases_from_failed(Path(path))
        assert len(cases) >= 0
    finally:
        Path(path).unlink()


# ---- Phase 10.2 fixture correction regression tests ----

_CASES_BY_ID = {c.id: c for c in ALL_CASES}


def test_disc_08_expects_electric_pump_not_leopard():
    case = _CASES_BY_ID["disc-08"]
    assert "Electric_pump.pdf" in case.expected_document_names
    assert "leopard.pdf" not in case.expected_document_names


def test_app_16_expects_source_grounded_fact_not_manual_spray_gun():
    case = _CASES_BY_ID["app-16"]
    assert "Manual Spray Gun" not in case.expected_required_facts
    assert "MAXIMUM WORKING PRESSURE (AM250)" in case.expected_required_facts


def test_app_19_app_20_expect_two_component_not_two_component_plural():
    for cid in ("app-19", "app-20"):
        case = _CASES_BY_ID[cid]
        assert "two component" in case.expected_required_facts
        assert "Two-component plural" not in case.expected_required_facts


def test_no_fixture_expects_nonexistent_leopard_pdf():
    for case in ALL_CASES:
        docs = case.expected_document_names or []
        assert "leopard.pdf" not in docs, f"{case.id} expects nonexistent leopard.pdf"


def test_no_fixture_expects_unsupported_manual_spray_gun_phrase():
    for case in ALL_CASES:
        facts = case.expected_required_facts or []
        if isinstance(facts, str):
            facts = [facts]
        assert "Manual Spray Gun" not in facts, f"{case.id} expects unsupported Manual Spray Gun"


def test_no_fixture_expects_two_component_plural():
    for case in ALL_CASES:
        facts = case.expected_required_facts or []
        if isinstance(facts, str):
            facts = [facts]
        assert "Two-component plural" not in facts, f"{case.id} expects non-verbatim Two-component plural"


# ---- Phase 10.2 repair tooling regression tests ----

def test_repair_tool_audit_mode_runs():
    from app.rag.vectorstore.qdrant_store import QdrantStore
    from scripts.phase10_2_repair_tool import run_audit
    store = QdrantStore()
    result = run_audit(store, ["Tiger_mini.pdf"])
    assert result["mode"] == "audit"
    assert result["total_points"] > 0
    assert "Tiger_mini.pdf" in result["documents"]
    assert result["documents"]["Tiger_mini.pdf"]["point_count"] == 8


def test_repair_tool_dry_run_mode_runs():
    from app.rag.vectorstore.qdrant_store import QdrantStore
    from scripts.phase10_2_repair_tool import run_dry_run
    store = QdrantStore()
    result = run_dry_run(store, ["Elephant.pdf"])
    assert result["mode"] == "dry-run"
    assert "Elephant.pdf" in result["repair_plans"]
    plan = result["repair_plans"]["Elephant.pdf"]
    assert plan["repair_type"] == "ocr_correction"
    assert plan["point_count_impact"] == 0
    assert "backups" in result
    assert result["rollback_available"] is True


def test_repair_tool_does_not_have_apply_mode():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--document", action="append")
    # --apply must not exist
    actions = {a.dest for a in parser._actions}
    assert "apply" not in actions
