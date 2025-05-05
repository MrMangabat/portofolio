# /aiml_models/agent_teams/agent_tailored_cover_letter/src/config/config_top_level.py
# aiml_models/agent_teams/agent_tailored_cover_letter/src/config/config_top_level.py

"""
Purpose:
Loads environment variables explicitly for the AI agent cover letter service.

Capabilities:
- Reads values from .env file using os.getenv.
- Keeps parity with backend's config_top_level structure.

Reasoning:
Avoids BaseSettings for now due to simplicity and user familiarity.


!!!!!!!!
pydantic base settings must be used in the future
!!!!!!!!
"""

import os
from dotenv import load_dotenv

# Load from the local .env file
load_dotenv(dotenv_path="aiml_models/agent_teams/agent_tailored_cover_letter/src/.env")

class ConfigTopLevel:
    # PostgreSQL
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "")

    # Qdrant
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")

    # MinIO
    MINIO_HOST: str = os.getenv("MINIO_HOST", "")
    MINIO_PORT: str = os.getenv("MINIO_PORT", "")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "")

    # Ollama or LLM fallback
    LLM_HOST: str = os.getenv("LLM_HOST", "http://127.0.0.1:11434")

    # Optional
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
