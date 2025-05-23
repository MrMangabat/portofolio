# backend/services/service_cover_letter/src/routes/routes_files.py
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.config.config_low_level import MiniOConnection
from src.data_models.minio_models import FileItem
from src.service_layer.file_service import FileService
from src.data_repositories.miniO_repository.CRUD_minio import MinioRepository
from src.event_broker.event_producers.file_uploaded_producer import FileUploadedProducer
from src.data_models.kafka_models.producers.file_upload_event import FileUploadedEvent
from io import BytesIO
import uuid



router = APIRouter()

def get_file_service() -> FileService:
    minio_connection = MiniOConnection.get_minio_connection()
    repository = MinioRepository(minio_connection)
    return FileService(repository)

async def upload_files(
    files: List[UploadFile] = File(...),
    file_service: FileService = Depends(get_file_service),
    user_id: str = "placeholder-user"  # Replace with actual user_id from session or auth
) -> List[FileItem]:
    try:
        logging.info(f"Received files: {[file.filename for file in files]}")
        minio_responses = await file_service.process_files(files)

        # Initialize Kafka producer
        producer = FileUploadedProducer()

        # Create the FileUploadedEvent once per user/session
        kafka_event = FileUploadedEvent(
            user_id=user_id,  # Set the user_id once
            upload_method="web",
            bucket="",  # To be set per file
            filename="",  # To be set per file
            content_type="",  # To be set per file
            file_id=""  # To be set per file
        )

        # Publish Kafka event for each uploaded file
        for _, saved_file in zip(files, minio_responses):
            # Update the event for each file
            kafka_event.file_id = saved_file.file_id
            kafka_event.filename = saved_file.file_name
            kafka_event.bucket = saved_file.bucket
            kafka_event.content_type = saved_file.file_type

            # Pass the same event instance to Kafka producer
            producer.publish_file_uploaded(kafka_event)

        return minio_responses

    except Exception as e:
        logging.error(f"Error processing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{bucket_type}/{file_name}")
def delete_file(
    bucket_type: str,
    file_name: str,
    file_service: FileService = Depends(get_file_service)
) -> dict:
    try:
        file_service.delete_file(file_name, bucket_type)
        return {"detail": "File deleted successfully"}
    except Exception as e:
        logging.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{bucket_type}", response_model=List[FileItem])
def list_files_from_bucket(bucket_type: str, file_service: FileService = Depends(get_file_service)) -> List[FileItem]:
    return file_service.list_files(bucket_type)
