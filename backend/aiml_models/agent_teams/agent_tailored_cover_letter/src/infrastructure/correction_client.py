#  backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/correction_client.py
import httpx
from typing import List, Literal
from src.config.config_top_level import ConfigTopLevel

class CorrectionsClient:
    def __init__(self) -> None:
        self.config = ConfigTopLevel.load_config()
        self.base_url = "http://localhost:8010/corrections"

    def fetch_corrections(self, correction_type: Literal["word", "sentence", "skill"]) -> List[str]:
        response = httpx.get(self.base_url, params={"correction_type": correction_type})
        response.raise_for_status()
        return response.json()  # This gives you a proper list of dicts
