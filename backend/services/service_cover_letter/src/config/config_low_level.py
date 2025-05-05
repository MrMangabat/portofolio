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
        minio_ip = self._read_minio_ip()
        print(f"🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑🔑 Connecting to MinIO with:")
        print(f"   Host: {minio_ip}")
        print(f"   Port: {Config.MINIO_PORT}")
        print(f"   Access Key: {Config.MINIO_ACCESS_KEY}")
        print(f"   Secret Key: {Config.MINIO_SECRET_KEY}")

        self.client: Minio = Minio(
            endpoint=f"{minio_ip}:{Config.MINIO_PORT}",
            access_key=Config.MINIO_ACCESS_KEY,
            secret_key=Config.MINIO_SECRET_KEY,
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

