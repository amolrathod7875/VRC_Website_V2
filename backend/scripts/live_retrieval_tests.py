"""
Live retrieval tests for final 5 catalogues after ingestion.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
from app.rag.services.rag_service import RAGService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.reranker import Reranker
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.generation.factory import LLMFactory
from app.rag.generation.generation_service import GenerationService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_rag_service():
    qdrant_store = QdrantStore()
    dense = DenseEmbeddingService()
    sparse = SparseEmbeddingService()
    retriever = HybridRetriever(qdrant_store=qdrant_store)
    reranker = Reranker()
    context_builder = ContextBuilder(reranker=reranker)
    llm = LLMFactory.create()
    generator = GenerationService(llm_provider=llm)
    return RAGService(
        dense=dense,
        sparse=sparse,
        retriever=retriever,
        generator=generator,
        context_builder=context_builder,
    )

async def test_query(rag_service: RAGService, query: str, filters: dict = None):
    """Test a query and return results."""
    try:
        result = await rag_service.answer(query, filters=filters)
        return result
    except Exception as e:
        logger.error(f"Query failed: {query} - {e}")
        return {"error": str(e)}

async def main():
    rag_service = build_rag_service()
    
    print("=" * 60)
    print("LIVE RETRIEVAL TESTS - FINAL 5 CATALOGUES")
    print("=" * 60)
    
    # 11. DRAGON LIVE RETRIEVAL
    print("\n>>> DRAGON TESTS")
    print("-" * 40)
    
    r1 = await test_query(rag_service, "What is Dragon?")
    print(f"Q: What is Dragon?")
    print(f"A: {r1.get('answer', 'ERROR')[:300]}")
    print(f"Sources: {len(r1.get('sources', []))}")
    
    r2 = await test_query(rag_service, "What configurations are available for Dragon?")
    print(f"\nQ: What configurations are available for Dragon?")
    print(f"A: {r2.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r2.get('sources', []))}")
    
    # 12. POLYUREA LIVE RETRIEVAL
    print("\n>>> POLYUREA TESTS")
    print("-" * 40)
    
    r3 = await test_query(rag_service, "What is the Polyurea system?")
    print(f"Q: What is the Polyurea system?")
    print(f"A: {r3.get('answer', 'ERROR')[:300]}")
    print(f"Sources: {len(r3.get('sources', []))}")
    
    r4 = await test_query(rag_service, "What variants are available for Polyurea?")
    print(f"\nQ: What variants are available for Polyurea?")
    print(f"A: {r4.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r4.get('sources', []))}")
    
    r5 = await test_query(rag_service, "What is the pressure ratio for Polyurea 50:1 variant?")
    print(f"\nQ: What is the pressure ratio for Polyurea 50:1 variant?")
    print(f"A: {r5.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r5.get('sources', []))}")
    
    # 13. TUBE VARNISH LIVE RETRIEVAL
    print("\n>>> TUBE VARNISH TESTS")
    print("-" * 40)
    
    r6 = await test_query(rag_service, "What is the Tube Varnish Coating System?")
    print(f"Q: What is the Tube Varnish Coating System?")
    print(f"A: {r6.get('answer', 'ERROR')[:300]}")
    print(f"Sources: {len(r6.get('sources', []))}")
    
    r7 = await test_query(rag_service, "What are the main components of the Tube Varnish Coating System?")
    print(f"\nQ: What are the main components of the Tube Varnish Coating System?")
    print(f"A: {r7.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r7.get('sources', []))}")
    
    r8 = await test_query(rag_service, "What is the process or workflow for the Tube Varnish Coating System?")
    print(f"\nQ: What is the process or workflow for the Tube Varnish Coating System?")
    print(f"A: {r8.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r8.get('sources', []))}")
    
    # 14. VRC MIX LOW-MEDIUM LIVE TEST
    print("\n>>> VRC MIX LOW-MEDIUM TESTS")
    print("-" * 40)
    
    r9 = await test_query(rag_service, "What is VRC MIX Low-Medium Pressure?")
    print(f"Q: What is VRC MIX Low-Medium Pressure?")
    print(f"A: {r9.get('answer', 'ERROR')[:300]}")
    print(f"Sources: {len(r9.get('sources', []))}")
    
    r10 = await test_query(rag_service, "What is the mixing ratio range for VRC MIX Low-Medium Pressure?")
    print(f"\nQ: What is the mixing ratio range for VRC MIX Low-Medium Pressure?")
    print(f"A: {r10.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r10.get('sources', []))}")
    
    r11 = await test_query(rag_service, "What is VRC MIX HP?")
    print(f"\nQ: What is VRC MIX HP?")
    print(f"A: {r11.get('answer', 'ERROR')[:300]}")
    print(f"Sources: {len(r11.get('sources', []))}")
    
    # 15. BARREL LIVE RETRIEVAL
    print("\n>>> BARREL PUMP TESTS")
    print("-" * 40)
    
    r12 = await test_query(rag_service, "What is Barrel Pump?")
    print(f"Q: What is Barrel Pump?")
    print(f"A: {r12.get('answer', 'ERROR')[:300]}")
    print(f"Sources: {len(r12.get('sources', []))}")
    
    r13 = await test_query(rag_service, "What pressure ratios are available for Barrel Pump?")
    print(f"\nQ: What pressure ratios are available for Barrel Pump?")
    print(f"A: {r13.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r13.get('sources', []))}")
    
    r14 = await test_query(rag_service, "What is the discharge per cycle for Barrel Pump?")
    print(f"\nQ: What is the discharge per cycle for Barrel Pump?")
    print(f"A: {r14.get('answer', 'ERROR')[:500]}")
    print(f"Sources: {len(r14.get('sources', []))}")
    
    print("\n" + "=" * 60)
    print("LIVE RETRIEVAL TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())