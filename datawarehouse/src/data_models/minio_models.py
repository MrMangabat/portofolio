# backend/jobapplication_feature/data_models/minio_models.py
from typing import Optional

from pydantic import BaseModel, Field

class FileItem(BaseModel):
    id: Optional[int] = None
    file_name: str = Field(..., description="The name of the file.")
    original_file_name: str = Field(..., description="The original name of the file.")
    size: int = Field(..., description="The size of the file in bytes.")
    file_type: str = Field(..., description="The type of the file, e.g. '.pdf', '.txt', '.jpeg', etc.")


class ExtractedText(BaseModel):
    id: Optional[int] = None
    file_name: str = Field(..., description="The name of the file.")
    text: str = Field(..., description="The extracted text from the file.")


class ManualEntry(BaseModel):
    # id: Optional[int] = None
    file_name: str = Field(..., description="The name of the file.")
    text: str = Field(..., description="The manually entered text.")