from typing import Any, Dict, List, Optional
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings


class ContextBuilder:
    def __init__(self, reranker: Optional[Reranker] = None) -> None:
        self.reranker = reranker

    def build(self, chunks: List[Dict[str, Any]], query: str, max_chars: int = 12000) -> Dict[str, Any]:
        ordered = sorted(chunks, key=lambda item: item.get("authority_priority", 0), reverse=True)
        seen = set()
        unique: List[Dict[str, Any]] = []
        for chunk in ordered:
            text = chunk.get("text", "")
            if not text:
                continue
            key = text.strip()
            if key in seen:
                continue
            seen.add(key)
            unique.append(chunk)

        if self.reranker and rag_settings.RAG_RERANK_ENABLED:
            unique = self.reranker.rerank(query, unique)

        selected: List[Dict[str, Any]] = []
        total_chars = 0
        for chunk in unique:
            length = len(chunk.get("text", ""))
            if total_chars + length > max_chars:
                break
            selected.append(chunk)
            total_chars += length

        context_parts = []
        sources = []
        for chunk in selected:
            context_parts.append(chunk.get("text", ""))
            source = {
                "source_type": chunk.get("source_type"),
                "document": chunk.get("document_name"),
                "product": chunk.get("product"),
                "section": chunk.get("section"),
                "page": chunk.get("page_number"),
                "model": chunk.get("model"),
                "line_start": chunk.get("line_start"),
                "line_end": chunk.get("line_end"),
                "verification_status": chunk.get("verification_status") or chunk.get("data_status"),
            }
            if chunk.get("source_type") == "catalogue":
                source["url"] = f"/media/catalogues/{chunk.get('document_name', '')}"
            sources.append(source)

        return {"context": "\n\n".join(context_parts), "sources": sources, "chunks": selected}
