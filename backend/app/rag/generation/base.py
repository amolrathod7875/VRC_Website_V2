from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str, context: str) -> str:
        raise NotImplementedError

    @property
    def provider_name(self) -> str:
        return type(self).__name__.lower().replace("provider", "")

    @property
    def model_name(self) -> str:
        return "unknown"
