"""Standalone Phase 10 evaluation runner with extended timeout.

Runs the full evaluation suite outside of pytest to allow a longer timeout.
"""
import argparse
import asyncio
import json
from pathlib import Path
import sys

from evals.runner import EvalRun, compute_fingerprint, _get_git_revision
from evals.evaluator import RagEvaluator
from evals.cases_basic import CASES as ALL_CASES
from evals.cases_smoke import CASES as SMOKE_CASES
from evals.case_schema import EvalCase
from evals.sanity import check_imports

RESULTS_DIR = Path(__file__).resolve().parent.parent / "evals" / "results"


def load_cases_from_failed(report_path: Path) -> list[EvalCase]:
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        failed_ids = []
        for r in data.get("results", []):
            if not r.get("pass"):
                failed_ids.append(r.get("case_id"))
        by_id = {c.id: c for c in ALL_CASES}
        cases = []
        for fid in failed_ids:
            if fid in by_id:
                cases.append(by_id[fid])
        return cases
    except Exception as exc:
        print(f"Failed to load failed cases from {report_path}: {exc}", file=sys.stderr)
        return []


async def main():
    check_imports()

    parser = argparse.ArgumentParser(description="Phase 10 evaluation runner")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--category", action="append", help="Filter by category")
    parser.add_argument("--case", action="append", help="Run specific case ID")
    parser.add_argument("--failed-from", type=str, help="Run failed cases from previous report")
    parser.add_argument("--all", action="store_true", help="Run all cases")
    parser.add_argument("--output", type=str, help="Output JSON path")
    parser.add_argument("--concurrency", type=int, default=1, help="Concurrency level")
    args = parser.parse_args()

    cases: list[EvalCase] = ALL_CASES

    if args.smoke:
        cases = SMOKE_CASES
    if args.failed_from:
        cases = load_cases_from_failed(Path(args.failed_from))
    if args.category:
        cats = set(c.lower() for c in args.category)
        cases = [c for c in cases if c.category.lower() in cats]
    if args.case:
        case_ids = set(args.case)
        cases = [c for c in cases if c.id in case_ids]
    if args.all and not any([args.smoke, args.failed_from, args.category, args.case]):
        cases = ALL_CASES

    # If no specific mode selected, run all by default
    if not any([args.smoke, args.failed_from, args.category, args.case, args.all]):
        cases = ALL_CASES

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    revision = _get_git_revision()
    fp = compute_fingerprint(cases, extra={"revision": revision, "mode": "run_phase10"})
    checkpoint_path = RESULTS_DIR / f"checkpoint_{fp}.json"
    progress_path = RESULTS_DIR / "phase10_progress.json"

    evaluator = RagEvaluator()
    run = EvalRun(cases, evaluator, checkpoint_path=checkpoint_path, run_fingerprint=fp, concurrency=args.concurrency)
    results = await run.run()
    summary = run.summarize()

    json_path = Path(args.output) if args.output else (RESULTS_DIR / "phase10_results.json")
    md_path = json_path.with_suffix(".md") if json_path.suffix else (json_path.parent / f"{json_path.name}.md")
    if args.output and json_path.suffix != ".md":
        md_path = json_path.parent / f"{json_path.stem}_report.md"
    if not args.output:
        md_path = RESULTS_DIR / "phase10_report.md"

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(
            {"meta": {"generated_at": "baseline", "complete": len(results) == len(cases), "revision": revision}, "summary": summary, "results": results},
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


if __name__ == "__main__":
    asyncio.run(main())
