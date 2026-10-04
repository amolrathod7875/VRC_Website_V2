"""
Phase 9C.3 — Batch 2 Retrieval Validation
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.generation.generation_service import GenerationService
from app.rag.generation.factory import LLMFactory
from app.rag.config import rag_settings
from app.core.database import async_session_factory
from sqlalchemy import select
from app.models.rag_document import RagDocument


async def get_qdrant_counts():
    from qdrant_client import QdrantClient
    from collections import Counter
    client = QdrantClient(url=rag_settings.QDRANT_URL, api_key=rag_settings.QDRANT_API_KEY or None)
    col = rag_settings.QDRANT_COLLECTION_NAME
    points, _ = client.scroll(collection_name=col, limit=10000, with_payload=True)
    doc_counts = Counter(p.payload.get('document_name') for p in points if p.payload)
    return dict(doc_counts)


async def retrieve_and_print(question: str, product_filter: str = None):
    qdrant_store = QdrantStore()
    dense = DenseEmbeddingService()
    sparse = SparseEmbeddingService()
    retriever = HybridRetriever(qdrant_store=qdrant_store)
    reranker = Reranker()
    context_builder = ContextBuilder(reranker=reranker)

    dense_query = dense.embed_query(question)
    sparse_query = sparse.embed_query(question)
    filters = {}
    if product_filter:
        filters["product_slug"] = product_filter
    chunks = await retriever.retrieve(dense_query=dense_query, sparse_query=sparse_query, filters=filters or None)

    print(f"\nQuestion: {question}")
    if product_filter:
        print(f"Product filter: {product_filter}")
    print(f"Retrieved {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:5], 1):
        text = chunk.get('text', '')[:200]
        doc = chunk.get('document_name', 'unknown')
        model = chunk.get('model', 'N/A')
        score = chunk.get('score', 0)
        product = chunk.get('product_slug', 'unknown')
        print(f"  {i}. [{doc}] product={product} model={model} score={score:.4f}")
        print(f"     Text: {text}...")
    return chunks


async def generate_answer(question: str, chunks: list):
    llm = LLMFactory.create()
    gen = GenerationService(llm_provider=llm)
    context_builder = ContextBuilder(reranker=Reranker())
    built = context_builder.build(chunks, question)
    context = built.get('context', '')
    try:
        result = await gen.generate_answer(question, context)
        answer = result.get('answer', '')
        print(f"\nAnswer: {answer[:500]}")
    except Exception as e:
        print(f"\nGeneration failed: {e}")
        print(f"Context ({len(context)} chars): {context[:500]}")


async def main():
    print("=" * 60)
    print("PHASE 9C.3 — BATCH 2 RETRIEVAL VALIDATION")
    print("=" * 60)

    # Check current Qdrant state
    counts = await get_qdrant_counts()
    print("\n[QDRANT STATE]")
    for name, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {name}: {count}")
    total = sum(counts.values())
    print(f"  TOTAL: {total}")

    # A. Paint Preparation Unit queries
    print("\n[RETRIEVAL TESTS — PAINT PREPARATION UNIT]")
    chunks = await retrieve_and_print("What is the Paint Preparation Unit?", product_filter="paint-preparation-unit")
    chunks = await retrieve_and_print("What is it used for?", product_filter="paint-preparation-unit")
    chunks = await retrieve_and_print("What are its technical specifications?", product_filter="paint-preparation-unit")

    # B. Portable Pressure Feed Pot queries
    print("\n[RETRIEVAL TESTS — PORTABLE PRESSURE FEED POT]")
    chunks = await retrieve_and_print("What is the capacity of the Portable Pressure Feed Pot?", product_filter="portable-pressure-feed-pot")
    chunks = await retrieve_and_print("What is its maximum working pressure?", product_filter="portable-pressure-feed-pot")
    chunks = await retrieve_and_print("What is its net weight?", product_filter="portable-pressure-feed-pot")

    # C. Turbine queries
    print("\n[RETRIEVAL TESTS — TURBINE]")
    chunks = await retrieve_and_print("What is the Turbine Stirrer?", product_filter="turbine")
    chunks = await retrieve_and_print("What turbine stirrer variants are available?", product_filter="turbine")
    chunks = await retrieve_and_print("Tell me about TB-70.", product_filter="turbine")
    chunks = await retrieve_and_print("Tell me about TB-110.", product_filter="turbine")
    chunks = await retrieve_and_print("Tell me about TB-180.", product_filter="turbine")

    # D. Cross-product tests
    print("\n[CROSS-PRODUCT TESTS]")
    chunks = await retrieve_and_print("What is the pressure ratio of LION?", product_filter="lion")
    chunks = await retrieve_and_print("Tell me about Leopard.", product_filter="leopard")
    chunks = await retrieve_and_print("Tell me about Tiger.", product_filter="tiger")

    # E. Turbine/Pneumatic Stirrer isolation
    print("\n[TURBINE/PNEUMATIC STIRRER ISOLATION]")
    chunks = await retrieve_and_print("What is the Turbine Stirrer?", product_filter="turbine")
    turbine_docs = set(c.get('document_name', '') for c in chunks if c.get('product_slug') == 'turbine')
    print(f"  Turbine docs in Turbine query: {turbine_docs}")
    # Pneumatic Stirrer is not indexed, so it should not appear
    assert "PNEUMATIC STIRRER.pdf" not in turbine_docs, "Pneumatic Stirrer should not be indexed"

    # F. Price guard
    print("\n[PRICE GUARD TESTS]")
    chunks = await retrieve_and_print("How much does the Paint Preparation Unit cost?", product_filter="paint-preparation-unit")
    chunks = await retrieve_and_print("How much does the Portable Pressure Feed Pot cost?", product_filter="portable-pressure-feed-pot")
    chunks = await retrieve_and_print("How much does the Turbine Stirrer cost?", product_filter="turbine")

    # G. PostgreSQL document count
    print("\n[POSTGRESQL DOCUMENT COUNT]")
    async with async_session_factory() as db:
        result = await db.execute(select(RagDocument))
        docs = result.scalars().all()
        print(f"  Total RagDocument records: {len(docs)}")
        for doc in docs:
            print(f"    {doc.document_name}: sha256={doc.sha256[:16]}..., status={doc.status}, chunks={doc.chunk_count}")

    print("\n" + "=" * 60)
    print("RETRIEVAL VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
