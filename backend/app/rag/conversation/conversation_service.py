import uuid
import json
import logging
import re
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, delete
from app.models.rag_conversation import RagConversation, RagMessage
from app.rag.product_identity import resolve_product_identity, extract_model_identifier

logger = logging.getLogger(__name__)

MAX_HISTORY_MESSAGES = 8
MAX_HISTORY_CHARS = 4000

TECHNICAL_TERM_MAPPING = [
    ("output", "output per cycle"),
    ("applications", "applications/use"),
]


class ConversationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_or_create_conversation(self, conversation_id: Optional[str]) -> RagConversation:
        if conversation_id:
            try:
                cid = uuid.UUID(conversation_id)
            except (ValueError, TypeError):
                raise ValueError("Invalid conversation_id format")

            result = await self.db.execute(
                select(RagConversation).where(RagConversation.id == cid, RagConversation.status == "active")
            )
            conversation = result.scalar_one_or_none()
            if not conversation:
                raise ValueError("Conversation not found")
            return conversation

        conversation = RagConversation(status="active")
        self.db.add(conversation)
        await self.db.flush()
        await self.db.refresh(conversation)
        return conversation

    async def append_user_message(self, conversation_id: uuid.UUID, content: str) -> RagMessage:
        message = RagMessage(
            conversation_id=conversation_id,
            role="user",
            content=content,
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def append_assistant_message(
        self,
        conversation_id: uuid.UUID,
        content: str,
        sources: Optional[List[Dict[str, Any]]] = None,
        retrieval_metadata: Optional[Dict[str, Any]] = None,
    ) -> RagMessage:
        message = RagMessage(
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            sources=json.dumps(sources or []),
            retrieval_metadata=json.dumps(retrieval_metadata or {}),
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def get_recent_messages(self, conversation_id: uuid.UUID, limit: int = MAX_HISTORY_MESSAGES) -> List[Dict[str, Any]]:
        result = await self.db.execute(
            select(RagMessage)
            .where(RagMessage.conversation_id == conversation_id)
            .order_by(desc(RagMessage.created_at))
            .limit(limit)
        )
        rows = result.scalars().all()
        rows.reverse()

        messages: List[Dict[str, Any]] = []
        for row in rows:
            messages.append({
                "role": row.role,
                "content": row.content,
                "sources": json.loads(row.sources) if row.sources else [],
                "retrieval_metadata": json.loads(row.retrieval_metadata) if row.retrieval_metadata else {},
            })
        return messages

    def _explicit_product_in_message(self, message: Dict[str, Any]) -> Optional[str]:
        content = message.get("content", "") or ""
        resolved = resolve_product_identity(content)
        if not resolved:
            return None
        return resolved[0]

    def get_active_product_context(self, messages: List[Dict[str, Any]]) -> Dict[str, Optional[str]]:
        context: Dict[str, Optional[str]] = {
            "product_slug": None,
            "model": None,
            "document": None,
        }

        if not messages:
            return context

        latest_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        explicit_slug = self._explicit_product_in_message(latest_user) if latest_user else None

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
            # Explicit product mention wins; do not overwrite with stale assistant metadata.
            return context

        # No explicit product in current message: derive from the most recent assistant message only.
        for msg in reversed(messages):
            if msg.get("role") != "assistant":
                continue
            sources = msg.get("sources", []) or []
            if not sources:
                continue
            primary = sources[0]
            if primary.get("product_slug"):
                context["product_slug"] = primary["product_slug"]
            if primary.get("model"):
                context["model"] = primary["model"]
            if primary.get("document"):
                context["document"] = primary["document"]
            return context

        return context

    def _normalize_technical_terms(self, text: str) -> str:
        result = text
        for term, replacement in TECHNICAL_TERM_MAPPING:
            result = re.sub(rf"\b{re.escape(term)}\b", replacement, result, flags=re.IGNORECASE)
        has_pressure_ratio = bool(re.search(r"\bpressure\s+ratio\b", result, re.IGNORECASE))
        if not has_pressure_ratio:
            result = re.sub(r"\bpressure\b", "pressure ratio", result, flags=re.IGNORECASE)
            result = re.sub(r"\bratio\b", "pressure ratio", result, flags=re.IGNORECASE)
        return result

    def build_augmented_query(self, question: str, recent_messages: List[Dict[str, Any]], active_context: Dict[str, Optional[str]]) -> str:
        if not recent_messages:
            return question

        # `question` is the current user message. Use it directly for explicit-product detection.
        explicit_slug = self._explicit_product_in_message({"content": question})

        # Explicit current-turn product mention overrides old context; do not augment with stale identifiers.
        if explicit_slug:
            return self._normalize_technical_terms(question)

        is_ambiguous = self._is_ambiguous_followup(question)

        if not is_ambiguous:
            return self._normalize_technical_terms(question)

        normalized_question = self._normalize_technical_terms(question)
        parts = [normalized_question]
        if active_context.get("product_slug"):
            parts.append(active_context["product_slug"])
        if active_context.get("model"):
            parts.append(active_context["model"])
        if active_context.get("document"):
            parts.append(active_context["document"])

        seen = set()
        unique_parts = []
        for part in parts:
            normalized = part.strip().lower()
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_parts.append(part.strip())

        return " ".join(unique_parts)

    def _is_ambiguous_followup(self, question: str) -> bool:
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

    def build_generation_context(self, recent_messages: List[Dict[str, Any]], retrieval_context: str) -> str:
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
