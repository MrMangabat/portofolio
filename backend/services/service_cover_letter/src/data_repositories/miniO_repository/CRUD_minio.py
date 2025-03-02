# backend/services/service_cover_letter/src/data_repositories/miniO_repository/CRUD_minio.py
from typing import Dict, List, Optional
from src.config.config_low_level import MiniOConnection
from minio.error import S3Error
from io import BytesIO
import logging

class MinioRepository:
    def __init__(self, connection: MiniOConnection) -> None:
        self.client = connection.client
        self.connection = connection

        self.buckets = {
            "cover_letters": "uploaded-cover-letters",
            "images": "images"
        }

        self.logger = logging.getLogger(__name__)
        self._ensure_buckets_exist()

    def _ensure_buckets_exist(self) -> None:
        for bucket_name in self.buckets.values():
            self.logger.info(f"Checking bucket existence: {bucket_name}")
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                self.logger.info(f"Created bucket '{bucket_name}'")

    def _get_virtual_host_url(self, bucket_name: str) -> str:
        return f"http://{bucket_name}.{self.connection.minio_host}:{self.connection.minio_port}"

    def get_file_url(self, file_name: str, bucket_type: str) -> str:
        bucket_name = self.buckets.get(bucket_type)
        if not bucket_name:
            raise ValueError(f"Invalid bucket type: {bucket_type}")

        bucket_url = self._get_virtual_host_url(bucket_name)
        return f"{bucket_url}/{file_name}"

    def upload_file(self, file_content: bytes, file_name: str, content_type: str, bucket_type: str, metadata: Optional[dict] = None) -> None:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            self.logger.info(f"Uploading '{file_name}' to '{bucket_name}'")

            self.client.put_object(
                bucket_name,
                file_name,
                data=BytesIO(file_content),
                length=len(file_content),
                content_type=content_type,
                metadata=metadata or {}
            )

            file_url = self.get_file_url(file_name, bucket_type)
            self.logger.info(f"Successfully uploaded '{file_name}' — Access it at: {file_url}")
        except S3Error as e:
            self.logger.error(f"S3Error: {e}")
            raise

    def delete_file(self, file_name: str, bucket_type: str) -> None:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            self.client.remove_object(bucket_name, file_name)
            self.logger.info(f"🗑️ Deleted file '{file_name}' from bucket '{bucket_name}'.")
        except S3Error as e:
            self.logger.error(f"Failed to delete file '{file_name}': {e}")
            raise

    def list_files(self, bucket_type: str) -> List[Dict[str, str]]:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            objects = self.client.list_objects(bucket_name)
            file_list = []
            for obj in objects:
                stat = self.client.stat_object(bucket_name, obj.object_name)
                original_name = stat.metadata.get('X-Amz-Meta-Original_name', obj.object_name)
                file_list.append({
                    "file_name": obj.object_name,
                    "size": stat.size,
                    "original_name": original_name
                })
            return file_list
        except S3Error as e:
            self.logger.error(f"Failed to list files: {e}")
            raise