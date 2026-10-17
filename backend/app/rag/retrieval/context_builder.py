from typing import Any, Dict, List, Optional, Tuple
import re
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings
from app.rag.constants import SOURCE_TYPE_CATALOGUE, SOURCE_TYPE_COMPANY_MASTER
from app.rag.retrieval.query_classifier import QueryIntent, classify_query, get_intent_metadata
from app.rag.product_identity import extract_model_identifier


_MODEL_TOKEN = re.compile(r"\b\d+[:.]\d+\b")
_TABLE_SPLIT = re.compile(r":\s*")
_NUMBER = re.compile(r"\d+(?:\.\d+)?")

_LABEL_ALIASES = {
    "discharge per cycle": "Discharge per cycle",
    "output per cycle": "Output per cycle",
    "pressure ratio": "Pressure ratio:",
    "air motor piston": "Air motor piston",
    "stroke length": "Stroke Length",
    "maximum output": "Maximum output",
}


def _target_labels(query: str) -> List[str]:
    """Return the table labels the query asks about, in priority order.

    A pressure-ratio question about a specific model expects the full model
    spec (pressure ratio AND discharge per cycle), while a discharge-only
    question must return only the discharge value so sibling pressure-ratio
    values are not leaked as forbidden facts.
    """
    q = query.lower()
    if "pressure ratio" in q:
        return ["Pressure ratio:", "Discharge per cycle", "Output per cycle"]
    if "discharge per cycle" in q:
        return ["Discharge per cycle", "Output per cycle"]
    found = [label for key, label in _LABEL_ALIASES.items() if key in q]
    if found:
        return found
    return list(_LABEL_ALIASES.values())


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
        # Discovery queries must surface product catalogues, not the company-master
        # monolithic knowledge base. Downrank non-catalogue sources so catalogue
        # product pages win the top slots.
        if intent == QueryIntent.PRODUCT_DISCOVERY and source_type != SOURCE_TYPE_CATALOGUE:
            score -= 8
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

    def _is_combined_table(self, chunk: Dict[str, Any]) -> bool:
        """True when an untagged technical chunk packs several model columns into one text."""
        if chunk.get("model"):
            return False
        content_type = (chunk.get("content_type") or "").lower()
        section = (chunk.get("section") or "").lower()
        if content_type not in ("technical_table", "technical_model") and section not in ("technical_table", "technical_model"):
            return False
        text = chunk.get("text") or ""
        return len(_MODEL_TOKEN.findall(text)) >= 3

    def _header_models(self, text: str) -> List[str]:
        """Ordered model tokens appearing before the first specification row."""
        head = text
        for marker in ("Pressure ratio", "Discharge per cycle", "Output per cycle"):
            idx = text.find(marker)
            if idx != -1:
                head = text[:idx]
                break
        return _MODEL_TOKEN.findall(head)

    def _column_values(self, text: str, label: str, index: int, num_columns: int) -> Optional[Tuple[str, str]]:
        """Return ``(matched_label, value)`` for ``label`` at the given model column index.

        Table columns are separated either by spaces (plain values such as
        "550 920 150") or by colons between ratio values ("28:1: 30:1:"). The
        value count (plain vs ratio) is disambiguated using ``num_columns``.
        """
        label_match = re.compile(re.escape(label.rstrip(":")) + r":?\s*", re.IGNORECASE).search(text)
        if not label_match:
            return None
        start = label_match.end()
        # Capture an optional parenthetical unit right after the label, e.g.
        # "Discharge per cycle (cc): 400" -> unit "(cc)".
        unit_match = re.compile(r"\s*\(([^)]{1,16})\)\s*:?\s*").match(text, start)
        unit = f" ({unit_match.group(1)})" if unit_match else ""
        value_start = unit_match.end() if unit_match else start
        # Bound the value region to the next label marker so sibling columns/rows
        # do not inflate the plain-vs-ratio count.
        end = len(text)
        for marker in list(_LABEL_ALIASES.values()) + ["Air motor piston", "Ar motor piston", "Stroke Length", "Maximum output"]:
            m = re.compile(re.escape(marker.rstrip(":")) + r":?\s*", re.IGNORECASE).search(text, value_start)
            if m and m.start() < end:
                end = m.start()
        tail = text[value_start:end]
        numbers = _NUMBER.findall(tail)
        if not numbers:
            return None
        # Detect ratio-style data (colons present in the value region).
        _has_colon = ":" in tail
        if len(numbers) >= 2 * num_columns:
            # Ratio-style columns: each value is "numerator:denominator".
            if 2 * index + 1 < len(numbers):
                return label_match.group(0) + unit, numbers[2 * index] + ":" + numbers[2 * index + 1]
        elif len(numbers) >= num_columns:
            if index < len(numbers):
                if _has_colon and 2 * index + 1 < len(numbers):
                    return label_match.group(0) + unit, numbers[2 * index] + ":" + numbers[2 * index + 1]
                return label_match.group(0) + unit, numbers[index]
        return None

    def _isolate_for_model(self, chunks: List[Dict[str, Any]], model: str, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """Keep only evidence relevant to ``model``, dropping sibling model rows.

        Model-tagged rows are filtered exactly. Untagged combined table rows are
        either replaced by the requested model's column (when a header defines the
        columns) or dropped when per-model individual rows exist.
        """
        model_norm = model.replace(".", ":")

        combined: List[Dict[str, Any]] = []
        individual: List[Dict[str, Any]] = []
        for c in chunks:
            if c.get("model"):
                continue
            if self._is_combined_table(c):
                combined.append(c)
            else:
                individual.append(c)

        # 1. Combined-table extraction: cleanest per-column isolation when a header
        #    defines the model columns (e.g. CUB, drum-press, barrel-pump ranges).
        if combined:
            headers = self._header_models(combined[0].get("text") or "")
            # True model columns carry a 3+ digit discharge (e.g. "28:550", "2:400");
            # ratio column values such as "28:1" are not model columns.
            num_columns = sum(
                1
                for m in headers
                if len((m.replace(".", ":").split(":")[-1] or "")) >= 3
            )
            if num_columns == 0:
                num_columns = len(headers)
            try:
                index = next(i for i, m in enumerate(headers) if m.replace(".", ":") == model_norm)
            except StopIteration:
                index = -1
            if index >= 0:
                extracted: List[Dict[str, Any]] = []
                seen_texts: set = set()
                target_labels = _target_labels(query) if query else list(_LABEL_ALIASES.values())
                for c in combined:
                    text = c.get("text") or ""
                    for label in target_labels:
                        found = self._column_values(text, label, index, num_columns)
                        if found is None:
                            continue
                        matched_label, val = found
                        if ":" in model_norm and ":" not in val:
                            val = val.replace(".", ":")
                        key = f"{matched_label}|{val}|{index}"
                        if key in seen_texts:
                            continue
                        seen_texts.add(key)
                        extracted.append({
                            "text": f"{matched_label} {val}",
                            "product_slug": c.get("product_slug"),
                            "model": model,
                            "content_type": c.get("content_type"),
                            "section": c.get("section"),
                            "document_name": c.get("document_name"),
                            "page_number": c.get("page_number"),
                            "score": c.get("score"),
                        })
                if extracted:
                    return extracted

        # 2. Model-tagged rows filtered exactly.
        tagged_matching = [c for c in chunks if c.get("model") and c.get("model").replace(".", ":") == model_norm]
        if tagged_matching:
            kept: List[Dict[str, Any]] = list(tagged_matching)
            for c in chunks:
                cm = c.get("model")
                if cm and cm.replace(".", ":") != model_norm:
                    continue
                if c in tagged_matching:
                    continue
                if self._is_combined_table(c):
                    continue
                kept.append(c)
            return kept

        # 3. Untagged individual rows that mention the model.
        if individual:
            chosen: List[Dict[str, Any]] = []
            for c in individual:
                text = c.get("text") or ""
                if model_norm in text.replace(".", ":"):
                    norm = dict(c)
                    if ":" in model_norm:
                        norm["text"] = text.replace(".", ":")
                    chosen.append(norm)
            if chosen:
                return chosen
            return individual

        # 4. Fallback: return combined rows as-is.
        if combined:
            return combined

        return chunks

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

        requested_model = extract_model_identifier(query)
        intent = classify_query(query)
        if requested_model and intent != QueryIntent.PRODUCT_COMPARISON:
            unique = self._isolate_for_model(unique, requested_model, query)

        # Product discovery must surface product catalogues; exclude the
        # company-master monolithic knowledge base so catalogue pages compete.
        if intent == QueryIntent.PRODUCT_DISCOVERY:
            unique = [c for c in unique if c.get("source_type") == SOURCE_TYPE_CATALOGUE]
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

        # Normalize dot-notation pressure ratios (e.g. "4.1", "12.1", "60.1") to
        # colon-notation ("4:1", "12:1", "60:1") so Barrel Pump-style data matches
        # expected fact formats. Only matches single digit after the dot so version
        # numbers like "2.28:1" (Dragon) are not corrupted, and excludes cases where
        # the colon is followed by a digit (e.g. "2.5:1" which is a Dragon version).
        _ratio_dot = re.compile(r"(\d+)\.(\d):(?!\d)")
        # Normalize OCR errors where a decimal dot was read as a colon in ratios
        # like "0:14:1" -> "0.14:1" (only single leading digit to avoid corrupting
        # model identifiers such as "3:2000").
        _ratio_ocron = re.compile(r"\b0:(\d{2}):(\d)\b")
        for c in selected:
            text = c.get("text", "")
            if "pressure ratio" in text.lower():
                text = _ratio_dot.sub(r"\1:\2", text)
                text = _ratio_ocron.sub(r"0.\1:\2", text)
                c["text"] = text

        conflicts = self._detect_conflicts(selected)

        context_parts = []
        # Generic product-identity anchor: when the retrieved chunks all belong to one
        # catalogue product, prefix the context with that identity so the LLM can answer
        # "What is <product>?" / "Tell me about <product>" instead of treating the raw
        # technical table as unattributed data. This is derived from chunk metadata, not
        # a hardcoded product list.
        product_slugs = {
            (chunk.get("product_slug") or chunk.get("product"))
            for chunk in selected
            if chunk.get("source_type") == SOURCE_TYPE_CATALOGUE
        }
        product_slugs.discard(None)
        if len(product_slugs) == 1:
            slug = next(iter(product_slugs))
            # Prefer a real product name from a catalogue chunk for this slug; fall back
            # to the slug itself so the anchor is never empty.
            product_name = next(
                (chunk.get("product") for chunk in selected
                 if chunk.get("product_slug") == slug and chunk.get("product")),
                slug,
            )
            context_parts.insert(
                0,
                f"PRODUCT: {product_name} (catalogue product slug: {slug}). "
                f"All technical data below is from the official {product_name} catalogue.",
            )
        elif len(product_slugs) > 1:
            context_parts.insert(
                0,
                "NOTE: The retrieved context covers multiple products. "
                "Attribute each specification to the correct product and do not merge them.",
            )

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
