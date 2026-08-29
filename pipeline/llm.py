import os

from langchain_openai import ChatOpenAI

BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterProvider:
    """Creates LLM clients per agent role, all pointed at OpenRouter."""

    name = "openrouter"

    def __init__(self, models=None, api_key=""):
        self.models = models or {}
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")

    def llm(self, role, **kwargs):
        model = self.models.get(role) or self.models.get("default")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set.")
        if not model:
            raise RuntimeError(f"no model configured for role '{role}'.")
        kwargs.setdefault("temperature", 0)
        return ChatOpenAI(model=model, api_key=self.api_key, base_url=BASE_URL, **kwargs)


__all__ = ["OpenRouterProvider"]
