# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/llm_client.py

import httpx

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from src.config.config_top_level import ConfigTopLevel
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResult
from typing import List


class LLMClient:
    def __init__(self, model: str = "llama3.2:3b") -> None:
        config = ConfigTopLevel.load_config()
        self.ollama_url = config.ollama_base_url
        self.model = model

    def invoke(self, messages: List[BaseMessage]) -> str:
        converted_messages = []
        for message in messages:
            if isinstance(message, SystemMessage):
                converted_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                converted_messages.append({"role": "user", "content": message.content})
            else:
                raise ValueError(f"Unsupported message type: {message.type}")

        payload = {
            "model": self.model,
            "prompt": converted_messages,
            "format": {
                "type": "jsonschema",
                "schema": JobAnalysisResult.model_json_schema()
            },
            "stream": False
        }
        import json
        print("\n🛠️ Final Payload Sent to Ollama:")
        print(json.dumps(payload, indent=2))

        response = httpx.post(
            f"{self.ollama_url}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print("\n🔍 Raw Ollama Response Headers:")
        print(response.headers)
        print("\n🔍 Raw Ollama Response Text:")
        print(response.text)

        response.raise_for_status()
        return response.json()["response"]  # Corrected path for Ollama v0.5+
