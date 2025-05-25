# backend/api_gateway/src/config/api_gateway_settings.py
from pydantic_settings import BaseSettings
from typing import List

class APIGatewaySettings(BaseSettings):
    API_BASE_URL: str = "http://localhost:8080"
    COVER_LETTER_SERVICE_URL: str = "http://service_cover_letter:8010"

    allowed_origins: str = "http://localhost,http://localhost:5173,http://localhost:8080"

    class Config:
        env_file = ".env"

    def get_allowed_origins_list(self) -> List[str]:
        return self.allowed_origins.split(",")
