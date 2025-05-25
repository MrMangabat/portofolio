# backend/services/service_cover_letter/src/routes/routes_embedding_file_service.py

"""
FastAPI route for embedding uploaded files into Qdrant.

Purpose:
    - Receive files from HTTP clients (frontend, agent, test runner, etc.)
    - Trigger service-layer embedding logic.
    - Respond with embedding status and referenceable file_id.

Reasoning:
    Keeps Qdrant logic decoupled and ensures the upload interface is modular and reusable.
"""

import uuid
from io import BytesIO
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends

from src.config.config_db_connections import QdrantConnection
from src.data_repositories.qdrant_repository.CRUD_qdrant import QdrantCoverLetterRepository
from src.service_layer.embbing_file_service import FileEmbeddingService

router = APIRouter()


def get_embedding_service() -> FileEmbeddingService:
    """
    Dependency injector for the embedding service.
    """
    qdrant_conn = QdrantConnection()
    qdrant_repo = QdrantCoverLetterRepository(connection=qdrant_conn)
    return FileEmbeddingService(qdrant_repository=qdrant_repo)


@router.post("/embed-files", summary="Upload and embed files into Qdrant")
async def embed_files(
    files: List[UploadFile] = File(...),
    service: FileEmbeddingService = Depends(get_embedding_service)
):
    """
    Receives multiple files, extracts text, embeds into Qdrant, and returns their UUIDs.
    """
    response = []

    for file in files:
        file_id = str(uuid.uuid4())
        file_stream = BytesIO(await file.read())

        success = service.embed_file(
            file_stream=file_stream,
            filename=file.filename,
            file_id=file_id,
            metadata={"original_name": file.filename}
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to embed file: {file.filename}"
            )

        response.append({"file_id": file_id, "filename": file.filename})

    return {"status": "success", "embedded_files": response}


