# backend/services/service_cover_letter/src/data_models/minio_models.py
from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from uuid import UUID
from pydantic import BaseModel, Field, validator
from typing import Literal

class FileItem(BaseModel):
    """
    Represents a file stored in MinIO with full metadata.

    Purpose:
        Serves as a schema to represent files across the system.
    Capabilities:
        Used for listing files, storing metadata, and tracking UUID links to other services like Qdrant.
    Reasoning:
        file_id is stored as a UUID string to ensure universal compatibility with Qdrant, Kafka, MinIO, and JSON.
        A validator enforces correct UUID formatting without requiring a UUID object.
    """
    file_id: str = Field(..., description="Unique identifier for the file (UUID as string).")
    file_name: str = Field(..., description="The internal name of the file in MinIO.")
    original_file_name: str = Field(..., description="The original name of the uploaded file.")
    bucket: Literal["cover-letters", "cv", "images"] = Field(..., description="Bucket category for the file.")
    size: int = Field(..., description="Size of the file in bytes.")
    file_type: str = Field(..., description="File extension, e.g., 'pdf', 'txt', etc.")



class ExtractedText(BaseModel):
    """
    Stores extracted text from a file for downstream NLP processing.

    Purpose:
        Represents the outcome of PDF/DOCX parsing.
    Capabilities:
        Maps back to file metadata via `file_name`.
    """
    id: Optional[int] = None
    file_name: str = Field(..., description="The name of the file.")
    text: str = Field(..., description="The extracted text from the file.")