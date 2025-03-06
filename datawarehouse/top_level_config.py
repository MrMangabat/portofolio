# backend/core_configuration/config.py

import os
from dotenv import load_dotenv
from pathlib import Path

class Config:
    """Loads environment variables and provides configuration settings."""
    def __init__(self):
        env_path = Path(__file__).parent / '.env'
        load_dotenv(dotenv_path=env_path)

        # PostgreSQL configuration
        self.RELATIONAL_DATABASE_URL = os.getenv("POSTGRES_URL_DB")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")

        # MinIO configuration
        self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
        self.MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
        self.MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")

        # Qdrant configuration
        self.QDRANT_HOST = os.getenv("QDRANT_HOST")
        self.QDRANT_PORT = os.getenv("QDRANT_PORT")

        # General settings
        self.DEBUG = os.getenv("APP_DEBUG", "False").lower() == "true"  # This line converts the value to a boolean

