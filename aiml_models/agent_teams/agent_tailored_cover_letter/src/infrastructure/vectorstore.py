# aiml_models/agent_teams/agent_tailored_cover_letter/src/infrastructure/vectorstore.py

from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from typing import List, Optional, Tuple

class QdrantVectorSearch:
    def __init__(self, host: str, collection_name: str) -> None:
        """
        Purpose:
            Initialize Qdrant vector search with a dense embedding model and collection config.

        Capabilities:
            - Connects to a running Qdrant instance.
            - Initializes sentence-transformer embedding model.
            - Sets target collection name for storage/retrieval.

        Args:
            host (str): Qdrant host address (e.g., 'localhost' or Docker hostname).
            collection_name (str): Target collection in Qdrant for storing embeddings.
        """
        self.embedding_model: HuggingFaceEmbeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            encode_kwargs={'normalize_embeddings': False}
        )
        self.client: QdrantClient = QdrantClient(host=host)
        self.collection_name: str = collection_name

    def upsert_documents(self, documents: List[Document]) -> None:
        Qdrant.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            client=self.client,
            collection_name=self.collection_name,
        )

    def search(self, query: str, k: int = 3, threshold: float = 0.6) -> Optional[Tuple[Document, float]]:
        retriever = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_model
        ).as_retriever(search_type="similarity", search_kwargs={"k": k}, score_threshold = threshold)

        results = retriever.get_relevant_documents(query)

        if not results:
            return None

        # You can store a custom similarity score in metadata if needed
        best_result = results[0]
        return best_result, best_result.metadata.get("score", 0.0)