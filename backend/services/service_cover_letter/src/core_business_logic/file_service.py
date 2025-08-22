# backend/services/service_cover_letter/src/service_layer/file_service.py
from uuid import uuid4
import logging
from typing import List, Dict, Any
from fastapi import UploadFile
from src.repositories.minio.CRUD_minio import MinioRepository
from src.models.external_services.minio.minio_models import FileItem
from src.messaging_integrations.kafka.producers.file_upload_event import FileUploadedEvent
from src.messaging_integrations.kafka.file_uploaded_producer import FileUploadedProducer
class FileService:
    def __init__(self, repository: MinioRepository) -> None:
        self.repository: MinioRepository = repository
        self.logger = logging.getLogger(__name__)
        self.kafka_producer = FileUploadedProducer()  # Initialized once per service instance
        
        # Add PostgreSQL repository for enhanced metadata
        from src.repositories.postgresql.file_metadata_repository import FileMetadataRepository
        self.metadata_repo = FileMetadataRepository()
        
        logging.info(f"INSIDE: {__file__} | FileService initialized with repository: {repository}")
        logging

    async def process_files(self, files: List[UploadFile]) -> List[FileItem]:
        """
        Saves uploaded files to MinIO and returns metadata.

        Args:
            files (List[UploadFile]): List of incoming files from API request.

        Returns:
            List[FileItem]: Structured metadata about the uploaded files.
        """

        file_items: List[FileItem] = []
        logging.info(f"{__file__} | ✅ raw_files fetched: {files}")

        for file in files:
            file_extension: str = file.filename.split('.')[-1].lower()
            bucket_type: str = 'cover-letters' if file_extension in ['pdf', 'txt'] else 'images'

            file_id: str = str(uuid4())  # ✅ Correct: always a UUID string
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

                # ✅ Uncomment when Kafka event is reactivated
                # kafka_event = FileUploadedEvent(
                #     file_id=file_id,
                #     user_id="placeholder-user",
                #     bucket=bucket_type,
                #     filename=unique_filename,
                #     content_type=file.content_type,
                #     upload_method="web"
                # )
                # success = self.kafka_producer.publish_file_uploaded(kafka_event)
                # if not success:
                #     self.logger.warning(f"{__file__} | ⚠️ Kafka publish failed for file_id={file_id}")

            except Exception as e:
                self.logger.error(f"{__file__} | ❌ Error processing file {file.filename}: {e}")
                continue

        return file_items
    
    async def process_files_with_metadata(
        self, 
        files: List[UploadFile], 
        file_type: str,
        language: str,
        jobtype: str = None,
        industry_sectors: List[str] = None,
        template_subtype: str = "cover_letter",
        company_size_target: str = "any",
        experience_years: int = None,
        primary_roles: List[str] = None,
        is_current_cv: bool = False
    ) -> List[Dict]:
        """
        Enhanced file processing with PostgreSQL metadata storage.
        
        WHY: Implements the TDD-validated enhanced file workflow with structured metadata
        CONTRIBUTION: Replaces simple file upload with comprehensive metadata management
        HOW: Processes files through MinIO + PostgreSQL + Qdrant pipeline with proper error handling
        """
        from uuid import uuid4
        processed_files = []
        
        for file in files:
            file_extension = file.filename.split('.')[-1].lower()
            bucket_type = 'cover-letters' if file_extension in ['pdf', 'txt'] else 'cv' if file_type == 'cv' else 'images'
            
            file_id = str(uuid4())
            unique_filename = f"{file_id}.{file_extension}"
            
            try:
                # 1. Upload to MinIO (existing workflow)
                content = await file.read()
                self.repository.upload_file(
                    file_content=content,
                    file_name=unique_filename,
                    content_type=file.content_type,
                    bucket_type=bucket_type,
                    metadata={"x-amz-meta-original-name": file.filename}
                )
                
                # 2. Create PostgreSQL metadata record (NEW - TDD validated)
                file_metadata = self.metadata_repo.create_file_metadata(
                    filename=file.filename,
                    file_type=file_type,
                    language=language,
                    minio_bucket=bucket_type,
                    minio_filename=unique_filename,
                    original_content_type=file.content_type,
                    file_size=len(content)
                )
                
                # 3. Create type-specific metadata (TDD Test Behavior 2)
                if file_type == "template" and jobtype:
                    template_metadata = self.metadata_repo.create_template_metadata(
                        file_id=file_metadata.id,
                        jobtype=jobtype,
                        industry_sectors=industry_sectors or [],
                        template_subtype=template_subtype,
                        company_size_target=company_size_target
                    )
                elif file_type == "cv":
                    cv_metadata = self.metadata_repo.create_cv_metadata(
                        file_id=file_metadata.id,
                        primary_roles=primary_roles or [],
                        experience_years=experience_years,
                        is_current_cv=is_current_cv
                    )
                
                processed_files.append({
                    "file_id": str(file_metadata.id),
                    "filename": file.filename,
                    "file_type": file_type,
                    "language": language,
                    "minio_filename": unique_filename,
                    "bucket": bucket_type,
                    "jobtype": jobtype
                })
                
                logging.info(f"{__file__} | ✅ Enhanced file processing complete: {file.filename}")
                
            except Exception as e:
                logging.error(f"{__file__} | ❌ Enhanced file processing failed: {str(e)}")
                # Rollback: delete from MinIO if PostgreSQL fails
                try:
                    self.repository.delete_file(unique_filename, bucket_type)
                except:
                    pass
                raise ValueError(f"File processing failed: {str(e)}")
        
        return processed_files

    def delete_file_minio(self, file_name: str, bucket_type: str) -> None:
        self.repository.delete_file(file_name, bucket_type)

        try:
            raw_files: List[Dict[str, Any]] = self.repository.list_files(bucket_type)

            return [
                FileItem(
                    file_id=file["file_name"].split(".")[0],  # ✅ Extract UUID from filename
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
        """
        logging.info(f"{__file__} | 📂 Service method called: list_files(bucket_type={bucket_type})")

        try:
            raw_files: List[Dict[str, Any]] = self.repository.list_files(bucket_type)
            logging.info(f"{__file__} | 🔍 Raw files fetched: {raw_files}")

            file_items = [
                FileItem(
                    file_id=file["file_name"].split(".")[0],  # Extract UUID from filename
                    file_name=file["file_name"],
                    original_file_name=file.get("original_name", ""),
                    size=file["size"],
                    file_type=file.get("file_type", ""),
                    bucket=bucket_type
                )
                for file in raw_files
            ]

            logging.info(f"{__file__} | ✅ Converted to {len(file_items)} FileItem(s)")
            logging.info(f"FileItemObjct: {file_items}")
            print(f"{__file__} | :{(file_items)}")
            return file_items

        except Exception as e:
            logging.error(f"{__file__} | ❌ Error in list_files for bucket '{bucket_type}': {e}", exc_info=True)
            raise

    def get_file_content(self, file_name: str, bucket_type: str) -> bytes:
        # Placeholder for file content retrieval (not yet implemented)
        pass