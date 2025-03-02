# backend/services/service_cover_letter/src/service_layer/file_service.py
import uuid
import logging
from typing import List
from fastapi import UploadFile
from src.data_repositories.miniO_repository.CRUD_minio import MinioRepository
from src.data_models.minio_models import FileItem

class FileService:
    def __init__(self, repository: MinioRepository) -> None:
        self.repository: MinioRepository = repository
        self.logger = logging.getLogger(__name__)

    async def process_files(self, files: List[UploadFile]) -> List[FileItem]:
        file_items: List[FileItem] = []
        for file in files:
            file_extension = file.filename.split('.')[-1].lower()
            bucket_type = 'cover_letters' if file_extension in ['pdf', 'txt'] else 'images'

            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            content = await file.read()

            self.repository.upload_file(
                file_content=content,
                file_name=unique_filename,
                content_type=file.content_type,
                bucket_type=bucket_type,
                metadata={"original_name": file.filename}
            )

            file_items.append(FileItem(
                file_name=unique_filename,
                original_file_name=file.filename,
                size=len(content),
                file_type=file_extension
            ))

        return file_items

    def delete_file(self, file_name: str, bucket_type: str) -> None:
        self.repository.delete_file(file_name, bucket_type)

    def list_files(self, bucket_type: str) -> List[FileItem]:
        raw_files = self.repository.list_files(bucket_type)
        return [
            FileItem(
                file_name=file["file_name"],
                original_file_name=file["original_name"],
                size=file["size"],
                file_type=""
            ) for file in raw_files
        ]

    def get_file_content(self, file_name: str, bucket_type: str) -> bytes:
        return self.repository.get_file(file_name, bucket_type)
