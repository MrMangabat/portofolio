# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/files_client.py

import httpx
from typing import List, Literal
from src.config.config_top_level import ConfigTopLevel

class CorrectionsClient:
    def __init__(self) -> None:
        self.config = ConfigTopLevel.load_config()
        self.base_url = f"{self.config.cover_letter_service_url}/corrections"

    def fetch_corrections(self, correction_type: Literal["word", "sentence", "skill"]) -> List[str]:
        response = httpx.get(self.base_url, params={"correction_type": correction_type})
        response.raise_for_status()

        return [item["text"] for item in response.json()]
