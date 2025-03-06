# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/config/config_low_level.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from minio import Minio
from qdrant_client import QdrantClient
from src.config.config_top_level import TopLevelConfig

class PostgresConnection:
    config = TopLevelConfig.load_from_env()
    engine = create_engine(
        f"postgresql://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class MinioConnection:
    config = TopLevelConfig.load_from_env()
    client = Minio(
        endpoint=f"{config.minio_host}:{config.minio_port}",
        access_key=config.minio_access_key,
        secret_key=config.minio_secret_key,
        secure=False
    )

class QdrantConnection:
    config = TopLevelConfig.load_from_env()
    client = QdrantClient(url=config.qdrant_url)
