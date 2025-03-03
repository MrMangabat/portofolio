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

        self.buckets: Dict[str, str] = {
            "cover_letters": "uploaded-cover-letters",
            "images": "images"
        }

        self.logger = logging.getLogger(__name__)
        self._ensure_buckets_exist()

    def _ensure_buckets_exist(self) -> None:
        for bucket_name in self.buckets.values():
            print(f"🟡 Checking bucket: {bucket_name}")
            exists = self.client.bucket_exists(bucket_name)

            if not exists:
                print(f"⚠️ Bucket {bucket_name} not found — creating it.")
                self.client.make_bucket(bucket_name)
                print(f"✅ Created bucket: {bucket_name}")
            else:
                print(f"✅ Bucket {bucket_name} already exists.")

    def upload_file(self, file_content: bytes, file_name: str, content_type: str, bucket_type: str, metadata: Optional[dict] = None) -> None:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")
            
            import urllib.parse
            safe_file_name = urllib.parse.quote(file_name, safe='')

            metadata = metadata or {}

            print(f"📤 Uploading to MinIO: {bucket_name}/{safe_file_name}")
            print(f"   Metadata: {metadata}")
            print(f"   Content-Type: {content_type}")
            self.client.put_object(
                bucket_name,
                file_name,
                data=BytesIO(file_content),
                length=len(file_content),
                content_type=content_type,
                metadata=metadata
            )
            print(f"✅ Uploaded '{file_name}' to bucket '{bucket_name}'")
        except S3Error as e:
            self.logger.error(f"S3Error during upload: {e}")
            raise

    def delete_file(self, file_name: str, bucket_type: str) -> None:
        try:
            bucket_name = self.buckets.get(bucket_type)
            if not bucket_name:
                raise ValueError(f"Invalid bucket type: {bucket_type}")

            self.client.remove_object(bucket_name, file_name)
            print(f"✅ Deleted file '{file_name}' from bucket '{bucket_name}'")
        except S3Error as e:
            self.logger.error(f"S3Error during delete: {e}")
            raise

    def list_files(self, bucket_type: str) -> List[Dict[str, str]]:
        bucket_name = self.buckets.get(bucket_type)
        if not bucket_name:
            raise ValueError(f"Invalid bucket type: {bucket_type}")
        
        file_list = []
        for obj in self.client.list_objects(bucket_name):
            stat = self.client.stat_object(bucket_name, obj.object_name)
            original_name = stat.metadata.get("x-amz-meta-original-name", obj.object_name)
            file_list.append({
                "file_name": obj.object_name,
                "size": stat.size,
                "original_name": original_name  # This now works
            })
            print(f"📦 Metadata for {obj.object_name}: {stat.metadata}")

        return file_list

