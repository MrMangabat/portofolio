# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/correction_client.py

"""
This client fetches word/sentence/skill corrections from the cover letter service.
It performs an HTTP GET request and returns validated correction entries.

Purpose:
    Acts as a client-side utility to retrieve constraint rules for editorial or generation logic.

Capabilities:
    - Can fetch any correction type by specifying: 'word', 'sentence', or 'skill'.
    - Raises if API call fails.
    
Reasoning:
    Isolates inter-service HTTP call logic from business logic for modularity and easier testing.
"""

import httpx
from typing import List, Literal, Dict
from src.config.service_settings import AgentSettings  # ✅ new config location

class CorrectionsClient:
    def __init__(self) -> None:
        self.config = AgentSettings()
        self.base_url: str = f"http://{self.config.CORRECTION_API_URL}/corrections"
        print(f"CorrectionsClient initialized with base URL: {self.base_url}")
        
    def fetch_corrections(self, correction_type: Literal["word", "sentence", "skill"]) -> List[Dict[str, str]]:
        """
        Calls the corrections API and returns a list of correction dictionaries.
        """
        print(f"Fetching corrections of type: {correction_type} from {self.base_url}")
        print(f"Fetching corrections of type: {correction_type} from {self.base_url}")

        response = httpx.get(self.base_url, params={"correction_type": correction_type})
        response.raise_for_status()
        return response.json()
