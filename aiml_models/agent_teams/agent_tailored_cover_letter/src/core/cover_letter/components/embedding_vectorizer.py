# src/core/cover_letter/components/embedding_vectorizer.py

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingVectorizer:
    """
    Purpose:
        Converts raw text data into dense vector representations using a SentenceTransformer model.

    Capabilities:
        - Load a pretrained sentence-transformers model.
        - Encode text or list of text entries into consistent embeddings.
        - Prepares output for direct upsert into Qdrant.

    Reasoning:
        Keeps all embedding logic decoupled from vector store logic.
        Supports flexible usage and future upgrades to multilingual or domain-specific models.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        # Load the sentence transformer model
        self.model: SentenceTransformer = SentenceTransformer(model_name)

    def embed_text(self, content: str) -> List[float]:
        """
        Embeds a single piece of text into a dense vector.
        """
        # Generate a dense vector representation
        return self.model.encode(content, convert_to_numpy=True).tolist()

    def embed_multiple(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts into a list of dense vectors.
        """
        return self.model.encode(texts, convert_to_numpy=True).tolist()
