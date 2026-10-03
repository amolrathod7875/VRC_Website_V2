"""
Phase 9A — Retrieval and Conversation Validation
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
    print("PHASE 9A — RETRIEVAL AND CONVERSATION VALIDATION")
    print("=" * 60)

    # Check current Qdrant state
    counts = await get_qdrant_counts()
    print("\n[QDRANT STATE]")
    for name, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {name}: {count}")
    total = sum(counts.values())
    print(f"  TOTAL: {total}")

    # A. Product queries for approved pilot products
    print("\n[RETRIEVAL TESTS — PRODUCT QUERIES]")
    for product, slug in [("Rhino", "rhino"), ("Elephant", "elephant")]:
        chunks = await retrieve_and_print(f"What is {product}?", product_filter=slug)

    # B. Technical specification queries
    print("\n[RETRIEVAL TESTS — TECHNICAL SPECIFICATIONS]")
    chunks = await retrieve_and_print("What is the pressure ratio of Rhino?", product_filter="rhino")
    chunks = await retrieve_and_print("What are the technical specifications of Elephant?", product_filter="elephant")

    # C. Exact model identifier queries
    print("\n[RETRIEVAL TESTS — MODEL IDENTIFIERS]")
    chunks = await retrieve_and_print("Tell me about Rhino 60:1", product_filter="rhino")

    # D. Conversation validation (multi-turn)
    print("\n[CONVERSATION TESTS — RHINO]")
    chunks1 = await retrieve_and_print("Tell me about Rhino.", product_filter="rhino")
    chunks2 = await retrieve_and_print("What is its pressure ratio?", product_filter="rhino")
    chunks3 = await retrieve_and_print("What applications is it used for?", product_filter="rhino")

    print("\n[CONVERSATION TESTS — ELEPHANT]")
    chunks1 = await retrieve_and_print("Tell me about Elephant.", product_filter="elephant")
    chunks2 = await retrieve_and_print("What is its pressure ratio?", product_filter="elephant")
    chunks3 = await retrieve_and_print("What applications is it used for?", product_filter="elephant")

    # E. Cross-product validation
    print("\n[CROSS-PRODUCT TESTS]")
    chunks = await retrieve_and_print("What is the pressure ratio of Rhino?", product_filter="rhino")
    chunks = await retrieve_and_print("What is the pressure ratio of Elephant?", product_filter="elephant")
    # Verify no cross-contamination
    rhino_docs = set(c.get('document_name', '') for c in chunks if c.get('product_slug') == 'rhino')
    elephant_docs = set(c.get('document_name', '') for c in chunks if c.get('product_slug') == 'elephant')
    print(f"  Rhino docs in Rhino query: {rhino_docs}")
    print(f"  Elephant docs in Elephant query: {elephant_docs}")

    # F. Price guard
    print("\n[PRICE GUARD TESTS]")
    chunks = await retrieve_and_print("How much does Rhino cost?", product_filter="rhino")
    chunks = await retrieve_and_print("How much does Elephant cost?", product_filter="elephant")

    # G. Comparison test
    print("\n[COMPARISON TESTS]")
    chunks = await retrieve_and_print("Compare Rhino and Elephant pressure ratios.")

    # H. Tiger preservation test
    print("\n[TIGER PRESERVATION TEST]")
    chunks = await retrieve_and_print("What is the Tiger pressure ratio?")
    tiger_count = sum(1 for c in chunks if c.get('document_name') == 'Tiger.pdf')
    print(f"  Tiger chunks retrieved: {tiger_count}")

    # I. PostgreSQL document count
    print("\n[POSTGRESQL DOCUMENT COUNT]")
    async with async_session_factory() as db:
        result = await db.execute(select(RagDocument))
        docs = result.scalars().all()
        print(f"  Total RagDocument records: {len(docs)}")
        for doc in docs:
            print(f"    {doc.document_name}: sha256={doc.sha256[:16]}..., status={doc.status}, chunks={doc.chunk_count}")

    # J. Manual source comparison spot checks
    print("\n[MANUAL OCR QUALITY SPOT CHECKS]")
    import json
    debug_dir = Path("rag_debug/phase9a_pilot")
    for slug in ["rhino", "elephant"]:
        ocr_file = debug_dir / slug / "ocr_results.json"
        if ocr_file.exists():
            ocr_data = json.loads(ocr_file.read_text(encoding="utf-8"))
            print(f"\n  {slug.upper()} OCR Results:")
            for page in ocr_data[:2]:
                print(f"    Page {page['page_number']}: {page['character_count']} chars, "
                      f"{page['block_count']} blocks, confidence={page.get('confidence', 'N/A')}")
                print(f"      Preview: {page['full_text_preview'][:200]}...")
                print(f"      Warnings: {page.get('warnings', [])}")
                print(f"      Technical IDs: {page.get('technical_identifiers', [])[:5]}")
        else:
            print(f"  {slug}: No debug artifacts found")

    print("\n" + "=" * 60)
    print("RETRIEVAL AND CONVERSATION VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
