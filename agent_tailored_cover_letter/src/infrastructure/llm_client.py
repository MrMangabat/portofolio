# backend/aiml_models/

from typing import Dict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI
from src.config.service_settings import AgentSettings  # 👈 New

class LLMClient:
    """
    Purpose:
        This client wraps LangChain-compatible LLMs (Ollama & OpenAI) and provides a pipe-compatible interface.
    """

    models: Dict[str, BaseChatModel]

    def __init__(self) -> None:
        settings = AgentSettings()  # ✅ Now uses typed settings
        # openai_api_key: str = settings.OPENAI_API_KEY  # ✅ Pulled from env via pydantic

        self.models = {
            "ollama": ChatOllama(
                model="llama3:8b",
                # model="llama3.1:8b",
                seed=66,
                format="json"  # Enable JSON mode for structured outputs
            ),
            "deepseek": ChatOllama(
                model="deepseek-r1",
                seed=66,
                format="json"  # Enable JSON mode for structured outputs
            ),

        }

    def get_model(self, name: str) -> BaseChatModel:
        if name not in self.models:
            raise ValueError(f"Model '{name}' is not supported. Available models: {list(self.models.keys())}")
        return self.models[name]

