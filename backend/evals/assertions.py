"""Phase 10 evaluation assertions."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from evals.case_schema import EvalCase


class AssertionFailure(Exception):
    def __init__(self, case_id: str, message: str) -> None:
        super().__init__(f"[{case_id}] {message}")
        self.case_id = case_id
        self.message = message


def _norm(text: str) -> str:
    return " ".join((text or "").lower().split())


def _chunk_text(chunk: Dict[str, Any]) -> str:
    return _norm(chunk.get("text", ""))


def _all_text(chunks: List[Dict[str, Any]]) -> str:
    return " ".join(_chunk_text(c) for c in chunks)


def _docs(chunks: List[Dict[str, Any]]) -> List[str]:
    return [c.get("document_name", "") for c in chunks]


def _slugs(chunks: List[Dict[str, Any]]) -> List[str]:
    return [c.get("product_slug", "") for c in chunks]


def assert_intent(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if case.expected_intent is None:
        return None
    actual = result.get("classified_intent")
    if actual != case.expected_intent:
        return f"intent expected={case.expected_intent} actual={actual}"
    return None


def assert_product(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if case.expected_product_slug is None:
        return None
    actual = result.get("active_context", {}).get("product_slug")
    if actual != case.expected_product_slug:
        return f"product expected={case.expected_product_slug} actual={actual}"
    return None


def assert_model(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if case.expected_model is None:
        return None
    actual = result.get("active_context", {}).get("model")
    if actual != case.expected_model:
        return f"model expected={case.expected_model} actual={actual}"
    return None


def assert_documents(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.expected_document_names:
        return None
    chunks = result.get("retrieved_chunks", []) or result.get("selected_chunks", []) or []
    docs = set(d for d in _docs(chunks) if d)
    for expected in case.expected_document_names:
        if expected not in docs:
            return f"document missing expected={expected} actual={sorted(d for d in docs if d)}"
    return None


def assert_required_facts(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.expected_required_facts:
        return None
    chunks = result.get("retrieved_chunks", []) or result.get("selected_chunks", []) or []
    text = _all_text(chunks)
    if isinstance(case.expected_required_facts, str):
        required = [case.expected_required_facts]
    else:
        required = list(case.expected_required_facts)
    missing = [f for f in required if _norm(f) not in text]
    if missing:
        return f"required facts missing: {missing}"
    return None


def assert_forbidden_facts(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.forbidden_facts:
        return None
    chunks = result.get("retrieved_chunks", []) or result.get("selected_chunks", []) or []
    text = _all_text(chunks)
    leaked = [f for f in case.forbidden_facts if _norm(f) in text]
    if leaked:
        return f"forbidden facts present: {leaked}"
    return None


def assert_catalogues(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.expected_catalogues:
        return None
    actual = sorted(c.get("document_name", "") for c in result.get("catalogues", []))
    expected = sorted(case.expected_catalogues)
    if actual != expected:
        return f"catalogues expected={expected} actual={actual}"
    return None


def assert_show_sources(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if case.expected_show_sources is None:
        return None
    actual = result.get("show_sources")
    if actual != case.expected_show_sources:
        return f"show_sources expected={case.expected_show_sources} actual={actual}"
    return None


def assert_unavailable(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.expected_unavailable:
        return None
    answer = result.get("answer", "")
    if "not available" not in _norm(answer):
        return f"expected unavailable answer, got: {answer[:120]!r}"
    return None


def assert_no_retrieval(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.expected_no_retrieval:
        return None
    chunks = result.get("retrieved_chunks", []) or []
    if chunks:
        return f"expected no retrieval but got {len(chunks)} chunks"
    return None


def assert_forbidden_documents(case: EvalCase, result: Dict[str, Any]) -> Optional[str]:
    if not case.forbidden_document_names:
        return None
    chunks = result.get("retrieved_chunks", []) or result.get("selected_chunks", []) or []
    docs = set(d for d in _docs(chunks) if d)
    leaked = [d for d in case.forbidden_document_names if d in docs]
    if leaked:
        return f"forbidden documents present: {leaked}"
    return None


def evaluate_case(case: EvalCase, result: Dict[str, Any]) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    for fn in (
        assert_intent, assert_product, assert_model, assert_documents,
        assert_required_facts, assert_forbidden_facts,
        assert_catalogues, assert_show_sources, assert_unavailable,
        assert_no_retrieval, assert_forbidden_documents,
    ):
        msg = fn(case, result)
        if msg:
            failures.append(msg)
    return (len(failures) == 0), failures
