# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/config/config_top_level.py
from dotenv import load_dotenv
import os

from pydantic import BaseModel
from dotenv import load_dotenv
import os

class ConfigTopLevel(BaseModel):
    ollama_base_url: str

    @classmethod
    def load_config(cls) -> "ConfigTopLevel":
        load_dotenv()
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        )
