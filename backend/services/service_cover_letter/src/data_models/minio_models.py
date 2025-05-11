# backend/services/service_cover_letter/src/data_models/minio_models.py
from typing import Optional

from pydantic import BaseModel, Field

class FileItem(BaseModel):
    file_id: str = Field(..., description="Unique identifier for the file (UUID + extension).")
    file_name: str = Field(..., description="The internal name of the file in MinIO.")
    original_file_name: str = Field(..., description="The original name of the uploaded file.")
    bucket: str = Field(..., description="Bucket where the file is stored.")
    size: int = Field(..., description="Size of the file in bytes.")
    file_type: str = Field(..., description="File extension, e.g., 'pdf', 'txt', etc.")

class ExtractedText(BaseModel):
    id: Optional[int] = None
    file_name: str = Field(..., description="The name of the file.")
    text: str = Field(..., description="The extracted text from the file.")


class ManualEntry(BaseModel):
    # id: Optional[int] = None
    file_name: str = Field(..., description="The name of the file.")
    text: str = Field(..., description="The manually entered text.")