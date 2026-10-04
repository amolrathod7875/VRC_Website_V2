import re
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from app.rag.product_identity import resolve_product_identity


class QueryIntent(str, Enum):
    GENERAL_COMPANY = "general_company"
    PRODUCT_TECHNICAL = "product_technical"
    PRODUCT_APPLICATION = "product_application"
    CONTACT_LOCATION = "contact_location"
    GOVERNANCE = "governance"
    MODEL_IDENTIFIER = "model_identifier"
    PRODUCT_COMPARISON = "product_comparison"
    GREETING = "greeting"
    ASSISTANT_IDENTITY = "assistant_identity"
    GENERAL_CHAT = "general_chat"
    UNKNOWN = "unknown"


NEGATIVE_EXISTENTIAL_PATTERNS = [
    re.compile(r"\bdoes\s+vr\s+coatings\s+(make|manufacture|sell|offer|provide|have|support|include)\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+the\s+company\s+(make|manufacture|sell|offer|provide|have|support|include)\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+tiger\s+(support|have|include|offer|provide)\s+(.+)", re.IGNORECASE),
    re.compile(r"\bis\s+tiger\s+compatible\s+with\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+product\s+(support|have|include|offer|provide)\s+(.+)", re.IGNORECASE),
    re.compile(r"\bis\s+vr\s+coatings\s+located\s+in\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+operate\s+in\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+have\s+certification\s+(.+)", re.IGNORECASE),
    re.compile(r"\bis\s+product\s+available\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+product\s+have\s+feature\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+make\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+manufacture\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+sell\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+have\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+support\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+include\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+offer\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+vr\s+coatings\s+provide\s+(.+)", re.IGNORECASE),
    re.compile(r"\bis\s+vr\s+coatings\s+in\s+(.+)", re.IGNORECASE),
    re.compile(r"\bis\s+vr\s+coatings\s+at\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+the\s+company\s+have\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+the\s+company\s+support\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+the\s+company\s+include\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+the\s+company\s+offer\s+(.+)", re.IGNORECASE),
    re.compile(r"\bdoes\s+the\s+company\s+provide\s+(.+)", re.IGNORECASE),
]

COMPARISON_PATTERNS = [
    re.compile(r"\bcompare\b", re.IGNORECASE),
    re.compile(r"\bvs\b", re.IGNORECASE),
    re.compile(r"\bversus\b", re.IGNORECASE),
    re.compile(r"\bdifference\s+between\b", re.IGNORECASE),
]

AFFIRMATIVE_YES_NO_PATTERNS = [
    re.compile(r"\bdoes\s+tiger\s+\d+:\d+\s+have\s+a\s+pressure\s+ratio\s+of\s+\d+:\d+\b", re.IGNORECASE),
    re.compile(r"\bis\s+the\s+pressure\s+ratio\s+of\s+tiger\s+\d+:\d+\s+\d+:\d+\b", re.IGNORECASE),
    re.compile(r"\bdoes\s+tiger\s+\d+:\d+\s+have\s+an?\s+.+?\s+of\s+.+\b", re.IGNORECASE),
    re.compile(r"\bis\s+vr\s+coatings\s+located\s+in\b", re.IGNORECASE),
    re.compile(r"\bis\s+vr\s+coatings\s+founded\s+in\b", re.IGNORECASE),
    re.compile(r"\bis\s+vr\s+coatings\s+based\s+in\b", re.IGNORECASE),
]

MODEL_IDENTIFIER_PATTERN = re.compile(r"^([A-Za-z]+)?\s*\d+:\d+$", re.IGNORECASE)


def classify_query(question: str) -> QueryIntent:
    normalized = question.strip().lower()

    if MODEL_IDENTIFIER_PATTERN.match(normalized):
        return QueryIntent.MODEL_IDENTIFIER

    for pattern in COMPARISON_PATTERNS:
        if pattern.search(normalized):
            return QueryIntent.PRODUCT_COMPARISON

    governance_keywords = ["unknown", "tbc", "proposed", "inferred", "conflict", "data status", "governance"]
    if any(kw in normalized for kw in governance_keywords):
        return QueryIntent.GOVERNANCE

    contact_keywords = ["contact", "phone", "number", "email", "address", "office", "location", "head office", "south india", "north india"]
    if any(kw in normalized for kw in contact_keywords):
        return QueryIntent.CONTACT_LOCATION

    product_technical_keywords = ["pressure ratio", "output per cycle", "flow rate", "viscosity", "max pressure", "technical specification", "cc ", "bar ", "psi"]
    if any(kw in normalized for kw in product_technical_keywords):
        return QueryIntent.PRODUCT_TECHNICAL

    yes_no_technical_keywords = ["have a pressure ratio", "have an output", "have a flow", "have a viscosity", "have a max"]
    if any(kw in normalized for kw in yes_no_technical_keywords):
        return QueryIntent.PRODUCT_TECHNICAL

    general_company_keywords = ["vr coatings", "company", "manufacture", "manufacturing", "products", "about", "tell me about", "what is", "what does"]
    if any(kw in normalized for kw in general_company_keywords):
        return QueryIntent.GENERAL_COMPANY

    product_application_keywords = ["used for", "application", "compatible with", "suitable for", "coating", "painting", "spray"]
    if any(kw in normalized for kw in product_application_keywords):
        return QueryIntent.PRODUCT_APPLICATION

    return QueryIntent.UNKNOWN


def is_negative_existential(question: str) -> bool:
    normalized = question.strip().lower()
    for pattern in NEGATIVE_EXISTENTIAL_PATTERNS:
        if pattern.search(normalized):
            return True
    return False


def is_affirmative_yes_no(question: str) -> bool:
    normalized = question.strip().lower()
    for pattern in AFFIRMATIVE_YES_NO_PATTERNS:
        if pattern.search(normalized):
            return True
    return False


def evaluate_evidence_guard(question: str, context: str) -> Tuple[bool, str]:
    if not context or not context.strip():
        return True, "This information is not available in the current VR Coatings knowledge base."

    normalized_context = " ".join(context.strip().lower().split())
    normalized_question = " ".join(question.strip().lower().split())

    if is_affirmative_yes_no(question):
        return False, ""

    if is_negative_existential(question):
        negative_subject = _extract_negative_subject(question)
        if negative_subject and negative_subject.lower() in normalized_context:
            return False, ""
        return True, "This information is not available in the current VR Coatings knowledge base."

    return False, ""


def _extract_negative_subject(question: str) -> str:
    for pattern in NEGATIVE_EXISTENTIAL_PATTERNS:
        match = pattern.search(question.strip())
        if match:
            groups = match.groups()
            if len(groups) >= 2:
                subject = groups[-1].strip()
                return subject.strip("?!.,;:")
    return ""


def get_intent_metadata(intent: QueryIntent) -> dict:
    if intent == QueryIntent.GENERAL_COMPANY:
        return {
            "prefer_sections": ["company overview", "about", "company profile", "canonical profile", "manufacturing", "business overview", "product portfolio"],
            "downrank_sections": ["change log", "governance", "unknown_register", "internal notes", "dataset goals", "document maintenance"],
            "prefer_source_types": ["company_master"],
        }
    if intent == QueryIntent.PRODUCT_COMPARISON:
        return {
            "prefer_sections": ["technical_model", "description", "features", "applications", "technical specifications"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue", "company_master"],
        }
    if intent == QueryIntent.PRODUCT_TECHNICAL:
        return {
            "prefer_sections": ["technical specifications", "technical_model", "specifications"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue"],
        }
    if intent == QueryIntent.PRODUCT_APPLICATION:
        return {
            "prefer_sections": ["applications", "technical specifications", "technical_model"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue", "company_master"],
        }
    if intent == QueryIntent.CONTACT_LOCATION:
        return {
            "prefer_sections": ["contact", "locations", "regional contacts", "head office"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["company_master"],
        }
    if intent == QueryIntent.GOVERNANCE:
        return {
            "prefer_sections": ["unknown", "tbc", "governance", "data status", "register"],
            "downrank_sections": ["technical specifications", "company overview"],
            "prefer_source_types": ["company_master"],
        }
    if intent == QueryIntent.MODEL_IDENTIFIER:
        return {
            "prefer_sections": ["technical specifications", "technical_model"],
            "downrank_sections": ["change log", "governance", "unknown_register"],
            "prefer_source_types": ["catalogue", "company_master"],
        }
    return {
        "prefer_sections": [],
        "downrank_sections": [],
        "prefer_source_types": [],
    }


def is_vr_coatings_domain_query(
    question: str,
    active_context: Optional[Dict[str, Optional[str]]] = None,
    recent_messages: Optional[List[Dict[str, Any]]] = None,
) -> bool:
    if not question or not question.strip():
        return False

    normalized = question.strip().lower()

    # 1. Explicit known product/model/company reference in the current message.
    if resolve_product_identity(question):
        return True

    company_keywords = ["vr coatings", "vrc ", " vrc", "company", "catalogue"]
    if any(kw in normalized for kw in company_keywords):
        return True

    # Product/technical/application keywords strongly imply a domain query.
    domain_keywords = [
        "pressure ratio", "output per cycle", "flow rate", "viscosity", "max pressure",
        "technical specification", "cc ", "bar ", "psi",
        "used for", "application", "compatible with", "suitable for", "coating", "painting",
        "warranty", "price", "cost", "weight", "size", "material",
    ]
    if any(kw in normalized for kw in domain_keywords):
        return True

    # 2. Confident contextual product follow-up.
    if active_context and active_context.get("product_slug"):
        if _is_domain_followup(question):
            return True

    return False


def _is_domain_followup(question: str) -> bool:
    q = question.strip().lower()

    general_knowledge_indicators = [
        "artificial intelligence", "machine learning", "python", "java", "javascript",
        "sql", "tcp", "udp", "joke", "factorial", "capital of", "president",
        "planet", "country", "explain newton", "write a ", "code to", "function to",
        "what is a ", "how does a ", "difference between ", " ai", "deep learning",
        "neural network", "transformer model", "algorithm", "data structure",
    ]
    for indicator in general_knowledge_indicators:
        if indicator in q:
            return False

    domain_indicators = [
        "its ", "it's ", "its", "this ", "that ", "these ", "those ",
        "output", "pressure", "ratio", "cost", "price", "weight", "size",
        "applications", "application", "features", "specifications",
        "tell me more", "more ", "and ", "or ", "what about",
        "how about", "and the", "and its", "warranty", "material",
    ]
    for pattern in domain_indicators:
        if q.startswith(pattern) or f" {pattern}" in f" {q} ":
            return True

    words = q.split()
    if len(words) <= 4:
        return True

    return False
