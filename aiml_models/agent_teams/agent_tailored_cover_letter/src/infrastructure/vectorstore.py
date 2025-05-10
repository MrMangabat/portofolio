# aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/vectorstore.py



"""
QdrantVectorSearch provides semantic similarity search functionality using direct QdrantClient access.

Purpose:
    - Search for top-k similar documents based on query embedding.
    - Return the best match above a defined similarity threshold.

Capabilities:
    - Encodes query using SentenceTransformers.
    - Performs raw vector search in Qdrant.
    - Outputs LangChain-compatible Document with score.

Reasoning:
    Uses lightweight native QdrantClient for speed and control.
"""

from typing import List, Optional, Tuple
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams, ScoredPoint
from src.config.config_low_level import QdrantConnection


class QdrantVectorSearch:
    def __init__(self, connection: QdrantConnection, collection_name: Optional[str] = None) -> None:
        """
        Initializes the vector search with QdrantClient and embedding model.

        Args:
            connection (QdrantConnection): Pre-initialized Qdrant connection.
            collection_name (Optional[str]): Target Qdrant collection.
        """
        # Sentence-transformer model for embedding queries
        self.embedding_model: SentenceTransformer = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

        # Direct Qdrant client instance
        self.client: QdrantClient = connection.client

        # Collection name to query from
        self.collection_name: str = collection_name or connection.default_collection

    def search(self, query: str, k: int = 2, threshold: float = 0.6) -> Optional[Tuple[Document, float]]:
        """
        Performs semantic search in Qdrant and returns best result if above threshold.

        Args:
            query (str): Raw text query.
            k (int): Number of top results to consider.
            threshold (float): Minimum score to qualify as a match.

        Returns:
            Optional[Tuple[Document, float]]: Top match and its score, or None if no good match.
        """
        # Encode the query into vector space
        query_vector: List[float] = self.embedding_model.encode(query, normalize_embeddings=False).tolist()

        # Search directly in Qdrant
        results: List[ScoredPoint] = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=k,
            with_payload=True,
            search_params=SearchParams(hnsw_ef=128),  # Optional param
        )

        if not results:
            return f"No fileembedding found: {None}"

        best_result: ScoredPoint = results[0]
        score: float = best_result.score or threshold



        # Wrap result in a Document object for downstream LangGraph use
        document = Document(
            page_content=best_result.payload.get("text", ""),
            metadata={"score": score, "id": best_result.id}
        )

        return document, score