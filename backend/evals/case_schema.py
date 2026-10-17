"""Phase 10 evaluation case schema."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


CATEGORIES = [
    "identity", "technical", "table", "multi-product", "system",
    "applications", "discovery", "comparison", "catalogue", "unavailable",
    "context", "general-chat", "source-isolation",
]


@dataclass
class EvalCase:
    id: str
    category: str
    question: str
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    expected_intent: Optional[str] = None
    expected_product_slug: Optional[str] = None
    expected_model: Optional[str] = None
    expected_document_names: List[str] = field(default_factory=list)
    expected_required_facts: List[str] = field(default_factory=list)
    forbidden_facts: List[str] = field(default_factory=list)
    expected_catalogues: List[str] = field(default_factory=list)
    expected_show_sources: Optional[bool] = None
    expected_unavailable: bool = False
    notes: str = ""
    severity: str = "MEDIUM"
    expected_no_retrieval: bool = False
    forbidden_document_names: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "category": self.category, "question": self.question,
            "conversation_history": self.conversation_history,
            "expected_intent": self.expected_intent,
            "expected_product_slug": self.expected_product_slug,
            "expected_model": self.expected_model,
            "expected_document_names": self.expected_document_names,
            "expected_required_facts": self.expected_required_facts,
            "forbidden_facts": self.forbidden_facts,
            "expected_catalogues": self.expected_catalogues,
            "expected_show_sources": self.expected_show_sources,
            "expected_unavailable": self.expected_unavailable,
            "notes": self.notes, "severity": self.severity,
            "expected_no_retrieval": self.expected_no_retrieval,
            "forbidden_document_names": self.forbidden_document_names,
        }


def case(id: str, category: str, question: str, **kwargs: Any) -> EvalCase:
    return EvalCase(id=id, category=category, question=question, **kwargs)