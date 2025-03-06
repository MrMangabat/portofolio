# backend/jobapplication_feature/services/file_service.py

from typing import List
from fastapi import UploadFile
from core_configuration.database_connections import MinioConnection
from core_configuration.config import Config
from service_cover_letter.data_models.minio_models import FileItem
from minio.error import S3Error

from io import BytesIO
import uuid
import logging
import re

class MinioRepository:
    """Handles file storage and retrieval in MinIO."""

    def __init__(self, minio_connection: MinioConnection):
        self.client = minio_connection.client
        self.buckets = {
            "cover_letters": "uploaded-cover-letters",
            "images": "images"
        }
        self.logger = logging.getLogger(__name__)
        self._ensure_buckets_exist()

    def _ensure_buckets_exist(self):
        """Ensure that the buckets exist in MinIO."""
        for bucket_name in self.buckets.values():
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                self.logger.info(f"Created bucket '{bucket_name}' in MinIO.")

    def upload_file(self, file_content: bytes, file_name: str, content_type: str, bucket_type: str, metadata: dict = None):
        """Upload a file to the appropriate MinIO bucket."""
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            # Pass along the metadata
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=file_name,
                data=BytesIO(file_content),
                length=len(file_content),
                content_type=content_type,
                metadata=metadata  # <- Important: attach user-defined metadata
            )
            self.logger.info(f"Uploaded file '{file_name}' to bucket '{bucket_name}'.")

        except S3Error as e:
            self.logger.error(f"Failed to upload file '{file_name}': {e}")
            raise

    def get_file(self, file_name: str, bucket_type: str) -> bytes:
        """Retrieve a file from the appropriate MinIO bucket."""
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            response = self.client.get_object(bucket_name, file_name)
            data = response.read()
            self.logger.info(f"Retrieved file '{file_name}' from bucket '{bucket_name}'.")
            return data
        except S3Error as e:
            self.logger.error(f"Failed to retrieve file '{file_name}': {e}")
            raise

    def delete_file(self, file_name: str, bucket_type: str):
        """Delete a file from the appropriate MinIO bucket."""
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            self.client.remove_object(bucket_name, file_name)
            self.logger.info(f"Deleted file '{file_name}' from bucket '{bucket_name}'.")
        except S3Error as e:
            self.logger.error(f"Failed to delete file '{file_name}': {e}")
            raise

    def list_files(self, bucket_type: str) -> list[dict]:
        """List all files in the specified bucket, including their user-defined metadata."""
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            objects = self.client.list_objects(bucket_name)
            file_list = []
            for obj in objects:
                # For each object, get metadata so we can retrieve the original file name
                stat = self.client.stat_object(bucket_name, obj.object_name)

                # User-defined metadata come back as e.g. X-Amz-Meta-Original_name
                original_name = stat.metadata.get('X-Amz-Meta-Original_name', obj.object_name)
                file_size = stat.size

                file_list.append({
                    "file_name": obj.object_name,       # The UUID-based name
                    "size": file_size,
                    "original_name": original_name      # The original file name from metadata
                })

            self.logger.info(f"Listed files in bucket '{bucket_name}'.")
            return file_list
        except S3Error as e:
            self.logger.error(f"Failed to list files: {e}")
            raise