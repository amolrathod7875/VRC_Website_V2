from typing import Any, Dict, List, Optional
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings
from app.rag.constants import SOURCE_TYPE_CATALOGUE, SOURCE_TYPE_COMPANY_MASTER
from app.rag.retrieval.query_classifier import QueryIntent, classify_query, get_intent_metadata


class ContextBuilder:
    def __init__(self, reranker: Optional[Reranker] = None) -> None:
        self.reranker = reranker

    def _normalize_text(self, text: str) -> str:
        return " ".join(text.strip().lower().split())

    def _score_for_intent(self, chunk: Dict[str, Any], intent: QueryIntent) -> int:
        section = (chunk.get("section") or "").lower()
        source_type = (chunk.get("source_type") or "").lower()
        metadata = get_intent_metadata(intent)

        score = 0
        for preferred in metadata.get("prefer_sections", []):
            if preferred in section:
                score += 3
                break
        for downrank in metadata.get("downrank_sections", []):
            if downrank in section:
                score -= 5
                break
        for preferred_type in metadata.get("prefer_source_types", []):
            if preferred_type == source_type:
                score += 2
                break
        return score

    def _detect_conflicts(self, chunks: List[Dict[str, Any]]) -> List[str]:
        conflicts: List[str] = []
        by_model: Dict[str, List[Dict[str, Any]]] = {}
        for chunk in chunks:
            model = chunk.get("model")
            product_slug = chunk.get("product_slug")
            if not model or not product_slug:
                continue
            key = f"{product_slug}:{model}"
            by_model.setdefault(key, []).append(chunk)

        for key, group in by_model.items():
            if len(group) < 2:
                continue
            source_types = {c.get("source_type") for c in group}
            if SOURCE_TYPE_CATALOGUE in source_types and SOURCE_TYPE_COMPANY_MASTER in source_types:
                conflicts.append(
                    f"Conflicting information detected for {key}. Official catalogue takes precedence for product specifications."
                )
        return conflicts

    def build(
        self,
        chunks: List[Dict[str, Any]],
        query: str,
        max_chunks: int = 8,
        max_chars: int = 12000,
    ) -> Dict[str, Any]:
        ordered = list(chunks)
        seen = set()
        unique: List[Dict[str, Any]] = []
        for chunk in ordered:
            text = chunk.get("text", "")
            if not text:
                continue
            key = self._normalize_text(text)
            if key in seen:
                continue
            seen.add(key)
            unique.append(chunk)

        intent = classify_query(query)
        unique.sort(key=lambda c: self._score_for_intent(c, intent), reverse=True)

        if self.reranker and rag_settings.RAG_RERANK_ENABLED:
            unique = self.reranker.rerank(query, unique)

        selected: List[Dict[str, Any]] = []
        total_chars = 0
        for chunk in unique:
            if len(selected) >= max_chunks:
                break
            length = len(chunk.get("text", ""))
            if total_chars + length > max_chars:
                break
            selected.append(chunk)
            total_chars += length

        conflicts = self._detect_conflicts(selected)

        context_parts = []
        sources = []
        for chunk in selected:
            context_parts.append(chunk.get("text", ""))
            source = {
                "source_type": chunk.get("source_type"),
                "document": chunk.get("document_name"),
                "product": chunk.get("product"),
                "product_slug": chunk.get("product_slug"),
                "section": chunk.get("section"),
                "page": chunk.get("page_number"),
                "model": chunk.get("model"),
                "line_start": chunk.get("line_start"),
                "line_end": chunk.get("line_end"),
                "verification_status": chunk.get("verification_status") or chunk.get("data_status"),
                "authority_priority": chunk.get("authority_priority"),
            }
            if chunk.get("source_type") == SOURCE_TYPE_CATALOGUE:
                source["url"] = f"/media/catalogues/{chunk.get('document_name', '')}"
            sources.append(source)

        if conflicts:
            context_parts.insert(0, "NOTE: " + "; ".join(conflicts))

        return {
            "context": "\n\n".join(context_parts),
            "sources": sources,
            "chunks": selected,
        }
