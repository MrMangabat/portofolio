# backend/services/service_cover_letter/src/routes/routes_files.py
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.config.config_db_connections import MiniOConnection, QdrantConnection
from src.data_models.minio_models import FileItem
from src.data_models.kafka_models.producers.file_upload_event import FileUploadedEvent
from src.service_layer.file_service import FileService
from src.data_repositories.miniO_repository.CRUD_minio import MinioRepository
from src.data_repositories.qdrant_repository.CRUD_qdrant import QdrantCoverLetterRepository
from src.event_broker.event_producers.file_uploaded_producer import FileUploadedProducer
from io import BytesIO
import uuid
from src.service_layer.embbing_file_service import FileEmbeddingService
from src.service_layer.text_extractor import FileTextExtractor


router = APIRouter()

def get_file_service() -> FileService:
    minio_connection = MiniOConnection.get_minio_connection()
    repository = MinioRepository(minio_connection)
    return FileService(repository)

@router.post("/upload", response_model=List[FileItem])
async def upload_files(
    files: List[UploadFile] = File(...),
    file_service: FileService = Depends(get_file_service)
) -> List[FileItem]:
    """
    Uploads files, saves them to MinIO, extracts text, embeds them in Qdrant (no Kafka).
    """
    try:
        logging.info(f"{__file__} | 📥 Received files: {[file.filename for file in files]}")

        minio_responses: List[FileItem] = await file_service.process_files(files)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        qdrant_connection = QdrantConnection()

        qdrant_repo = QdrantCoverLetterRepository(qdrant_connection)

        for file_item, raw_file in zip(minio_responses, files):
            logging.info(f"{__file__} | 🔍 Starting embedding for file_id={file_item.file_id}")

            await raw_file.seek(0)  # rewind to read again
            byte_stream: BytesIO = BytesIO(await raw_file.read())

            extracted_text = FileTextExtractor.extract_text(byte_stream, file_item.original_file_name)

            if not extracted_text:
                logging.warning(f"{__file__} | ⚠️ No text extracted for {file_item.original_file_name}")
                continue

            qdrant_repo.upsert_file_embedding(
                file_id=file_item.file_id,
                text=extracted_text,
                metadata={
                    "file_id": file_item.file_id,
                    "file_name": file_item.file_name,
                    "original_file_name": file_item.original_file_name,
                    "bucket": file_item.bucket,
                    "file_type": file_item.file_type
                }
            )
            logging.info(f"{__file__} | ✅ Embedded file_id={file_item.file_id}")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        return minio_responses

    except Exception as e:
        logging.error(f"{__file__} | ❌ Error in upload_files: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="File upload and embedding failed.")

@router.get("/{bucket}", response_model=List[FileItem])
def get_files(bucket: str, file_service: FileService = Depends(get_file_service)) -> List[FileItem]:
    logging.info(f"{__file__} | ⚙️ Received GET for bucket={bucket}")
    try:
        return file_service.list_files(bucket)
    except Exception as e:
        logging.error(f"{__file__} | ❌ Failed to list bucket {bucket}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch files")


@router.delete("/{bucket}/{file_name}")
def delete_file(
    bucket: str,
    file_name: str,
    file_service: FileService = Depends(get_file_service)
) -> List[FileItem]:
    """
    Deletes a file from MinIO and returns the updated file list.
    """
    logging.info(f"{__file__} | 🗑 DELETE file request: {file_name} from bucket={bucket}")
    try:
        return file_service.delete_file_minio(file_name, bucket)
    except Exception as e:
        logging.error(f"{__file__} | ❌ Failed to delete file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete file")


####
'''
Date: 2025-05-11
Discussion Topic: Bypassing Kafka for Immediate Embedding after Upload
Final Decision: Temporarily call embedding logic directly inside the FastAPI upload route
Rationale:
    - Kafka is not stable yet, and embedding logic must be validated.
    - MasterGraphFlow requires Qdrant embeddings to function.
    - Once Kafka producer-consumer flow is stable, embedding call will be moved back into the consumer logic.

'''
# async def upload_files(
#     files: List[UploadFile] = File(...),
#     file_service: FileService = Depends(get_file_service),
#     user_id: str = "placeholder-user"  # Replace with actual user_id from session or auth
# ) -> List[FileItem]:
#     try:
#         logging.info(f"Received files: {[file.filename for file in files]}")
#         minio_responses = await file_service.process_files(files)

#         # Initialize Kafka producer
#         producer = FileUploadedProducer()

#         # Create the FileUploadedEvent once per user/session
#         kafka_event = FileUploadedEvent(
#             user_id=user_id,  # Set the user_id once
#             upload_method="web",
#             bucket="",  # To be set per file
#             filename="",  # To be set per file
#             content_type="",  # To be set per file
#             file_id=""  # To be set per file
#         )

#         # Publish Kafka event for each uploaded file
#         for _, saved_file in zip(files, minio_responses):
#             # Update the event for each file
#             kafka_event.file_id = saved_file.file_id
#             kafka_event.filename = saved_file.file_name
#             kafka_event.bucket = saved_file.bucket
#             kafka_event.content_type = saved_file.file_type

#             # Pass the same event instance to Kafka producer
#             producer.publish_file_uploaded(kafka_event)

#         return minio_responses

#     except Exception as e:
#         logging.error(f"Error processing files: {e}")
        # raise HTTPException(status_code=500, detail=str(e))