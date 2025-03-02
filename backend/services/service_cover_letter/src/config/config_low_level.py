# backend/services/service_cover_letter/src/config/config_low_level.py

"""
This module handles all infrastructure connections for the 'cover_letter' service.
It is intentionally placed within the service boundary to prevent cross-service coupling.
Configuration is static and changes only if the infrastructure itself changes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.config_top_level import Config
from minio import Minio
from typing import Optional

class PostgressConnection:
    Base = declarative_base()
    engine = create_engine(Config.POSTGRES_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def get_db():
        db = PostgressConnection.SessionLocal()
        try:
            yield db
        finally:
            db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.config_top_level import Config
from minio import Minio
from typing import Optional

class PostgressConnection:
    Base = declarative_base()
    engine = create_engine(Config.POSTGRES_URL)
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
        self.minio_host = "minio"
        self.minio_port = "9000"
        self.client = Minio(
            endpoint=f"{self.minio_host}:{self.minio_port}",
            access_key=Config.MINIO_ACCESS_KEY,
            secret_key=Config.MINIO_SECRET_KEY,
            secure=False
        )

    @classmethod
    def get_minio_connection(cls) -> "MiniOConnection":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance