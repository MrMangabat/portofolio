# /home/mangabat/projects/portofolio/backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/master_graph_flow.py
# This file builds the entire execution graph for the cover letter generation process/execution tree

from typing import TypedDict, List, Annotated, Dict, Any, Optional
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.graph import StateGraph, START, END

import uuid
from pprint import pprint
from langgraph.checkpoint.sqlite import SqliteSaver

# Node imports
from src.core.company_analysis.graph_nodes.node_generate_vacancy_analysis import generate_vacancy_analysis
from src.core.company_analysis.graph_nodes.node_get_skills import get_skills
from src.core.cover_letter.graph_nodes.node_generate_cover_letter import generate_cover_letter
from src.core.cover_letter.graph_nodes.node_semantic_similarity import retrieve_best_matching_template
from src.core.editorial.graph_nodes.node_check_editorial_output import check_editorial_generation
from src.core.editorial.graph_nodes.node_validate_and_correct_editorial import validate_and_correct_editorial
from src.core.nlp_rules_classifier.graph_nodes.node_grammatical_rules_classifier import grammatical_rules_classifier
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.editorial.graph_nodes.node_decide_editorial_correction import decide_editorial_next_step

def build_master_graph():
    """
    Builds the master LangGraph flow for generating a validated, personalized cover letter.

    Steps:
    - Extract user skills
    - Retrieve best matching template (semantic similarity search)
    - Analyze job vacancy
    - Generate initial cover letter
    - Run editorial correction loop until validation passes or max iterations
    - (Future) Human-in-the-loop
    - (Future) LaTeX + PDF generation

    Returns:
        LangGraph: Compiled execution graph
    """
    graph_builder = StateGraph(CoverLetterGraphState)

    # Add core generation steps
    graph_builder.add_node("get_skills", get_skills)
    graph_builder.add_node("semantic_similarity", retrieve_best_matching_template)
    graph_builder.add_node("analyse_vacancy", generate_vacancy_analysis)
    graph_builder.add_node("generate_cover_letter", generate_cover_letter)

    # Editorial validation loop
    graph_builder.add_node("check_editorial_output", check_editorial_generation)
    graph_builder.add_node("nlp_rules_classifier", grammatical_rules_classifier) # TODO: Add NLP rules classifier
    graph_builder.add_node("validate_and_correct_editorial", validate_and_correct_editorial)

    # Optional future steps (commented out for now)
    # graph_builder.add_node("human_in_the_loop", lambda state: state)  # TODO
    # graph_builder.add_node("create_pdf", lambda state: state)  # TODO

    # Define edges
    graph_builder.set_entry_point("get_skills")
    graph_builder.add_edge("get_skills", "semantic_similarity")
    graph_builder.add_edge("semantic_similarity", "analyse_vacancy")
    graph_builder.add_edge("analyse_vacancy", "generate_cover_letter")
    graph_builder.add_edge("generate_cover_letter", "check_editorial_output")

    # Conditional logic: Editorial validation loop or exit
    graph_builder.add_conditional_edges(
        "check_editorial_output",
        decide_editorial_next_step,
        path_map={
            "validate_and_correct_editorial": "validate_and_correct_editorial",
            "finalize_output": END
        }
    )
    graph_builder.add_edge("validate_and_correct_editorial", "check_editorial_output")

    graph_builder.set_finish_point(END)

    # Generate a unique thread ID
    unique_id = str(uuid.uuid4())

    # Configuration for the graph run
    config = {
        "configurable": {
            "thread_id": unique_id,
        }
    }

    # Set up the memory and compile the graph
    memory = SqliteSaver.from_conn_string(":memory:")
    t = graph_builder.compile(checkpointer=memory, config=config)

    for output in t.invoke(initial_state=CoverLetterGraphState(), config=config):
        # Print the output state for debugging
        print("Output state:")
        pprint(output)
        print("--------------------------------------------------")
    # Display the graph
    from IPython.display import Image, display

    try:
        display(Image(graph_builder.get_graph(xray=True).draw_mermaid_png()))
    except Exception as e:
        print(f"Error displaying the graph: {e}")


if __name__ == "__main__":
    build_master_graph()
