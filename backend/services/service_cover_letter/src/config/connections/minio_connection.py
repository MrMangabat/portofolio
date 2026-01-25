# backend/services/service_cover_letter/src/config/connections/minio_connection.py
"""
MinIO connection handler for the cover_letter service.
"""

from minio import Minio
from typing import Optional

from src.config.settings import CoverLetterSettings

settings_from_env = CoverLetterSettings()


class MinioConnection:
    _instance: Optional["MinioConnection"] = None

    def __init__(self) -> None:
        print(f"Connecting to MinIO with:")
        print(f"   Host: {settings_from_env.MINIO_HOST}")
        print(f"   Port: {settings_from_env.MINIO_PORT}")
        print(f"   Access Key: {settings_from_env.MINIO_ACCESS_KEY}")
        print(f"   Secret Key: {settings_from_env.MINIO_SECRET_KEY}")

        self.client: Minio = Minio(
            endpoint=f"172.17.0.1:{settings_from_env.MINIO_PORT}",
            access_key=settings_from_env.MINIO_ACCESS_KEY,
            secret_key=settings_from_env.MINIO_SECRET_KEY,
            secure=False,
            region=None
        )
        self._validate_connection()

    def _validate_connection(self) -> None:
        try:
            buckets = self.client.list_buckets()
            print(f"Connected to MinIO successfully. Buckets found: {[b.name for b in buckets]}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to MinIO: {e}")

    @classmethod
    def get_minio_connection(cls) -> "MinioConnection":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
