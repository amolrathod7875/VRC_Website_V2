from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str, context: str) -> str:
        raise NotImplementedError
