# backend/services/service_cover_letter/src/routes/routes_files.py
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.config.config_db_connections import MiniOConnection, QdrantConnection
from src.models.external_services.minio.minio_models import FileItem
# Kafka imports removed - not functional yet
from src.core_business_logic.file_service import FileService
from src.repositories.minio.CRUD_minio import MinioRepository
from src.repositories.postgresql.file_metadata_repository import FileMetadataRepository
from src.repositories.qdrant.CRUD_qdrant import QdrantCoverLetterRepository
# from src.event_broker.event_producers.file_uploaded_producer import FileUploadedProducer
from io import BytesIO
import uuid
from src.core_business_logic.embbing_file_service import FileEmbeddingService
from src.utils.text_extraction.text_extractor import FileTextExtractor
from fastapi import Form
from typing import Optional


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
        logging.info("XXXXXXXXXXXXXXXXXXXXX UPLOAD ROUTE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXX UPLOAD ROUTE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


        qdrant_connection = QdrantConnection()

        qdrant_repo = QdrantCoverLetterRepository(qdrant_connection)

        for file_item, raw_file in zip(minio_responses, files):
            logging.info(f"{__file__} | 🔍 Starting embedding for file_id={file_item.file_id}")

            await raw_file.seek(0)  # rewind to read again
            byte_stream: BytesIO = BytesIO(await raw_file.read())

            extracted_text = FileTextExtractor.extract_text(byte_stream, file_item.original_file_name)

            print(f"{__file__} | 📄 Extracted text for {file_item.original_file_name}: {extracted_text}...")

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

@router.get("/jobtypes")
def get_active_jobtypes():
    """
    Get active jobtypes for dropdown population - implements TDD Test Behavior 4.
    
    WHY: Provides jobtype vocabulary validated by TDD active state filtering tests
    CONTRIBUTION: Enables frontend metadata collection with standardized job categories
    HOW: Uses FileMetadataRepository.get_active_jobtypes with proper active filtering
    """
    try:
        metadata_repo = FileMetadataRepository()
        jobtypes = metadata_repo.get_active_jobtypes()
        
        return {
            "data": [
                {
                    "id": jt.id,
                    "name": jt.name,
                    "category": jt.category,
                    "description": jt.description
                }
                for jt in jobtypes
            ]
        }
        
    except Exception as e:
        logging.error(f"{__file__} | ❌ Failed to fetch jobtypes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch jobtypes")


@router.get("/industries")
def get_active_industries():
    """
    Get active industries for multi-select population.
    
    WHY: Provides industry vocabulary for template and CV categorization
    CONTRIBUTION: Enables industry-based filtering and market analysis capabilities
    HOW: Uses FileMetadataRepository.get_active_industries with proper filtering
    """
    try:
        metadata_repo = FileMetadataRepository()
        industries = metadata_repo.get_active_industries()
        
        return {
            "data": [
                {
                    "id": ind.id,
                    "name": ind.name,
                    "sector": ind.sector,
                    "description": ind.description
                }
                for ind in industries
            ]
        }
        
    except Exception as e:
        logging.error(f"{__file__} | ❌ Failed to fetch industries: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch industries")

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


# TDD Integration: Enhanced metadata endpoints
@router.post("/upload-with-metadata")
async def upload_files_with_metadata(
    files: List[UploadFile] = File(...),
    file_type: str = Form(...),
    language: str = Form(...), 
    jobtype: Optional[str] = Form(None),
    industry_sectors: Optional[str] = Form(None),  # JSON string
    template_subtype: Optional[str] = Form("cover_letter"),
    company_size_target: Optional[str] = Form("any"),
    experience_years: Optional[int] = Form(None),
    primary_roles: Optional[str] = Form(None),  # JSON string
    is_current_cv: bool = Form(False),
    file_service: FileService = Depends(get_file_service)
):
    """
    Enhanced file upload with comprehensive metadata collection.
    
    WHY: Implements TDD-validated enhanced file workflow with structured metadata
    CONTRIBUTION: Replaces simple upload with comprehensive categorization system
    HOW: Uses FileService.process_files_with_metadata with proper validation
    """
    import json
    
    try:
        # Parse JSON strings
        industry_list = json.loads(industry_sectors) if industry_sectors else []
        roles_list = json.loads(primary_roles) if primary_roles else []
        
        logging.info(f"{__file__} | 📤 Enhanced upload: {len(files)} files, type={file_type}, language={language}")
        
        result = await file_service.process_files_with_metadata(
            files=files,
            file_type=file_type,
            language=language,
            jobtype=jobtype,
            industry_sectors=industry_list,
            template_subtype=template_subtype,
            company_size_target=company_size_target,
            experience_years=experience_years,
            primary_roles=roles_list,
            is_current_cv=is_current_cv
        )
        
        return {"message": "Files processed successfully", "files": result}
        
    except Exception as e:
        logging.error(f"{__file__} | ❌ Enhanced upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")




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