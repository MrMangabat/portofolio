# backend/services/service_cover_letter/src/data_repositories/qdrant_repository/CRUD_qdrant.py
"""
QdrantCoverLetterRepository handles all Qdrant operations related to cover letter embeddings.

Purpose:
    - Acts as a repository layer to manage embedding vectors for cover letter documents.

Capabilities:
    - Embed file content using HuggingFace sentence-transformers.
    - Upsert embeddings into a Qdrant collection.
    - Perform similarity-based search using native Qdrant client.
    - Delete vectors by file_id if needed.

Reasoning:
    This design isolates the Qdrant logic into a dedicated microservice layer owned by the backend,
    ensuring agent flows downstream can retrieve from a clean and queryable vector index without performing raw ingestion.
"""

import uuid
import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue, ScoredPoint
from sentence_transformers import SentenceTransformer

from src.config.config_low_level import QdrantConnection


class QdrantCoverLetterRepository:
    def __init__(self, connection: QdrantConnection) -> None:
        """
        Initialize Qdrant repository for cover letter embeddings.

        Args:
            connection (QdrantConnection): Shared client and config for Qdrant.
        """
        self.client: QdrantClient = connection.client
        self.collection_name: str = connection.default_collection

        # SentenceTransformer instance directly
        self.embedding_model: SentenceTransformer = SentenceTransformer(
            "sentence-transformers/all-mpnet-base-v2"
        )

    def upsert_file_embedding(self, file_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Embed file content and upsert it into Qdrant.

        Args:
            file_id (str): Unique file identifier (UUID-based).
            text (str): Plain text content extracted from the file.
            metadata (Optional[Dict[str, Any]]): Additional traceable metadata.
        """
        vector: List[float] = self.embedding_model.encode(text).tolist()

        payload: Dict[str, Any] = {
            "file_id": file_id,
            "uuid": str(uuid.uuid4()),
            "type": "cover_letter",
            "timestamp": datetime.now().isoformat(),
        }
        if metadata:
            payload.update(metadata)

        # Ensure collection exists
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=len(vector), distance=Distance.COSINE),
            )

        point = PointStruct(id=file_id, vector=vector, payload=payload)
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search_similar_documents(self, query: str, k: int = 3, threshold: float = 0.6) -> Optional[Tuple[Dict[str, Any], float]]:
        """
        Perform a semantic search in Qdrant for documents similar to the query.

        Args:
            query (str): The input text to search for.
            k (int): Number of top results to retrieve.
            threshold (float): Minimum similarity score threshold.

        Returns:
            Optional[Tuple[Dict[str, Any], float]]: Best match payload and similarity score.
        """
        vector: List[float] = self.embedding_model.encode(query).tolist()

        search_result: List[ScoredPoint] = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=k,
            score_threshold=threshold
        )

        if not search_result:
            return None

        best_match = search_result[0]
        return best_match.payload, best_match.score

    def delete_vector_by_file_id(self, file_id: str) -> None:
        """
        Delete all vectors in Qdrant associated with a given file_id.

        Args:
            file_id (str): The file identifier whose vectors should be removed.
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(key="file_id", match=MatchValue(value=file_id))
                ]
            )
        )