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
class LLMClient:
    """
    Purpose:
        This client wraps Langchain-compatible LLMs (Ollama & OpenAI) and provides a simple interface.

    Models managed:
        - llama3.2:3b via Ollama
        - deepseek-r1 via Ollama
        - gpt-4o via OpenAI

    Methods:
        - get_model(name: str): Returns the corresponding LLM client.
    """

    def __init__(self) -> None:
        load_dotenv()  # Load .env file variables into environment
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            raise EnvironmentError("OPENAI_API_KEY not found in .env or environment variables.")

        self.models = {
            "llama": ChatOllama(
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
                ),
        }

    def get_model(self, name: str):
        """
        Returns the desired model instance.

        Args:
            name (str): One of ["llama", "deepseek", "gpt"]

        Raises:
            ValueError: If model name is not recognized.
        """
        if name not in self.models:
            raise ValueError(f"Model '{name}' is not available. Choose from: {list(self.models.keys())}")
        return self.models[name]





# class LLMClient:
#     def __init__(self, model: str = "llama3.2:3b") -> None:
#         config = ConfigTopLevel.load_config()
#         self.ollama_url = config.ollama_base_url
#         self.model = model

#     def invoke(self, messages: List[BaseMessage]) -> str:
#         converted_messages = []
#         for message in messages:
#             if isinstance(message, SystemMessage):
#                 converted_messages.append({"role": "system", "content": message.content})
#             elif isinstance(message, HumanMessage):
#                 converted_messages.append({"role": "user", "content": message.content})
#             else:
#                 raise ValueError(f"Unsupported message type: {message.type}")

#         payload = {
#             "model": self.model,
#             "prompt": converted_messages,
#             "format": {
#                 "type": "jsonschema",
#                 "schema": JobAnalysisResult.model_json_schema()
#             },
#             "stream": False
#         }
#         import json
#         print("\n🛠️ Final Payload Sent to Ollama:")
#         print(json.dumps(payload, indent=2))

#         response = httpx.post(
#             f"{self.ollama_url}/api/generate",
#             json=payload,
#             headers={"Content-Type": "application/json"}
#         )
#         print("\n🔍 Raw Ollama Response Headers:")
#         print(response.headers)
#         print("\n🔍 Raw Ollama Response Text:")
#         print(response.text)

#         response.raise_for_status()
#         return response.json()["response"]  # Corrected path for Ollama v0.5+
