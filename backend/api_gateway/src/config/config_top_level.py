#backend/api_gateway/src/config/config_top_level.py
from pydantic_settings import BaseSettings
from typing import List

class TopLevelSettings(BaseSettings):
    API_BASE_URL: str = "http://localhost:8080"
    COVER_LETTER_SERVICE_URL: str = "http://localhost:8001"
    allowed_origins: str = "http://localhost,http://localhost:5173,http://localhost:8080,http://frontend:5173,http://api_gateway:8080"

    class Config:
        env_file = ".env"

    # Optional: Helper method to split into list
    def get_allowed_origins_list(self) -> List[str]:
        return self.allowed_origins.split(",")
    
# For ease of import elsewhere:
api_gateway_top_level_configs = TopLevelSettings()

