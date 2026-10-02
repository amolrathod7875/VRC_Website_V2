import asyncio
import time
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.generation.generation_service import GenerationService
from app.rag.generation.factory import LLMFactory
from app.rag.generation.prompts import ANSWER_UNAVAILABLE
from app.rag.config import rag_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUESTIONS = [
    "What is VR Coatings?",
    "When was VR Coatings founded?",
    "Where is the head office?",
    "What is the South India contact number?",
    "What is Tiger used for?",
    "What is Tiger 30:150?",
    "What is Tiger 30:150 pressure ratio?",
    "What is Tiger 30:150 output per cycle?",
    "medium viscosity paint spraying equipment",
    "How much does Tiger cost?",
    "What does UNKNOWN / TBC mean?",
    "Does VR Coatings make electric cars?",
    "Tell me the price of Tiger 30:150.",
    "Give me every technical specification available for Tiger 30:150.",
    "Compare the available Tiger models only using indexed information.",
]


def build_service():
    qdrant_store = QdrantStore()
    dense = DenseEmbeddingService()
    sparse = SparseEmbeddingService()
    retriever = HybridRetriever(qdrant_store=qdrant_store)
    reranker = Reranker()
    context_builder = ContextBuilder(reranker=reranker)
    llm = LLMFactory.create()
    generator = GenerationService(llm_provider=llm)
    return dense, sparse, retriever, generator, context_builder


async def answer_question(question: str, service) -> dict:
    dense, sparse, retriever, generator, context_builder = service
    start = time.perf_counter()
    dense_query = dense.embed_query(question)
    sparse_query = sparse.embed_query(question)
    retrieval_start = time.perf_counter()
    chunks = await retriever.retrieve(dense_query=dense_query, sparse_query=sparse_query)
    retrieval_duration = (time.perf_counter() - retrieval_start) * 1000

    built = context_builder.build(chunks, question)
    context = built.get("context", "")
    sources = built.get("sources", [])
    selected_chunks = built.get("chunks", [])

    if not context:
        return {
            "answer": ANSWER_UNAVAILABLE,
            "sources": [],
            "retrieval": {"chunks_used": 0},
            "latency_ms": (time.perf_counter() - start) * 1000,
        }

    gen_start = time.perf_counter()
    gen_result = await generator.generate_answer(question=question, context=context)
    generation_duration = (time.perf_counter() - gen_start) * 1000
    total_duration = (time.perf_counter() - start) * 1000

    return {
        "answer": gen_result.get("answer", ANSWER_UNAVAILABLE),
        "sources": sources,
        "retrieval": {"chunks_used": len(selected_chunks)},
        "latency_ms": total_duration,
        "retrieval_duration_ms": retrieval_duration,
        "generation_duration_ms": generation_duration,
    }


async def main():
    print("=" * 80)
    print("PHASE 5 MANUAL GROQ EVALUATION")
    print("=" * 80)
    print(f"GROQ model: {rag_settings.GROQ_MODEL}")
    print(f"Qdrant collection: {rag_settings.QDRANT_COLLECTION_NAME}")
    print("=" * 80)
    print()

    service = build_service()
    results = []

    for i, question in enumerate(QUESTIONS, 1):
        print(f"QUESTION {i}: {question}")
        try:
            result = await answer_question(question, service)
        except Exception as exc:
            print(f"ERROR: {exc}")
            result = {"answer": f"ERROR: {exc}", "sources": [], "retrieval": {"chunks_used": 0}}

        print(f"RETRIEVED SOURCES: {len(result.get('sources', []))} sources")
        for src in result.get("sources", [])[:3]:
            print(f"  - {src.get('document')} | {src.get('source_type')} | model={src.get('model')}")

        print(f"ANSWER: {result.get('answer', '')[:500]}")
        print(f"CITATIONS: {len(result.get('sources', []))} sources used")
        print(f"LATENCY: {result.get('latency_ms', 0):.2f} ms")
        print(f"CHUNKS USED: {result.get('retrieval', {}).get('chunks_used', 0)}")
        print("-" * 80)
        results.append(result)

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for i, (question, result) in enumerate(zip(QUESTIONS, results), 1):
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        print(f"{i}. {question}")
        print(f"   Answer length: {len(answer)}")
        print(f"   Sources: {len(sources)}")
        print(f"   PASS (manual review required)")
        print()


if __name__ == "__main__":
    asyncio.run(main())
