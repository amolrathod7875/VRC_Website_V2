import uuid
import json
import logging
import re
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, delete
from app.models.rag_conversation import RagConversation, RagMessage

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

    def get_active_product_context(self, messages: List[Dict[str, Any]]) -> Dict[str, Optional[str]]:
        context: Dict[str, Optional[str]] = {
            "product_slug": None,
            "model": None,
            "document": None,
        }

        for msg in reversed(messages):
            if msg.get("role") != "assistant":
                continue
            for src in msg.get("sources", []) or []:
                if src.get("product_slug") and not context["product_slug"]:
                    context["product_slug"] = src["product_slug"]
                if src.get("model") and not context["model"]:
                    context["model"] = src["model"]
                if src.get("document") and not context["document"]:
                    context["document"] = src["document"]
                if context["product_slug"] and context["model"]:
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

        last_user_msg = next((m for m in reversed(recent_messages) if m.get("role") == "user"), None)
        is_ambiguous = not last_user_msg or self._is_ambiguous_followup(question)

        if not is_ambiguous:
            return question

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
            "tell me more", "more ", "about ", "and ", "or ", "what about",
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
