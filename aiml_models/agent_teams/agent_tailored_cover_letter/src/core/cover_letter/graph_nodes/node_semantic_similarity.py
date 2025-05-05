# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_semantic_similarity.py

from typing import Dict, List, Optional
from io import BytesIO
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

from src.core.graph_master.master_graph_flow import CoverLetterGraphState
from langgraph.graph import StateGraph

from src.infrastructure.files_client import MinioFileClient
from src.core.cover_letter.components.file_text_extractor import FileTextExtractor
from src.infrastructure.vectorstore import QdrantVectorSearch


def retrieve_best_matching_template(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node that:
    - Fetches cover letter files from MinIO
    - Extracts text content using FileTextExtractor
    - Embeds and stores them in Qdrant
    - Searches for the best match based on job description

    Returns:
        Updated state with best_match_template_cover_letter
    """

    # Load job description
    job_description: str = state["job_description"]

    # Init clients
    file_client = MinioFileClient()
    extractor = FileTextExtractor()
    vectorstore = QdrantVectorSearch()

    # Get list of files from cover_letter bucket
    file_names: List[str] = file_client.list_files("cover_letters")
    documents: List[Document] = []

    for filename in file_names:
        file_data: Optional[BytesIO] = file_client.fetch_file("cover_letters", filename)
        if file_data:
            text = extractor.extract_text(file_data, filename)
            if text:
                documents.append(Document(page_content=text, metadata={"filename": filename}))

    # Upsert all into vectorstore
    vectorstore.upsert_documents(documents)

    # Perform semantic search
    best_match: Optional[str] = vectorstore.search(job_description)

    return {**state, "best_match_template_cover_letter": best_match}
