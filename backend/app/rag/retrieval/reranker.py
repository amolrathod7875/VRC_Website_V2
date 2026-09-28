from typing import Any, Dict, List


class Reranker:
    def rerank(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return chunks
