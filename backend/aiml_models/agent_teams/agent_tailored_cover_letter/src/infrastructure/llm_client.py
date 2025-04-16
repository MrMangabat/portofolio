# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/llm_client.py

import httpx

# from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from src.config.config_top_level import ConfigTopLevel
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResult
from typing import List

from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage
from typing import List
from langchain.schema import BaseMessage
from langchain_openai import ChatOpenAI


# src/core/llm_client/llm_client.py

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from typing import Dict
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv
import os


class LLMClient:
    """
    Purpose:
        This client wraps LangChain-compatible LLMs (Ollama & OpenAI) and provides a pipe-compatible interface.

    Capabilities:
        - Stores initialized LLMs ready for LangChain `Runnable` chaining using `|`.
        - Supports LLMs: llama3.2:3b, deepseek-r1 via Ollama; gpt-4o via OpenAI.

    Reasoning:
        Designed to expose pipe-compatible models for LangChain chains, so `prompt | model | parser` works.

    Methods:
        - get_model(name: str) -> BaseChatModel: Returns the corresponding LangChain `Runnable` model.
    """

    models: Dict[str, BaseChatModel]

    def __init__(self) -> None:
        load_dotenv()  # Load environment variables from .env

        openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            raise EnvironmentError("OPENAI_API_KEY is missing from the environment or .env file.")

        # Initialize LangChain-compatible models
        self.models = {
            "ollama": ChatOllama(
                model="llama3.2:3b",
                seed=66
            ),
            "deepseek": ChatOllama(
                model="deepseek-r1",
                seed=66
            ),
            "gpt": ChatOpenAI(
                model="gpt-4o-2024-11-20",
                api_key=openai_api_key,
                seed=66
            )
        }

    def get_model(self, name: str) -> BaseChatModel:
        """
        Retrieves a LangChain-compatible chat model.

        Args:
            name (str): Model key, one of: ["ollama", "deepseek", "gpt"]

        Returns:
            BaseChatModel: A model that can be used in LangChain `Runnable` pipelines.

        Raises:
            ValueError: If the requested model name is not registered.
        """
        if name not in self.models:
            raise ValueError(f"Model '{name}' is not supported. Available models: {list(self.models.keys())}")
        return self.models[name]
