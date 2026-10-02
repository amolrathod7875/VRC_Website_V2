import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.retrieval.hybrid_retriever import HybridRetriever
from app.rag.retrieval.context_builder import ContextBuilder
from app.rag.retrieval.reranker import Reranker
from app.rag.config import rag_settings

async def debug_question(question: str):
    print(f"\n{'='*80}")
    print(f"QUESTION: {question}")
    print(f"{'='*80}")
    
    qdrant_store = QdrantStore()
    dense = DenseEmbeddingService()
    sparse = SparseEmbeddingService()
    retriever = HybridRetriever(qdrant_store=qdrant_store)
    reranker = Reranker()
    context_builder = ContextBuilder(reranker=reranker)
    
    dense_query = dense.embed_query(question)
    sparse_query = sparse.embed_query(question)
    chunks = await retriever.retrieve(dense_query=dense_query, sparse_query=sparse_query)
    
    print(f"\nRetrieved {len(chunks)} chunks")
    print(f"\nTop 5 chunks:")
    for i, chunk in enumerate(chunks[:5], 1):
        text = chunk.get('text', '')[:200]
        source = chunk.get('source_type', 'unknown')
        doc = chunk.get('document_name', 'unknown')
        model = chunk.get('model', 'N/A')
        score = chunk.get('score', 0)
        print(f"\n{i}. [{source}] {doc} | model={model} | score={score:.4f}")
        print(f"   Text: {text}...")
    
    built = context_builder.build(chunks, question)
    context = built.get('context', '')
    print(f"\n\nBuilt context ({len(context)} chars):")
    print(f"{'='*80}")
    print(context[:2000])
    print(f"{'='*80}\n")

async def main():
    questions = [
        "Give me every technical specification available for Tiger 30:150.",
        "Compare the available Tiger models only using indexed information.",
    ]
    for q in questions:
        await debug_question(q)

if __name__ == "__main__":
    asyncio.run(main())
