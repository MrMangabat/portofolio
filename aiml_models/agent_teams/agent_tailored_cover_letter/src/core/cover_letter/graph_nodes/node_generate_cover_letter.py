# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_generate_cover_letter.py

from datetime import datetime
from src.core.graph_master.initialize_graph import CoverLetterGraphState
from langgraph.graph import StateGraph

from src.core.cover_letter.agent_service_class_cover_letter import AgentServiceClassCoverLetter
from src.infrastructure.correction_client import CorrectionsClient
from src.core.cover_letter.components.cover_letter_prompt_builder import CoverLetterPromptBuilder
from src.core.cover_letter.components.cover_letter_parser import CoverLetterResultParser
from src.infrastructure.llm_client import LLMClient


def generate_cover_letter(state: CoverLetterGraphState) -> StateGraph:
    """
    LangGraph node for generating a personalized cover letter.

    Args:
        state (CoverLetterGraphState): Current LangGraph state, including job analysis, skills, CV, and user rules.

    Returns:
        CoverLetterGraphState: Updated state with generated cover letter content under key 'cover_letter_output'.
    """
    print("------ COVER LETTER NODE: Generating Cover Letter ------")

    # Step 1: Instantiate the agent
    agent = AgentServiceClassCoverLetter(
        corrections_client=CorrectionsClient(),
        prompt_builder=CoverLetterPromptBuilder(),
        response_parser=CoverLetterResultParser(),
        llm_client=LLMClient()
    )

    result = agent.generate_cover_letter(state)

    # Step 2: Log messages
    messages = state["messages"] + [
        ("system", f"[cover_letter_gen] Generated introduction: {result.introduction}"),
        ("system", f"[cover_letter_gen] Skills emphasis: {result.skills}"),
        ("system", f"[cover_letter_gen] Thank-you section: {result.thank_you}")
    ]

    # Step 3: Append to agent_trace
    trace = state.get("agent_trace", [])
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    trace.append(f"NODE: cover_letter_gen @ {timestamp}")

    # Step 4: Debug print
    print(f"\n------- ITERATION: {state['iterations']} -------")
    print("----- Introduction:\n", result.introduction)
    print("----- Motivation:\n", result.motivation)
    print("----- Thank you:\n", result.thank_you)
    print("----- Agent Trace:", trace)
    print("--------------------------------------------------\n")

    return {
        **state,
        "generation": result,
        "cover_letter_output": result.dict(),
        "messages": messages,
        "agent_trace": trace,
    }
