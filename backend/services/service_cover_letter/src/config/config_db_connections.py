# /home/mangabat/projects/portofolio/backend/services/service_cover_letter/src/config/config_db_connections.py
"""
This module handles all infrastructure connections for the 'cover_letter' service.
It is intentionally placed within the service boundary to prevent cross-service coupling.
Configuration is static and changes only if the infrastructure itself changes.

!!!!!!!!
pydantic base settings must be used in the future
!!!!!!!!
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from minio import Minio
from typing import Optional
from qdrant_client import QdrantClient, models

from src.config.service_settings import CoverLetterSettings

settings_from_env = CoverLetterSettings()
### stadardize this connection pattern. ensure i can work cross notebook and system
class PostgressConnection:
    Base = declarative_base()
    engine = None
    SessionLocal = None

    @classmethod
    def initialize(cls) -> None:
        """
        Lazy initializer for engine and SessionLocal.
        Only called explicitly in FastAPI startup or actual usage contexts.
        """
        if cls.engine is None:
            try:
                cls.engine = create_engine(settings_from_env.POSTGRES_URL)
                cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
            except Exception as e:
                raise RuntimeError(f"❌ Failed to initialize Postgres connection: {e}")

    @staticmethod
    def get_db():
        if PostgressConnection.SessionLocal is None:
            raise RuntimeError("PostgressConnection was never initialized. Call initialize() first.")
        db = PostgressConnection.SessionLocal()
        try:
            yield db
        finally:
            db.close()



class MiniOConnection:
    _instance: Optional["MiniOConnection"] = None

    def __init__(self) -> None:
        print(f"🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑 Connecting to MinIO with:")
        print(f"   Host: {settings_from_env.MINIO_HOST}")
        print(f"   Port: {settings_from_env.MINIO_PORT}")
        print(f"   Access Key: {settings_from_env.MINIO_ACCESS_KEY}")
        print(f"   Secret Key: {settings_from_env.MINIO_SECRET_KEY}")

        self.client: Minio = Minio(
            endpoint=f"172.31.0.4:{settings_from_env.MINIO_PORT}",
            access_key=settings_from_env.MINIO_ACCESS_KEY,
            secret_key=settings_from_env.MINIO_SECRET_KEY,
            secure=False,
            region=None
        )
        self._validate_connection()

        

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
        self.url: str = settings_from_env.QDRANT_URL
        self.default_collection: str = "embedded_cover_letters"

        self.client = QdrantClient(url=self.url)

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