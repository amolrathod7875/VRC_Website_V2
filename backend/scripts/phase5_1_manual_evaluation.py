import asyncio
import time
import json
from datetime import datetime
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.generation.factory import LLMFactory
from app.rag.generation.generation_service import GenerationService
from app.rag.services.rag_service import RAGService
from app.rag.retrieval.query_classifier import classify_query


async def evaluate_question(question: str, service: RAGService) -> dict:
    start = time.perf_counter()
    try:
        result = await service.answer(question=question, filters=None)
    except Exception as exc:
        return {
            "question": question,
            "intent": classify_query(question).value,
            "answer": f"ERROR: {exc}",
            "sources": [],
            "retrieval_duration_ms": 0.0,
            "generation_duration_ms": 0.0,
            "total_duration_ms": (time.perf_counter() - start) * 1000,
            "pass": False,
        }
    retrieval = result.get("retrieval", {})
    return {
        "question": question,
        "intent": classify_query(question).value,
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "top_sources": [s.get("document", "") for s in result.get("sources", [])[:3]],
        "retrieval_duration_ms": retrieval.get("retrieval_duration_ms", 0.0),
        "generation_duration_ms": retrieval.get("generation_duration_ms", 0.0),
        "total_duration_ms": retrieval.get("total_duration_ms", 0.0),
        "pass": True,
    }


async def main():
    qdrant_store = QdrantStore()
    dense = DenseEmbeddingService()
    sparse = SparseEmbeddingService()
    retriever = HybridRetriever(qdrant_store=qdrant_store)
    reranker = Reranker()
    context_builder = ContextBuilder(reranker=reranker)
    try:
        llm = LLMFactory.create()
    except Exception as exc:
        print(f"Generation provider unavailable: {exc}")
        return
    generator = GenerationService(llm_provider=llm)
    service = RAGService(
        dense=dense,
        sparse=sparse,
        retriever=retriever,
        generator=generator,
        context_builder=context_builder,
    )

    questions = [
        "What is VR Coatings?",
        "What does VR Coatings manufacture?",
        "When was VR Coatings founded?",
        "Where is VR Coatings head office?",
        "What is the South India contact number?",
        "What is Tiger used for?",
        "Tiger 30:150 pressure ratio",
        "Tiger 30:150 output per cycle",
        "Does VR Coatings make electric cars?",
        "Does VR Coatings manufacture aircraft?",
        "Does VR Coatings sell laptops?",
        "Does Tiger support water-based coatings?",
        "Does Tiger 30:150 have a pressure ratio of 30:1?",
        "Does Tiger 30:150 have a pressure ratio of 90:1?",
        "What does UNKNOWN / TBC mean?",
        "How much does Tiger cost?",
        "Tell me about VR Coatings.",
        "What products does VR Coatings make?",
    ]

    results = []
    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] Evaluating: {question}")
        result = await evaluate_question(question, service)
        results.append(result)
        print(f"  Intent: {result['intent']}")
        print(f"  Answer: {result['answer'][:200]}")
        print(f"  Top sources: {result['top_sources']}")
        print(f"  Latency: {result['total_duration_ms']:.0f}ms")
        print()

    output_path = f"phase5_1_manual_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
