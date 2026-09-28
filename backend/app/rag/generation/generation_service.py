from typing import Any, Dict, List
from app.rag.config import rag_settings
from app.rag.generation.base import BaseLLMProvider
from app.rag.generation.factory import LLMFactory
from app.rag.generation.prompts import SYSTEM_PROMPT
from app.rag.retrieval.context_builder import ContextBuilder


class GenerationService:
    def __init__(self, llm_provider: BaseLLMProvider, context_builder: ContextBuilder) -> None:
        self.llm_provider = llm_provider
        self.context_builder = context_builder

    async def generate_answer(self, question: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not chunks:
            return {
                "answer": "I couldn't find enough verified information in the VR Coatings knowledge base to answer that accurately.",
                "sources": [],
            }
        built = self.context_builder.build(chunks, question)
        context = built.get("context", "")
        sources = built.get("sources", [])
        if not context:
            return {
                "answer": "I couldn't find enough verified information in the VR Coatings knowledge base to answer that accurately.",
                "sources": [],
            }
        user_prompt = f"Question: {question}"
        answer = await self.llm_provider.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt, context=context)
        return {"answer": answer, "sources": sources}
