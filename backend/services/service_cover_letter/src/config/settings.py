# backend/services/service_cover_letter/src/config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

from typing import Literal


class CoverLetterSettings(BaseSettings):
    ENV: Literal["dev", "prod", "test", "notebook"] = "dev"

    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def POSTGRES_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # MinIO
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_IP: str

    # Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int

    @property
    def QDRANT_URL(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    # Kafka (new additions)
    KAFKA_BROKER: str
    KAFKA_PORT: int
    KAFKA_TOPIC_FILE_UPLOADED: str
    KAFKA_BOOTSTRAP_SERVERS: str
    GROUP_ID: str

    # Logging
    LOG_LEVEL: str = "INFO"

    # OpenAI
    OPENAI_API_KEY: str = Field(..., alias="CHAT_GPT_API_KEY")

    # LLM Configuration
    LLM_MODEL: str = "gpt-4o"
    LLM_TEMPERATURE: float = 0.1

    # Agent Configuration
    AGENT_RECURSION_LIMIT: int = 50

    # Research Configuration
    RESEARCH_MAX_WORKERS: int = 4
    RESEARCH_TIMEOUT_MS: int = 30000

    # LangSmith Observability
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: str = "false"
    LANGSMITH_PROJECT: str = "cover-letter-service"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"

    class Config:
        env_file = ".env"
