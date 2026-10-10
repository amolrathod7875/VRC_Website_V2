"""Phase 10 evaluation runner.

Aggregates :class:`EvalCase` results across categories and products.
"""
from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from typing import Any, Dict, List, Optional

from evals.case_schema import EvalCase
from evals.evaluator import RagEvaluator

logger = logging.getLogger(__name__)


class EvalRun:
    def __init__(self, cases: List[EvalCase], evaluator: Optional[RagEvaluator] = None) -> None:
        self.cases = cases
        self.evaluator = evaluator or RagEvaluator()
        self.results: List[Dict[str, Any]] = []

    async def run(self) -> List[Dict[str, Any]]:
        self.results = []
        for case in self.cases:
            try:
                result = await self.evaluator.evaluate(case)
            except Exception as exc:
                result = {
                    "case_id": case.id,
                    "category": case.category,
                    "question": case.question,
                    "classified_intent": None,
                    "resolved_product_slug": None,
                    "resolved_model": None,
                    "active_context": {},
                    "applied_filter": {},
                    "augmented_query": case.question,
                    "retrieved_chunks": [],
                    "retrieved_chunk_ids": [],
                    "retrieved_content_types": [],
                    "retrieved_documents": [],
                    "selected_chunks": [],
                    "sources": [],
                    "answer": f"EVALUATOR_ERROR:{exc}",
                    "catalogues": [],
                    "show_sources": False,
                    "groq_called": False,
                    "generation_provider": "error",
                    "qdrant_mode": "error",
                    "retrieval": {},
                    "error": str(exc),
                    "pass": False,
                    "failures": [f"evaluator exception: {exc}"],
                }
            passed, failures = self._evaluate(case, result)
            result["pass"] = passed
            result["failures"] = failures
            self.results.append(result)
        return self.results

    def _evaluate(self, case: EvalCase, result: Dict[str, Any]) -> tuple[bool, List[str]]:
        from evals.assertions import evaluate_case
        return evaluate_case(case, result)

    def summarize(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("pass"))
        failed = total - passed

        by_category: Dict[str, Dict[str, int]] = defaultdict(lambda: {"pass": 0, "fail": 0})
        by_product: Dict[str, Dict[str, int]] = defaultdict(lambda: {"pass": 0, "fail": 0})
        by_severity: Dict[str, Dict[str, int]] = defaultdict(lambda: {"pass": 0, "fail": 0})

        severity_map: Dict[str, str] = {}
        for case in self.cases:
            severity_map[case.id] = case.severity or "MEDIUM"

        for r in self.results:
            cat = r.get("category") or "unknown"
            by_category[cat]["pass" if r.get("pass") else "fail"] += 1
            sev = severity_map.get(r.get("case_id", ""), "MEDIUM")
            by_severity[sev]["pass" if r.get("pass") else "fail"] += 1
            prod = (r.get("active_context") or {}).get("product_slug") or "unknown"
            by_product[prod]["pass" if r.get("pass") else "fail"] += 1

        return {
            "total_cases": total,
            "passed": passed,
            "failed": failed,
            "overall_pass_rate": round(passed / total, 4) if total else 0.0,
            "by_category": dict(by_category),
            "by_product": dict(by_product),
            "by_severity": dict(by_severity),
        }