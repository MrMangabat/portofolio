# backend/services/service_cover_letter/src/service_layer/file_service.py
from uuid import uuid4
import logging
from typing import List, Dict, Any
from fastapi import UploadFile
from src.data_repositories.miniO_repository.CRUD_minio import MinioRepository
from src.data_models.minio_models import FileItem
from src.data_models.kafka_models.producers.file_upload_event import FileUploadedEvent
from src.event_broker.event_producers.file_uploaded_producer import FileUploadedProducer
class FileService:
    def __init__(self, repository: MinioRepository) -> None:
        self.repository: MinioRepository = repository
        self.logger = logging.getLogger(__name__)
        self.kafka_producer = FileUploadedProducer()  # Initialized once per service instance
        logging.info(f"INSIDE: file_service.py | FileService initialized with repository: {repository}")

    async def process_files(self, files: List[UploadFile]) -> List[FileItem]:
        """
        Saves uploaded files to MinIO and returns metadata.

        Args:
            files (List[UploadFile]): List of incoming files from API request.

        Returns:
            List[FileItem]: Structured metadata about the uploaded files.
        """
        file_items: List[FileItem] = []

        for file in files:
            file_extension: str = file.filename.split('.')[-1].lower()
            bucket_type: str = 'cover-letters' if file_extension in ['pdf', 'txt'] else 'images'

            file_id: str = str(uuid4())
            unique_filename: str = f"{file_id}.{file_extension}"

            try:
                # Read raw file content
                content: bytes = await file.read()

                # Upload to MinIO with original filename as metadata
                self.repository.upload_file(
                    file_content=content,
                    file_name=unique_filename,
                    content_type=file.content_type,
                    bucket_type=bucket_type,
                    metadata={"x-amz-meta-original-name": file.filename}
                )

                # Create and append file metadata model
                file_item = FileItem(
                    file_id=file_id,
                    file_name=unique_filename,
                    original_file_name=file.filename,
                    bucket=bucket_type,
                    size=len(content),
                    file_type=file_extension
                )
                file_items.append(file_item)

                # ✅ Trigger Kafka file_uploaded event
                kafka_event = FileUploadedEvent(
                    file_id=file_id,
                    user_id="placeholder-user",  # TODO: Replace with actual user ID from session/auth
                    bucket=bucket_type,
                    filename=unique_filename,
                    content_type=file.content_type,
                    upload_method="web"
                )

                success = self.kafka_producer.publish_file_uploaded(kafka_event)
                if not success:
                    self.logger.warning(f"{__file__} | ⚠️ Kafka publish failed for file_id={file_id}")

            except Exception as e:
                self.logger.error(f"{__file__} | ❌ Error processing file {file.filename}: {e}")
                continue

        return file_items

    def delete_file(self, file_name: str, bucket_type: str) -> None:
        self.repository.delete_file(file_name, bucket_type)

        try:
            # Retrieve raw file metadata from the repository layer
            raw_files: List[Dict[str, Any]] = self.repository.list_files(bucket_type)

            # Return a list of validated FileItem objects
            return [
                FileItem(
                    file_id=file["file_name"],  # Assuming this is the UUID-based ID
                    file_name=file["file_name"],
                    original_file_name=file.get("original_name", ""),
                    size=file["size"],
                    file_type=file.get("file_type", ""),
                    bucket=bucket_type
                )
                for file in raw_files
            ]
        except Exception as e:
            logging.error(f"{__file__} | ❌ Error in list_files for bucket '{bucket_type}': {e}")
            raise

    def get_file_content(self, file_name: str, bucket_type: str) -> bytes:
        pass

    
    def list_files(self, bucket_type: str) -> List[FileItem]:
        """
        Lists files from the specified bucket type.

        Args:
            bucket_type (str): The type of bucket to list files from.

        Returns:
            List[FileItem]: A list of file metadata objects.
        """
        try:
            logging.info(f"INSIDE: fileservice.py | list_files |")
            # Retrieve raw file metadata from the repository layer
            raw_files: List[Dict[str, Any]] = self.repository.list_files(bucket_type)

            # Return a list of validated FileItem objects
            return [
                FileItem(
                    file_id=file["file_name"],  # Assuming this is the UUID-based ID
                    file_name=file["file_name"],
                    original_file_name=file.get("original_name", ""),
                    size=file["size"],
                    file_type=file.get("file_type", ""),
                    bucket=bucket_type
                )
                for file in raw_files
            ]
        except Exception as e:
            logging.error(f"{__file__} | ❌ Error in list_files for bucket '{bucket_type}': {e}")
            raise

    def get_file_content(self, file_name: str, bucket_type: str) -> bytes:
        # Placeholder for file content retrieval (not yet implemented)
        pass