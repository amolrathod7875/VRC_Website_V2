"""Startup sanity checks for evaluation."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def check_imports() -> None:
    """Verify all required modules can be imported."""
    try:
        from app.rag.config import rag_settings  # noqa: F401
    except Exception as exc:
        raise RuntimeError(f"Failed to import rag_settings: {exc}") from exc

    try:
        from app.rag.retrieval.hybrid_retriever import HybridRetriever  # noqa: F401
        from app.rag.embeddings.dense import DenseEmbeddingService  # noqa: F401
        from app.rag.embeddings.sparse import SparseEmbeddingService  # noqa: F401
        from app.rag.retrieval.reranker import Reranker  # noqa: F401
    except Exception as exc:
        raise RuntimeError(f"Failed to import retrieval components: {exc}") from exc
