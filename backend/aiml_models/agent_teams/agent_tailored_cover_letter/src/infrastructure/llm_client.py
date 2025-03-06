# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/llm_client.py

import httpx
import json
from typing import List, Dict, Any
from src.config.config_top_level import ConfigTopLevel

class LLMClient:
    """
    Purpose:
        Handles interaction with the locally running Ollama service.

    Capabilities:
        - Sends structured messages (formatted prompt) to Ollama.
        - Supports configurable models (deepseek, llama2, etc.).
        - Handles response parsing and error checking.
    
    Reasoning:
        Keeping LLM interaction isolated ensures:
        ✅ No hard dependency on any specific model.
        ✅ Easy to swap models (DeepSeek now, maybe Llama3 later).
        ✅ Works seamlessly within the agent service.
    """

    def __init__(self, model: str = "deepseek") -> None:
        config = ConfigTopLevel.load_config()
        self.ollama_url = config.ollama_base_url
        self.model = model

    def invoke(self, messages: List) -> str:
        # Convert LangChain Messages to plain dict
        converted_messages = []
        for message in messages:
            if message.type == "system":
                converted_messages.append({"role": "system", "content": message.content})
            elif message.type == "human":
                converted_messages.append({"role": "user", "content": message.content})
            elif message.type == "ai":
                converted_messages.append({"role": "assistant", "content": message.content})
            else:
                raise ValueError(f"Unsupported message type: {message.type}")

        payload = {
            "model": self.model,
            "messages": converted_messages,
            "stream": False
        }

        response = httpx.post(f"{self.ollama_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]

