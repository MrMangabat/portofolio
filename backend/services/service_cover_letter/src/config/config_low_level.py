# backend/services/service_cover_letter/src/config/config_low_level.py

"""
This module handles all infrastructure connections for the 'cover_letter' service.
It is intentionally placed within the service boundary to prevent cross-service coupling.
Configuration is static and changes only if the infrastructure itself changes.

!!!!!!!!
pydantic base settings must be used in the future
!!!!!!!!
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.config_top_level import Config
from minio import Minio
from typing import Optional
from qdrant_client import QdrantClient, models

config = Config()

class PostgressConnection:
    Base = declarative_base()
    engine = create_engine(config.POSTGRES_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def get_db():
        db = PostgressConnection.SessionLocal()
        try:
            yield db
        finally:
            db.close()

class PostgressConnection:
    Base = declarative_base()
    engine = create_engine(config.POSTGRES_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def get_db():
        db = PostgressConnection.SessionLocal()
        try:
            yield db
        finally:
            db.close()



class MiniOConnection:
    _instance: Optional["MiniOConnection"] = None

    def __init__(self) -> None:
        minio_ip = self._read_minio_ip()
        print(f"🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑 Connecting to MinIO with:")
        print(f"   Host: {minio_ip}")
        print(f"   Port: {config.MINIO_PORT}")
        print(f"   Access Key: {config.MINIO_ACCESS_KEY}")
        print(f"   Secret Key: {config.MINIO_SECRET_KEY}")

        self.client: Minio = Minio(
            endpoint=f"{minio_ip}:{config.MINIO_PORT}",
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False
        )
        self._validate_connection()

    @staticmethod
    def _read_minio_ip() -> str:
        resolved_env_path = "/app/service_cover_letter/src/resolved_env.env"
        with open(resolved_env_path, "r") as file:
            for line in file:
                if line.startswith("MINIO_IP="):
                    return line.strip().split("=")[1]
        raise RuntimeError("❌ MINIO_IP not found in resolved_env.env")

    def _validate_connection(self) -> None:
        try:
            buckets = self.client.list_buckets()
            print(f"✅ Connected to MinIO successfully. Buckets found: {[b.name for b in buckets]}")
        except Exception as e:
            raise RuntimeError(f"❌ Failed to connect to MinIO: {e}")

    @classmethod
    def get_minio_connection(cls) -> "MiniOConnection":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

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