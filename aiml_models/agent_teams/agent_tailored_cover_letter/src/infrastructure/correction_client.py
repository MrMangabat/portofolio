import httpx
from typing import List, Literal, Dict
from src.config.config_top_level import ConfigTopLevel

class CorrectionsClient:
    def __init__(self) -> None:
        self.config = ConfigTopLevel()
        self.base_url = "http://localhost:8010/corrections"

    def fetch_corrections(self, correction_type: Literal["word", "sentence", "skill"]) -> List[Dict[str, str]]:
        response = httpx.get(self.base_url, params={"correction_type": correction_type})
        response.raise_for_status()
        return response.json()  # Ensure it returns a list of dictionaries
