# backend/services/service_cover_letter/src/service_layer/file_service.py
from uuid import uuid4
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
        """
        Saves uploaded files to MinIO and returns metadata.

        Purpose:
            - Generates unique file_id and file_name.
            - Selects appropriate bucket based on file type.
            - Uploads the file content to MinIO with metadata.
            - Returns a list of FileItem containing full traceable info.

        Capabilities:
            - Handles multiple file types (e.g., PDF, TXT, images).
            - Generates UUID-based identifiers.
            - Assigns MinIO-compatible metadata.

        Returns:
            List[FileItem]: List of structured file metadata for each upload.
        """
        file_items: List[FileItem] = []

        for file in files:
            file_extension: str = file.filename.split('.')[-1].lower()
            bucket_type: str = 'uploaded-cover-letters' if file_extension in ['pdf', 'txt'] else 'images'

            file_id: str = str(uuid4())
            unique_filename: str = f"{file_id}.{file_extension}"

            # Read raw file content
            content: bytes = await file.read()

            # Upload to MinIO with content type and original name as metadata
            self.repository.upload_file(
                file_content=content,
                file_name=unique_filename,
                content_type=file.content_type,
                bucket_type=bucket_type,
                metadata={"x-amz-meta-original-name": file.filename}
            )

            # Construct a traceable file item
            file_items.append(FileItem(
                file_id=file_id,
                file_name=unique_filename,
                original_file_name=file.filename,
                bucket=bucket_type,
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
                original_file_name=file["original_name"],  # Matches CRUD_minio
                size=file["size"],
                file_type=""  # Can add extension parsing if needed
            )
            for file in raw_files
        ]

    def get_file_content(self, file_name: str, bucket_type: str) -> bytes:
        pass
