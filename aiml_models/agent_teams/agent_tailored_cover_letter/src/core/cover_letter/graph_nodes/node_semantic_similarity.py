# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_semantic_similarity.py
# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_semantic_similarity.py

from typing import Optional
from datetime import datetime
from langchain_core.documents import Document
import logging

from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.config.config_low_level import QdrantConnection
from src.infrastructure.vectorstore import QdrantVectorSearch

logger = logging.getLogger(__name__)


def retrieve_best_matching_template(state: CoverLetterGraphState) -> CoverLetterGraphState:
    """
    LangGraph node that:
    - Searches Qdrant for the most semantically similar cover letter based on the job description.
    - Assumes all embedding and upsertion into Qdrant was already handled by the backend service.

    Returns:
        Updated state with best_match_template_cover_letter and agent_trace.
    """
    logger.info("SEMANTIC SIMILARITY NODE: Searching for matching cover letter")

    # Extract the job description from the graph state
    job_description: str = state["job_description"]

    # Set up Qdrant connection
    qdrant_connection = QdrantConnection()
    vectorstore = QdrantVectorSearch(
        connection=qdrant_connection,
        collection_name=qdrant_connection.default_collection
    )

    # Search Qdrant using the job description
    best_match: Optional[Document] = vectorstore.search(query=job_description)

    # Parse filename from metadata if available
    best_match_filename: Optional[str] = (
        best_match[0].metadata.get("filename") if best_match else None
    )
    
    # Log timestamped trace for debugging and observability
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    trace = state.get("agent_trace", [])
    trace.append(f"NODE: semantic_similarity @ {timestamp}")

    # Log state details
    logger.info("Iteration: %s", state['iterations'])
    logger.info("Best semantic match (filename): %s", best_match_filename)
    logger.info("Agent trace: %s", trace)
    logger.info("Finished semantic similarity node")

    # Return updated graph state
    return {
        **state,
        "best_match_template_cover_letter": best_match_filename,
        "agent_trace": trace
    }
