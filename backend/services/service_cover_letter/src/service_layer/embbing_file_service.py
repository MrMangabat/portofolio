# backend/services/service_cover_letter/src/service_layer/embbing_file_service.py
"""
FileEmbeddingService handles end-to-end logic for embedding uploaded files into Qdrant.

Purpose:
    - Extract text from uploaded files (PDF, DOCX).
    - Embed the text and push to Qdrant vector store.
    - Attach metadata for traceability and future search.

Capabilities:
    - Handles ByteIO and metadata inputs.
    - Decides on the correct text extractor backend.
    - Delegates vector storage to Qdrant repository.

Reasoning:
    Keeps LangChain + Qdrant logic out of API layer and maintains clean modular separation.
"""

import logging
from typing import Optional, Dict
from io import BytesIO

from src.service_layer.text_extractor import FileTextExtractor
from src.data_repositories.qdrant_repository.CRUD_qdrant import QdrantCoverLetterRepository


class FileEmbeddingService:
    def __init__(self, qdrant_repository: QdrantCoverLetterRepository) -> None:
        """
        Args:
            qdrant_repository (QdrantCoverLetterRepository): Dependency for Qdrant upsert logic.
        """
        self.qdrant_repository = qdrant_repository
        self.logger = logging.getLogger(__name__)

    def embed_file(self, file_stream: BytesIO, filename: str, file_id: str, metadata: Optional[Dict[str, str]] = None) -> bool:
        """
        Extracts and embeds the text from a file into Qdrant.

        Args:
            file_stream (BytesIO): Raw uploaded file stream.
            filename (str): Name of the file.
            file_id (str): Unique identifier tied to the file.
            metadata (Optional[Dict[str, str]]): Custom tags (e.g., user_id, upload source).

        Returns:
            bool: True if embedded successfully, False otherwise.
        """
        text: Optional[str] = FileTextExtractor.extract_text(file_stream, filename)

        if not text:
            self.logger.warning(f"No text extracted from file: {filename}")
            return False

        try:
            self.qdrant_repository.upsert_file_embedding(
                file_id=file_id,
                text=text,
                metadata=metadata or {}
            )
            self.logger.info(f"Successfully embedded: {filename} → file_id={file_id}")
            self.logger.info(f"Generated embeddings for file {filename}.")
            return True
        except Exception as e:
            self.logger.error(f"Embedding failed for {filename}: {e}")
            return False
