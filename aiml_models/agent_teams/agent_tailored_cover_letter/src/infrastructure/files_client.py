# aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/files_client.py
from typing import Dict, Optional
from io import BytesIO
from minio import Minio
from minio.error import S3Error

from src.config.config_low_level import MinioConnection


class MinioFileClient:
    """
    Purpose:
        Provides access to raw files stored in different MinIO buckets.

    Capabilities:
        - Fetch file content as bytes.
        - Organize buckets by functional role: CVs, Cover Letters, Images.
        - Does NOT handle decoding or file content interpretation.

    Reasoning:
        Keeps file retrieval isolated from domain-specific logic like parsing or classification.
    """

    def __init__(self, connection: MinioConnection) -> None:
        self.client: Minio = connection.client
        self.connection: MinioConnection = connection

        self.buckets: Dict[str, str] = {
            "cover_letters": "uploaded-cover-letters",
            "cv": "uploaded-cvs",
            "images": "images"
        }

    def fetch_file(self, bucket_key: str, filename: str) -> Optional[BytesIO]:
        """
        Downloads a file as bytes from the corresponding MinIO bucket.
        
        Args:
            bucket_key (str): One of the keys from `self.buckets`.
            filename (str): The name of the file to retrieve.
        
        Returns:
            Optional[BytesIO]: Stream of file content, or None if not found.
        """
        if bucket_key not in self.buckets:
            raise ValueError(f"Invalid bucket key '{bucket_key}'. Valid options: {list(self.buckets.keys())}")

        bucket_name: str = self.buckets[bucket_key]

        try:
            file_response = self.client.get_object(bucket_name, filename)
            return BytesIO(file_response.read())  # Return file stream for parsing later
        except S3Error as e:
            print(f"MinIO Fetch Error: '{filename}' from '{bucket_name}': {e}")
            return None

