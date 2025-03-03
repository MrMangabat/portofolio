# backend/services/service_cover_letter/src/routes.py
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import subprocess

# Config
from src.config.config_low_level import PostgressConnection, MiniOConnection

# Data Models
from src.data_models.postgres_models import CorrectionItem, CorrectionType, JobListingItem
from src.data_models.minio_models import FileItem

# Service Layer
from src.service_layer.correction_services import CorrectionService
from src.service_layer.joblisting_service import JobListingService
from src.service_layer.file_service import FileService

# Repositories
from src.data_repositories.miniO_repository.CRUD_minio import MinioRepository

router = APIRouter()
############################################
@router.post("/reset_schema")
def reset_schema():
    try:
        result = subprocess.run(["sh", "./reset_schema.sh"], capture_output=True, text=True, check=True)
        return {"detail": "Schema reset completed successfully", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Schema reset failed: {e.stderr}")
############################################

############################################
# Correction Service (PostgreSQL)
############################################

def get_correction_service(db: Session = Depends(PostgressConnection.get_db)) -> CorrectionService:
    return CorrectionService(db)

@router.get("/corrections", response_model=List[CorrectionItem])
def read_corrections(
    correction_type: Optional[CorrectionType] = None,
    service: CorrectionService = Depends(get_correction_service)
) -> List[CorrectionItem]:
    return service.get_corrections(correction_type)

@router.post("/corrections", response_model=CorrectionItem)
def create_correction(
    correction: CorrectionItem,
    service: CorrectionService = Depends(get_correction_service)
) -> CorrectionItem:
    try:
        return service.create_correction(correction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/corrections/{correction_id}", response_model=CorrectionItem)
def remove_correction(
    correction_id: int,
    service: CorrectionService = Depends(get_correction_service)
) -> CorrectionItem:
    deleted_correction = service.remove_correction(correction_id)
    if not deleted_correction:
        raise HTTPException(status_code=404, detail="Correction not found")
    return deleted_correction

############################################
# Job Listing Service (PostgreSQL)
############################################

def get_job_listing_service(db: Session = Depends(PostgressConnection.get_db)) -> JobListingService:
    return JobListingService(db)

@router.get("/job_listings", response_model=List[JobListingItem])
def read_job_listings(
    service: JobListingService = Depends(get_job_listing_service)
) -> List[JobListingItem]:
    return service.get_all_job_listings()

############################################
# File Service (MinIO)
############################################
from src.config.config_top_level import Config
def get_file_service() -> FileService:

    minio_connection = MiniOConnection.get_minio_connection()
    repository = MinioRepository(minio_connection)
    return FileService(repository)

@router.post("/upload_files", response_model=List[FileItem])
async def upload_files(
    files: List[UploadFile] = File(...),
    file_service: FileService = Depends(get_file_service)
) -> List[FileItem]:
    try:
        return await file_service.process_files(files)
    except Exception as e:
        logging.error(f"Error processing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_files/{bucket_type}/{file_name}")
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

@router.get("/files/{bucket_type}", response_model=List[FileItem])
def list_files(bucket_type: str, file_service: FileService = Depends(get_file_service)) -> List[FileItem]:
    return file_service.list_files(bucket_type)


############################### Extracted Text Endpoints ###############################
# Extracted Text Endpoints
# @router.post("/extract_text", response_model=ExtractedText)
# async def extract_text(
#     file_name: str = Body(..., embed=True),
#     bucket_type: str = Body(..., embed=True),
#     file_service: FileService = Depends(get_file_service)
# ):
#     """
#     Extract text from a PDF (or txt) stored in MinIO.
#     """
#     try:
#         # 1) Retrieve bytes from MinIO
#         pdf_bytes = file_service.get_file_content(file_name, bucket_type)
        
#         # 2) Perform text extraction (pseudo code with docling or PyPDF2)
#         # docling usage example:
#         # from docling.document_converter import DocumentConverter
#         # extracted_text = DocumentConverter.pdf_to_text(pdf_bytes)

#         extracted_text = "Pretend we extracted something from the PDF here..."

#         # 3) Return an ExtractedText model
#         # If you want to store it, you can also do that in a DB or back to MinIO
#         return ExtractedText(
#             file_name=file_name,
#             text=extracted_text
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


