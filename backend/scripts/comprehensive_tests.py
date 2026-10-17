"""
Product discovery, price guard, regression, and multi-turn context tests.
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

async def test_query(rag_service: RAGService, query: str, filters: dict = None, recent_messages=None):
    try:
        result = await rag_service.answer(query, filters=filters, recent_messages=recent_messages)
        return result
    except Exception as e:
        logger.error(f"Query failed: {query} - {e}")
        return {"error": str(e)}

async def main():
    rag_service = build_rag_service()
    
    print("=" * 60)
    print("PRODUCT DISCOVERY, PRICE GUARD, REGRESSION, MULTI-TURN TESTS")
    print("=" * 60)
    
    # 17. PRODUCT DISCOVERY
    print("\n>>> PRODUCT DISCOVERY TESTS")
    print("-" * 40)
    
    r1 = await test_query(rag_service, "What systems are available for fireproof coating applications?")
    print(f"Q: What systems are available for fireproof coating applications?")
    print(f"A: {r1.get('answer', 'ERROR')[:400]}")
    print(f"Sources: {len(r1.get('sources', []))}")
    
    r2 = await test_query(rag_service, "Which system should I use for high viscosity two-component materials?")
    print(f"\nQ: Which system should I use for high viscosity two-component materials?")
    print(f"A: {r2.get('answer', 'ERROR')[:400]}")
    print(f"Sources: {len(r2.get('sources', []))}")
    
    # 18. PRICE GUARD
    print("\n>>> PRICE GUARD TESTS")
    print("-" * 40)
    
    r3 = await test_query(rag_service, "What is the price of Dragon?")
    print(f"Q: What is the price of Dragon?")
    print(f"A: {r3.get('answer', 'ERROR')[:400]}")
    print(f"Sources: {len(r3.get('sources', []))}")
    
    r4 = await test_query(rag_service, "How much does Polyurea cost?")
    print(f"\nQ: How much does Polyurea cost?")
    print(f"A: {r4.get('answer', 'ERROR')[:400]}")
    print(f"Sources: {len(r4.get('sources', []))}")
    
    r5 = await test_query(rag_service, "What is the price of Barrel Pump?")
    print(f"\nQ: What is the price of Barrel Pump?")
    print(f"A: {r5.get('answer', 'ERROR')[:400]}")
    print(f"Sources: {len(r5.get('sources', []))}")
    
    # 19. EXISTING REGRESSION MATRIX
    print("\n>>> REGRESSION MATRIX TESTS")
    print("-" * 40)
    
    regression_tests = [
        ("Tiger 30:150", "What is the discharge per cycle for Tiger 30:150?"),
        ("Tiger 30:150 ratio", "What is the pressure ratio for Tiger 30:150?"),
        ("LION", "What is LION?"),
        ("Rhino", "What is Rhino?"),
        ("Elephant", "What is Elephant?"),
        ("Cheetah", "What is Cheetah?"),
        ("Hippo", "What is Hippo?"),
        ("Leopard", "What is Leopard?"),
        ("Filters", "What filters are available?"),
        ("CUB", "What is CUB?"),
        ("Drum Press", "What is Drum Press?"),
        ("Pneumatic Stirrer", "What is Pneumatic Stirrer?"),
        ("Ball Valves", "What are Ball Valves?"),
        ("Turbine", "What is Turbine?"),
        ("HAWK", "What is HAWK?"),
        ("FALCON", "What is FALCON?"),
        ("Kingfisher", "What is Kingfisher?"),
        ("VRIA", "What is VRIA?"),
        ("VRC MIX HP", "What is VRC MIX HP?"),
    ]
    
    for name, query in regression_tests:
        r = await test_query(rag_service, query)
        answer = r.get('answer', 'ERROR')[:300]
        # Check for identity confusion
        confused = "ERROR" if any(x in answer.lower() for x in ["tiger", "lion", "rhino", "elephant", "cheetah", "hippo", "leopard"]) and name.lower() not in answer.lower() else ""
        print(f"  {name}: {answer} {confused}")
    
    # 20. MULTI-TURN CONTEXT
    print("\n>>> MULTI-TURN CONTEXT TESTS")
    print("-" * 40)
    
    # Test 1: Tiger 30:150 -> general question
    print("\n  Test: Tiger 30:150 -> general follow-up")
    r_tiger = await test_query(rag_service, "What is Tiger 30:150?")
    print(f"  Q1: What is Tiger 30:150? -> {r_tiger.get('answer', 'ERROR')[:150]}")
    r_tiger2 = await test_query(rag_service, "What is its discharge per cycle?", recent_messages=[
        {"role": "user", "content": "What is Tiger 30:150?"},
        {"role": "assistant", "content": r_tiger.get('answer', '')}
    ])
    print(f"  Q2: What is its discharge per cycle? -> {r_tiger2.get('answer', 'ERROR')[:150]}")
    
    # Test 2: Dragon -> Polyurea
    print("\n  Test: Dragon -> Polyurea variant follow-up")
    r_dragon = await test_query(rag_service, "What is Dragon?")
    print(f"  Q1: What is Dragon? -> {r_dragon.get('answer', 'ERROR')[:150]}")
    r_poly = await test_query(rag_service, "What variants does Polyurea have?", recent_messages=[
        {"role": "user", "content": "What is Dragon?"},
        {"role": "assistant", "content": r_dragon.get('answer', '')}
    ])
    print(f"  Q2: What variants does Polyurea have? -> {r_poly.get('answer', 'ERROR')[:150]}")
    
    # Test 3: VRC MIX HP -> VRC MIX Low Medium
    print("\n  Test: VRC MIX HP -> VRC MIX Low Medium technical follow-up")
    r_vrc_hp = await test_query(rag_service, "What is VRC MIX HP?")
    print(f"  Q1: What is VRC MIX HP? -> {r_vrc_hp.get('answer', 'ERROR')[:150]}")
    r_vrc_lm = await test_query(rag_service, "What is its mixing ratio range?", recent_messages=[
        {"role": "user", "content": "What is VRC MIX HP?"},
        {"role": "assistant", "content": r_vrc_hp.get('answer', '')}
    ])
    print(f"  Q2: What is its mixing ratio range? -> {r_vrc_lm.get('answer', 'ERROR')[:150]}")
    
    # Test 4: Barrel Pump -> Tiger
    print("\n  Test: Barrel Pump -> Tiger pressure ratio")
    r_barrel = await test_query(rag_service, "What is Barrel Pump?")
    print(f"  Q1: What is Barrel Pump? -> {r_barrel.get('answer', 'ERROR')[:150]}")
    r_tiger3 = await test_query(rag_service, "What is its pressure ratio?", recent_messages=[
        {"role": "user", "content": "What is Barrel Pump?"},
        {"role": "assistant", "content": r_barrel.get('answer', '')}
    ])
    print(f"  Q2: What is its pressure ratio? -> {r_tiger3.get('answer', 'ERROR')[:150]}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())