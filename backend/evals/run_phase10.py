"""Standalone Phase 10 evaluation runner with extended timeout.

Runs the full evaluation suite outside of pytest to allow a longer timeout.
"""
import asyncio
import json
from pathlib import Path

from evals.runner import EvalRun
from evals.evaluator import RagEvaluator
from evals.cases_basic import CASES

RESULTS_DIR = Path(__file__).resolve().parent.parent / "evals" / "results"


async def main():
    evaluator = RagEvaluator()
    run = EvalRun(CASES, evaluator)
    results = await run.run()
    summary = run.summarize()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = RESULTS_DIR / "phase10_results.json"
    md_path = RESULTS_DIR / "phase10_report.md"

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(
            {"meta": {"generated_at": "baseline"}, "summary": summary, "results": results},
            fh,
            indent=2,
            default=str,
        )

    total = summary["total_cases"]
    passed = summary["passed"]
    failed = summary["failed"]
    rate = summary.get("overall_pass_rate", 0.0)

    lines = ["# Phase 10 Deterministic RAG Evaluation Baseline", "",
             f"- Total cases: **{total}**",
             f"- Passed: **{passed}**",
             f"- Failed: **{failed}**",
             f"- Overall pass rate: **{rate:.2%}**",
             "", "## Pass Rates by Category", "", "| Category | Pass | Fail | Rate |", "|---|---|---|---|"]
    for cat, counts in sorted(summary.get("by_category", {}).items()):
        p = counts.get("pass", 0)
        f = counts.get("fail", 0)
        t = p + f
        r = p / t if t else 0.0
        lines.append(f"| {cat} | {p} | {f} | {r:.2%} |")

    lines.extend([
        "", "## Quality Gate", "",
        f"- CRITICAL failures: {sum(1 for r in results if any('CRITICAL' in str(f) for f in r.get('failures', [])))}",
        f"- Wrong-product: {sum(1 for r in results if any('product expected=' in str(f) for f in r.get('failures', [])))}",
        f"- Cross-product contamination: {sum(1 for r in results if any('forbidden facts present:' in str(f) for f in r.get('failures', [])))}",
        f"- Overall pass rate: {rate:.2%} (target >= 95%)", "",
        f"JSON report: {json_path}",
        f"Markdown report: {md_path}",
    ])
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nTotal: {total}, Passed: {passed}, Failed: {failed}, Rate: {rate:.2%}")
    print(f"Qdrant mode: mock={summary}")


if __name__ == "__main__":
    asyncio.run(main())
