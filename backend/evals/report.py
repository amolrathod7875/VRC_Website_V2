"""Phase 10 evaluation report generator.

Writes machine-readable JSON and human-readable Markdown reports.
"""
from __future__ import annotations

import json
import logging
import os
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List

from evals.case_schema import EvalCase
from evals.runner import EvalRun

logger = logging.getLogger(__name__)


def _safe_float(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return round(float(value), 4)
    return None


def generate_json_report(run: EvalRun, path: str) -> Dict[str, Any]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    summary = run.summarize()
    failures = [r for r in run.results if not r.get("pass")]

    critical = [r for r in failures if "CRITICAL" in (r.get("failures") or [])]
    # Derive severity from cases
    severity_map: Dict[str, str] = {c.id: c.severity or "MEDIUM" for c in run.cases}
    for r in failures:
        sev = severity_map.get(r.get("case_id", ""), "MEDIUM")
        r["severity"] = sev

    high = [r for r in failures if severity_map.get(r.get("case_id", "")) == "HIGH"]
    medium = [r for r in failures if severity_map.get(r.get("case_id", "")) == "MEDIUM"]
    low = [r for r in failures if severity_map.get(r.get("case_id", "")) == "LOW"]

    wrong_product = [r for r in failures if "product expected=" in " ".join(r.get("failures", []))]
    cross_contam = [r for r in failures if "forbidden facts present:" in " ".join(r.get("failures", []))]
    false_unavail = [r for r in failures if "expected unavailable answer" in " ".join(r.get("failures", []))]
    context_loss = [r for r in failures if "model expected=" in " ".join(r.get("failures", [])) or "product expected=" in " ".join(r.get("failures", []))]

    report: Dict[str, Any] = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_cases": summary["total_cases"],
            "overall_pass_rate": _safe_float(summary["overall_pass_rate"]),
        },
        "summary": summary,
        "failures": {
            "total": len(failures),
            "critical": len(critical),
            "high": len(high),
            "medium": len(medium),
            "low": len(low),
            "wrong_product": len(wrong_product),
            "cross_product_contamination": len(cross_contam),
            "false_unavailable": len(false_unavail),
            "context_loss": len(context_loss),
            "details": failures,
        },
        "qdrant_mode": run.results[0].get("qdrant_mode") if run.results else "unknown",
        "groq_called": any(r.get("groq_called") for r in run.results),
    }

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, default=str)
    logger.info("JSON report written to %s", path)
    return report


def generate_markdown_report(report: Dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    meta = report.get("meta", {})
    summary = report.get("summary", {})
    failures = report.get("failures", {})

    lines = [
        f"# Phase 10 Deterministic RAG Evaluation Report",
        f"",
        f"Generated: {meta.get('generated_at', 'N/A')}",
        f"",
        f"## Executive Summary",
        f"",
        f"- Total cases: **{summary.get('total_cases', 0)}**",
        f"- Passed: **{summary.get('passed', 0)}**",
        f"- Failed: **{summary.get('failed', 0)}**",
        f"- Overall pass rate: **{_safe_float(summary.get('overall_pass_rate', 0)) or 0.0:.2%}**",
        f"- Qdrant mode: **{report.get('qdrant_mode', 'unknown')}**",
        f"- Groq called: **{report.get('groq_called', False)}**",
        f"",
        f"## Pass Rates",
        f"",
        f"| Dimension | Rate |",
        f"|---|---|",
    ]
    for cat, counts in sorted(summary.get("by_category", {}).items()):
        total = counts.get("pass", 0) + counts.get("fail", 0)
        rate = round(counts.get("pass", 0) / total, 4) if total else 0.0
        lines.append(f"| {cat} | {counts.get('pass', 0)}/{total} ({rate:.2%}) |")

    lines.extend([
        f"",
        f"## Failure Breakdown",
        f"",
        f"- Critical: **{failures.get('critical', 0)}**",
        f"- High: **{failures.get('high', 0)}**",
        f"- Medium: **{failures.get('medium', 0)}**",
        f"- Low: **{failures.get('low', 0)}**",
        f"- Wrong product: **{failures.get('wrong_product', 0)}**",
        f"- Cross-product contamination: **{failures.get('cross_product_contamination', 0)}**",
        f"- False unavailable: **{failures.get('false_unavailable', 0)}**",
        f"- Context loss: **{failures.get('context_loss', 0)}**",
        f"",
        f"## Top Failing Cases",
        f"",
    ])

    for r in failures.get("details", [])[:10]:
        case_id = r.get("case_id", "unknown")
        cat = r.get("category", "unknown")
        fails = r.get("failures", [])
        lines.append(f"- **{case_id}** ({cat}): {'; '.join(fails)}")

    lines.extend([
        f"",
        f"## Quality Gate",
        f"",
        f"- CRITICAL failures: {failures.get('critical', 0)} (target: 0)",
        f"- Wrong-product retrieval: {failures.get('wrong_product', 0)} (target: 0)",
        f"- Cross-product contamination: {failures.get('cross_product_contamination', 0)} (target: 0)",
        f"- Overall deterministic pass: {_safe_float(summary.get('overall_pass_rate', 0)) or 0.0:.2%} (target: >= 95%)",
        f"",
    ])

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    logger.info("Markdown report written to %s", path)


def write_reports(run: EvalRun, results_dir: str = "evals/results") -> Dict[str, Any]:
    os.makedirs(results_dir, exist_ok=True)
    json_path = os.path.join(results_dir, "phase10_results.json")
    md_path = os.path.join(results_dir, "phase10_report.md")
    report = generate_json_report(run, json_path)
    generate_markdown_report(report, md_path)
    return report
