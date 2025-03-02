# backend/services/service_cover_letter/src/config/config_top_level.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file

class Config:
    """Top-level configuration for the Cover Letter microservice."""

    # PostgreSQL Settings (Loaded from .env)
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    # Construct Database URL
    POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Qdrant Database
    QDRANT_URL = os.getenv("QDRANT_URL")

    # MinIO Configuration
    MINIO_HOST = os.getenv("MINIO_HOST")
    MINIO_PORT = os.getenv("MINIO_PORT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
