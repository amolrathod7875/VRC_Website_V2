"""Phase 10 deterministic RAG evaluation tests.

Runs the full :mod:`evals` suite against the live Qdrant store and
PostgreSQL catalogue resolver without calling Groq.

Markers:
- ``live_llm``: tests that require a live LLM (skipped unless quota available).
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from evals.cases_basic import CASES
from evals.evaluator import RagEvaluator
from evals.mock_generation import MockGenerationService
from evals.runner import EvalRun


RESULTS_DIR = Path(__file__).resolve().parent.parent / "evals" / "results"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def evaluator() -> RagEvaluator:
    return RagEvaluator(mock_generator=MockGenerationService())


@pytest.mark.timeout(3600)
def test_phase10_full_deterministic_evaluation(evaluator: RagEvaluator) -> None:
    async def _run() -> dict:
        run = EvalRun(CASES, evaluator)
        results = await run.run()
        return {
            "results": results,
            "summary": run.summarize(),
        }

    data = asyncio.get_event_loop().run_until_complete(_run())
    results = data["results"]
    summary = data["summary"]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = RESULTS_DIR / "phase10_results.json"
    md_path = RESULTS_DIR / "phase10_report.md"

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "meta": {"generated_at": "baseline"},
                "summary": summary,
                "results": results,
            },
            fh,
            indent=2,
            default=str,
        )

    total = summary["total_cases"]
    passed = summary["passed"]
    failed = summary["failed"]
    rate = summary["overall_pass_pass_rate"] = summary.get("overall_pass_rate", 0.0)

    lines = [
        "# Phase 10 Deterministic RAG Evaluation Baseline",
        "",
        f"- Total cases: **{total}**",
        f"- Passed: **{passed}**",
        f"- Failed: **{failed}**",
        f"- Overall pass rate: **{rate:.2%}**",
        "",
        "## Pass Rates by Category",
        "",
        "| Category | Pass | Fail | Rate |",
        "|---|---|---|---|",
    ]
    for cat, counts in sorted(summary.get("by_category", {}).items()):
        p = counts.get("pass", 0)
        f = counts.get("fail", 0)
        t = p + f
        r = p / t if t else 0.0
        lines.append(f"| {cat} | {p} | {f} | {r:.2%} |")
    lines.extend([
        "",
        "## Quality Gate",
        "",
        f"- CRITICAL failures: {sum(1 for r in results if any('CRITICAL' in str(f) for f in r.get('failures', [])))}",
        f"- Wrong-product: {sum(1 for r in results if any('product expected=' in str(f) for f in r.get('failures', [])))}",
        f"- Cross-product contamination: {sum(1 for r in results if any('forbidden facts present:' in str(f) for f in r.get('failures', [])))}",
        f"- Overall pass rate: {rate:.2%} (target >= 95%)",
        "",
        f"JSON report: {json_path}",
        f"Markdown report: {md_path}",
    ])
    md_path.write_text("\n".join(lines), encoding="utf-8")

    assert total >= 150, f"Expected >= 150 cases, got {total}"
    qdrant_modes = {r.get("qdrant_mode") for r in results}
    assert qdrant_modes.issubset({"real", "mock", "error"}), f"Unexpected qdrant modes: {qdrant_modes}"


@pytest.mark.live_llm
def test_live_llm_marker_skipped() -> None:
    pytest.skip("Live-LLM tests require GROQ_API_KEY and available quota")
