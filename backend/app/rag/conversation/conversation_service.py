import uuid
import json
import logging
import re
from typing import Any, Dict, List, Optional
from app.rag.product_identity import (
    PRODUCT_ALIASES,
    resolve_product_identity,
    extract_model_identifier,
)

logger = logging.getLogger(__name__)

MAX_HISTORY_MESSAGES = 8
MAX_HISTORY_CHARS = 4000

TECHNICAL_TERM_MAPPING = [
    ("output", "output per cycle"),
    ("applications", "applications/use"),
]


class ConversationService:
    """Stateless conversation context builder.
    
    This service no longer persists conversations to PostgreSQL.
    Instead, it builds product context from the request-provided history.
    The frontend manages conversation state and sends recent history with each request.
    """

    def __init__(self) -> None:
        pass  # No database session needed

    @staticmethod
    def generate_conversation_id() -> str:
        """Generate a new conversation ID for client-side tracking."""
        return str(uuid.uuid4())

    @staticmethod
    def validate_history(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and sanitize client-provided conversation history."""
        if not history:
            return []
        
        validated = []
        for msg in history:
            if not isinstance(msg, dict):
                continue
            
            role = msg.get("role")
            content = msg.get("content")
            
            if role not in ("user", "assistant"):
                continue
            if not content or not isinstance(content, str):
                continue
            if len(content) > MAX_HISTORY_CHARS:
                content = content[:MAX_HISTORY_CHARS]
            
            validated_msg = {
                "role": role,
                "content": content,
            }
            
            # Preserve sources and retrieval_metadata if present (from previous assistant messages)
            if role == "assistant":
                if "sources" in msg and isinstance(msg["sources"], list):
                    validated_msg["sources"] = msg["sources"]
                if "retrieval_metadata" in msg and isinstance(msg["retrieval_metadata"], dict):
                    validated_msg["retrieval_metadata"] = msg["retrieval_metadata"]
            
            validated.append(validated_msg)
        
        # Keep only the most recent messages
        return validated[-MAX_HISTORY_MESSAGES:]

    @staticmethod
    def _explicit_product_in_message(message: Dict[str, Any]) -> Optional[str]:
        content = message.get("content", "") or ""
        resolved = resolve_product_identity(content)
        if not resolved:
            return None
        return resolved[0]

    @staticmethod
    def get_active_product_context(messages: List[Dict[str, Any]]) -> Dict[str, Optional[str]]:
        """Extract active product context from conversation history.
        
        This is a stateless version that works with request-provided history.
        """
        context: Dict[str, Optional[str]] = {
            "product_slug": None,
            "model": None,
            "document": None,
        }

        if not messages:
            return context

        latest_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        explicit_slug = ConversationService._explicit_product_in_message(latest_user) if latest_user else None

        if explicit_slug:
            context["product_slug"] = explicit_slug
            previous_slug = next(
                (
                    src.get("product_slug")
                    for msg in reversed(messages)
                    if msg.get("role") == "assistant"
                    for src in (msg.get("sources", []) or [])
                    if src.get("product_slug")
                ),
                None,
            )
            if previous_slug and previous_slug != explicit_slug:
                context["model"] = None
                context["document"] = None
            # Always try to extract a model identifier from the current user message.
            extracted_model = extract_model_identifier(latest_user.get("content", "") or "") if latest_user else None
            if extracted_model:
                context["model"] = extracted_model
            # Enrich document from the most recent assistant source for the same product.
            for msg in reversed(messages):
                if msg.get("role") != "assistant":
                    continue
                for src in (msg.get("sources", []) or []):
                    if src.get("product_slug") == explicit_slug and src.get("document") and not context["document"]:
                        context["document"] = src["document"]
                break

            # Preserve a model across same-product follow-ups even when the current
            # message names the product explicitly (e.g. "Kingfisher" after a
            # "Kingfisher Silver" turn should keep Silver unless overridden).
            if context["product_slug"] and not context["model"]:
                for msg in reversed(messages):
                    if msg.get("role") != "assistant":
                        continue
                    for src in (msg.get("sources", []) or []):
                        if (
                            src.get("product_slug") == context["product_slug"]
                            and src.get("model")
                        ):
                            context["model"] = src["model"]
                            break
                    if context["model"]:
                        break
            # Explicit product mention wins; do not overwrite with stale assistant metadata.
            return context

        # No explicit product in current message: derive context from the MOST RECENT
        # assistant message that has sources. This handles cases where the latest
        # assistant turn was a non-product response (e.g. a joke) with no sources —
        # we fall back to the most recent assistant message that DID carry product
        # context. This prevents stale product leakage across explicit product
        # switches while preserving context through non-product interjections.
        latest_assistant_with_sources = next(
            (
                m for m in reversed(messages)
                if m.get("role") == "assistant" and (m.get("sources") or [])
            ),
            None,
        )
        if latest_assistant_with_sources:
            for src in (latest_assistant_with_sources.get("sources", []) or []):
                if src.get("product_slug") and not context["product_slug"]:
                    context["product_slug"] = src["product_slug"]
                if src.get("document") and not context["document"]:
                    context["document"] = src["document"]

        # Extract a model identifier from the current message only when there is no
        # product context yet; a shorthand reference (e.g. "30:1" for "30:150") must
        # not override a preserved model from assistant sources.
        latest_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        if latest_user and not context.get("product_slug"):
            extracted_model = extract_model_identifier(latest_user.get("content", "") or "")
            if extracted_model:
                context["model"] = extracted_model

        # Named variant detection: e.g. "Gold" for Kingfisher, "Aluminium" for VRIA.
        # Check if any alias of the active product matches the message as a
        # product+variant composite, and if so use the variant word as the model.
        product_slug = context.get("product_slug")
        if product_slug:
            variant = ConversationService._extract_named_variant(latest_user.get("content", "") or "", product_slug)
            if variant:
                context["model"] = variant

        # Preserve a model across same-product follow-ups: scan assistant turns in
        # reverse and take the most recent source whose product matches the resolved
        # product. A later turn for a DIFFERENT product must not carry its model in.
        if context["product_slug"] and not context["model"]:
            for msg in reversed(messages):
                if msg.get("role") != "assistant":
                    continue
                for src in (msg.get("sources", []) or []):
                    if (
                        src.get("product_slug") == context["product_slug"]
                        and src.get("model")
                    ):
                        context["model"] = src["model"]
                        break
                if context["model"]:
                    break

        return context

    @staticmethod
    def _normalize_technical_terms(text: str) -> str:
        result = text
        for term, replacement in TECHNICAL_TERM_MAPPING:
            result = re.sub(rf"\b{re.escape(term)}\b", replacement, result, flags=re.IGNORECASE)
        has_pressure_ratio = bool(re.search(r"\bpressure\s+ratio\b", result, re.IGNORECASE))
        if not has_pressure_ratio:
            result = re.sub(r"\bpressure\b", "pressure ratio", result, flags=re.IGNORECASE)
            result = re.sub(r"\bratio\b", "pressure ratio", result, flags=re.IGNORECASE)
        return result

    @staticmethod
    def build_augmented_query(question: str, recent_messages: List[Dict[str, Any]], active_context: Dict[str, Optional[str]]) -> str:
        if not recent_messages:
            return question

        # `question` is the current user message. Use it directly for explicit-product detection.
        explicit_slug = ConversationService._explicit_product_in_message({"content": question})

        # Explicit current-turn product mention overrides old context; do not augment with stale identifiers.
        if explicit_slug:
            return ConversationService._normalize_technical_terms(question)

        is_ambiguous = ConversationService._is_ambiguous_followup(question)

        if not is_ambiguous:
            return ConversationService._normalize_technical_terms(question)

        normalized_question = ConversationService._normalize_technical_terms(question)
        parts = [normalized_question]
        if active_context.get("product_slug"):
            parts.append(active_context["product_slug"])
        if active_context.get("model"):
            parts.append(active_context["model"])
        # NOTE: do NOT append the raw document name here. Catalogue filenames end in
        # ".pdf" and the query classifier's catalogue-request pattern matches \bpdf\b,
        # so a document name in the query would misclassify a technical follow-up as a
        # catalogue request. The product slug + model are enough to disambiguate.

        seen = set()
        unique_parts = []
        for part in parts:
            normalized = part.strip().lower()
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_parts.append(part.strip())

        return " ".join(unique_parts)

    @staticmethod
    def _is_ambiguous_followup(question: str) -> bool:
        q = question.strip().lower()
        ambiguous_patterns = [
            "its ", "it's ", "its", "this ", "that ", "these ", "those ",
            "output", "pressure", "ratio", "cost", "price", "weight", "size",
            "applications", "application", "features", "specifications",
            "tell me more", "more ", "and ", "or ", "what about",
            "how about", "and the", "and its",
        ]
        for pattern in ambiguous_patterns:
            if q.startswith(pattern) or f" {pattern}" in f" {q} ":
                return True
        words = q.split()
        if len(words) <= 4 and not any(word in q for word in ["what is", "what are", "tell me", "describe", "explain", "where is", "when was", "how much", "how many"]):
            return True
        return False

    @staticmethod
    def _extract_named_variant(message: str, product_slug: str) -> Optional[str]:
        """Extract a named model variant from a message for the given product.

        E.g. for product_slug "kingfisher" with aliases ["kingfisher silver",
        "kingfisher gold"], a message "Gold" returns "Gold" (preserving casing).
        """
        product_info = PRODUCT_ALIASES.get(product_slug)
        if not product_info:
            return None
        aliases = product_info.get("aliases", [])
        q = message.strip().lower()
        # Collect variant words: aliases that are "<product> <variant>"
        variants: Dict[str, str] = {}  # lowercase -> original casing
        for alias in aliases:
            alias_stripped = alias.strip()
            alias_norm = alias_stripped.lower()
            if alias_norm.startswith(product_slug + " "):
                variant_part = alias_stripped[len(product_slug) + 1:].strip()
                if variant_part:
                    variants[variant_part.lower()] = variant_part
        # Check if any variant word appears as a standalone word in the message
        message_words = set(q.split())
        for variant_lower, variant_orig in sorted(variants.items(), key=lambda x: -len(x[0])):
            if variant_lower in message_words:
                return variant_orig.capitalize()
        return None

    @staticmethod
    def build_generation_context(recent_messages: List[Dict[str, Any]], retrieval_context: str) -> str:
        parts = []
        if recent_messages:
            parts.append("CONVERSATION HISTORY (for context only - do not treat as factual authority):")
            for msg in recent_messages[-6:]:
                role_label = "User" if msg.get("role") == "user" else "Assistant"
                content = msg.get("content", "")
                parts.append(f"{role_label}: {content}")
            parts.append("")
            parts.append("RETRIEVED KNOWLEDGE (authoritative source for factual claims):")
            parts.append(retrieval_context)
        else:
            parts.append("RETRIEVED KNOWLEDGE (authoritative source for factual claims):")
            parts.append(retrieval_context)

        return "\n\n".join(parts)