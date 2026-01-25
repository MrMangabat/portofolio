# backend/services/service_cover_letter/src/config/connections/qdrant_connection.py
"""
Qdrant connection handler for the cover_letter service.
"""

from qdrant_client import QdrantClient, models

from src.config.settings import CoverLetterSettings

settings_from_env = CoverLetterSettings()


class QdrantConnection:
    def __init__(self) -> None:
        self.url: str = settings_from_env.QDRANT_URL
        self.default_collection: str = "embedded_cover_letters"

        self.client = QdrantClient(url=self.url)

        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        """
        Check if the default collection exists in Qdrant.
        If not, create it with appropriate vector configuration.
        """
        existing_collections = [c.name for c in self.client.get_collections().collections]

        if self.default_collection not in existing_collections:
            self.client.create_collection(
                collection_name=self.default_collection,
                vectors_config=models.VectorParams(
                    size=768,  # required for sentence-transformers
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection: {self.default_collection}")
        else:
            print(f"Collection already exists: {self.default_collection}")
