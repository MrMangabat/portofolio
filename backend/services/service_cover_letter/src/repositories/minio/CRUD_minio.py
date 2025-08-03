# backend/services/service_cover_letter/src/data_repositories/miniO_repository/CRUD_minio.py
from typing import Dict, List, Optional
from src.config.config_db_connections import MiniOConnection
from minio.error import S3Error
from io import BytesIO
import logging

class MinioRepository:
    def __init__(self, connection: MiniOConnection) -> None:
        self.client = connection.client
        self.connection = connection

        self.buckets: Dict[str, str] = {
            "cover-letters": "uploaded-cover-letters",
            "cv": "uploaded-cvs",
            "images": "images"
        }

        self.logger = logging.getLogger(__name__)
        self._ensure_buckets_exist()

    def _ensure_buckets_exist(self) -> None:
        for bucket_name in self.buckets.values():
            print(f"Checking bucket: {bucket_name}")
            exists = self.client.bucket_exists(bucket_name)

            if not exists:
                print(f"Bucket {bucket_name} not found — creating it.")
                self.client.make_bucket(bucket_name)
                print(f"Created bucket: {bucket_name}")
            else:
                print(f"Bucket {bucket_name} already exists.")

    def upload_file(self, file_content: bytes, file_name: str, content_type: str, bucket_type: str, metadata: Optional[dict] = None) -> None:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")
            
            import urllib.parse
            safe_file_name = urllib.parse.quote(file_name, safe='')

            metadata = metadata or {}

            print(f"Uploading to MinIO: {bucket_name}/{safe_file_name}")
            print(f"Metadata: {metadata}")
            print(f"Content-Type: {content_type}")
            self.client.put_object(
                bucket_name,
                file_name,
                data=BytesIO(file_content),
                length=len(file_content),
                content_type=content_type,
                metadata=metadata
            )
            
            print(f"Uploaded '{file_name}' to bucket '{bucket_name}'")
        except S3Error as e:
            self.logger.error(f"S3Error during upload: {e}")
            raise

    def delete_file(self, file_name: str, bucket_type: str) -> None:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")
            logging.info(f"{__file__} | 🗑 Attempting delete: file_name={file_name}, bucket_type={bucket_type}")
            logging.info(f"{__file__} | 🗑 Attempting delete: file_name={file_name}, bucket_type={bucket_type}")

            self.client.remove_object(bucket_name, file_name)
            print(f"Deleted file '{file_name}' from bucket '{bucket_name}'")
        except S3Error as e:
            self.logger.error(f"S3Error during delete: {e}")
            raise

    def list_files(self, bucket_type: str) -> List[Dict[str, str]]:
        # Resolve the actual MinIO bucket name
        bucket_name = self.buckets.get(bucket_type, bucket_type)
        if bucket_name not in self.buckets.values():
            raise ValueError(f"Invalid bucket type: {bucket_type}")
        
        result: List[Dict[str, str]] = []

        try:
            objects = self.client.list_objects(bucket_name, recursive=True)

            for obj in objects:
                object_name: str = obj.object_name

                # Fetch metadata headers for the object
                metadata = self.client.stat_object(bucket_name, object_name).metadata

                result.append({
                    "file_name": object_name,  # ✅ Required for downstream code
                    "original_name": metadata.get("x-amz-meta-original-name", ""),
                    "size": obj.size,
                    "file_type": object_name.split(".")[-1]
                })

        except Exception as e:
            logging.error(f"{__file__} | ❌ Error listing files from MinIO bucket {bucket_type}: {e}")
            raise

        return result
