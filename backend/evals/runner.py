"""Phase 10 evaluation runner.

Aggregates :class:`EvalCase` results across categories and products.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from evals.case_schema import EvalCase
from evals.evaluator import RagEvaluator
from evals.sanity import check_imports

logger = logging.getLogger(__name__)


def _get_git_revision() -> str:
    try:
        rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=Path(__file__).resolve().parent.parent).decode().strip()
        return rev
    except Exception:
        return "unknown"


def compute_fingerprint(cases: List[EvalCase], extra: Optional[Dict[str, Any]] = None) -> str:
    data = {"cases": [c.to_dict() for c in cases], "extra": extra or {}}
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


class EvalRun:
    def __init__(
        self,
        cases: List[EvalCase],
        evaluator: Optional[RagEvaluator] = None,
        checkpoint_path: Optional[Path] = None,
        run_fingerprint: Optional[str] = None,
        concurrency: int = 1,
    ) -> None:
        self.cases = cases
        self.evaluator = evaluator or RagEvaluator()
        self.results: List[Dict[str, Any]] = []
        self.checkpoint_path = checkpoint_path
        self.run_fingerprint = run_fingerprint
        self.concurrency = max(1, concurrency)
        self._completed_ids: set[str] = set()
        self._load_checkpoint()

    def _load_checkpoint(self) -> None:
        if not self.checkpoint_path or not self.checkpoint_path.exists():
            return
        try:
            with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("fingerprint") != self.run_fingerprint:
                logger.warning("Checkpoint fingerprint mismatch; ignoring")
                return
            for r in data.get("results", []):
                case_id = r.get("case_id")
                if case_id:
                    self._completed_ids.add(case_id)
                    self.results.append(r)
        except Exception as exc:
            logger.warning("Failed to load checkpoint: %s", exc)

    def _save_checkpoint(self) -> None:
        if not self.checkpoint_path:
            return
        try:
            tmp_path = self.checkpoint_path.with_suffix(".tmp")
            data = {
                "fingerprint": self.run_fingerprint,
                "results": self.results,
                "completed": len(self._completed_ids),
                "total": len(self.cases),
                "complete": len(self._completed_ids) == len(self.cases),
            }
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            os.replace(tmp_path, self.checkpoint_path)
        except Exception as exc:
            logger.warning("Failed to save checkpoint: %s", exc)

    async def _run_single(self, case: EvalCase) -> Dict[str, Any]:
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
        return result

    async def run(self) -> List[Dict[str, Any]]:
        # if we already have results from checkpoint, merge
        remaining = []
        for case in self.cases:
            if case.id in self._completed_ids:
                continue
            remaining.append(case)

        if remaining:
            if self.concurrency <= 1:
                for case in remaining:
                    res = await self._run_single(case)
                    self.results.append(res)
                    self._completed_ids.add(res.get("case_id"))
                    self._save_checkpoint()
            else:
                semaphore = asyncio.Semaphore(self.concurrency)

                async def run_with_sem(c):
                    async with semaphore:
                        return await self._run_single(c)

                tasks = [asyncio.create_task(run_with_sem(c)) for c in remaining]
                for task in asyncio.as_completed(tasks):
                    res = await task
                    self.results.append(res)
                    self._completed_ids.add(res.get("case_id"))
                    self._save_checkpoint()

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
