# aiml_models/agent_teams/agent_tailored_cover_letter/src/config/config_low_level.py

"""
Purpose:
Provides low-level infrastructure connections (PostgreSQL, MinIO, Qdrant) for AI agent.

Capabilities:
- Centralized DB/session creation
- Qdrant + MinIO clients

Reasoning:
Keeps separation of infra from business logic. Still avoids Pydantic for clarity at this stage.

!!!!!!!!
pydantic base settings must be used in the future
!!!!!!!!
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from minio import Minio
from qdrant_client import QdrantClient, models
from typing import Generator
from src.config.config_top_level import ConfigTopLevel

# Load configuration
config: ConfigTopLevel = ConfigTopLevel()

class PostgresConnection:
    engine = create_engine(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def get_db() -> Generator:
        db = PostgresConnection.SessionLocal()
        try:
            yield db
        finally:
            db.close()

class MinioConnection:
    def __init__(self) -> None:
        self.client: Minio = Minio(
            endpoint=f"{config.MINIO_HOST}:{config.MINIO_PORT}",
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False
        )

class QdrantConnection:
    def __init__(self) -> None:
        self.url: str = config.QDRANT_URL
        # self.port: int = config.QDRANT_PORT
        self.default_collection: str = "embedded_cover_letters"

        self.client = QdrantClient(url=f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}")

        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        """
        Check if the default collection exists in Qdrant.
        If not, create it with appropriate vector configuration.
        """
        existing_collections = [c.name for c in self.client.get_collections().collections]

        if self.default_collection not in existing_collections:
            self.client.create_collection(
                collection_name=self.default_collection,
                vectors_config=models.VectorParams(
                    size=768,  # required for sentence-transformers
                    distance=models.Distance.COSINE
                )
            )
            print(f"✅ Created collection: {self.default_collection}")
        else:
            print(f"✅ Collection already exists: {self.default_collection}")