"""Graph builder for CV Resume Builder workflow.

This module builds and compiles the hierarchical LangGraph workflow
with a 4-tier supervisor architecture.
"""

from langgraph.graph import END, START, StateGraph

from .nodes import main_supervisor
from .nodes.officers import (
    document_generation_officer,
    personality_analysis_officer,
    research_analysis_officer,
)
from .nodes.workers import (
    analyze_profile,
    generate_documents,
    reflect_on_output,
    user_review,
)
from .nodes.workers.research import (
    business_intelligence_analyst,
    company_profile_analyst,
    financial_analyst,
    macro_officer,
)
from .routing import route_main_supervisor, route_officer
from .state import State


def build_graph() -> StateGraph:
    """Build and compile the hierarchical supervisor graph.

    Returns:
        StateGraph: Compiled LangGraph workflow
    """
    # Initialize graph
    graph = StateGraph(State)

    # ========================================
    # TIER 1: Main Supervisor (Captain)
    # ========================================
    graph.add_node("main_supervisor", main_supervisor)

    # ========================================
    # TIER 2: Officers (Sub-Supervisors)
    # ========================================
    graph.add_node("research_analysis_officer", research_analysis_officer)
    graph.add_node("personality_analysis_officer", personality_analysis_officer)
    graph.add_node("document_generation_officer", document_generation_officer)

    # ========================================
    # TIER 3: Workers (General)
    # ========================================
    # Personality analysis team workers
    graph.add_node("analyze_profile", analyze_profile)

    # Document generation team workers
    graph.add_node("generate_docs", generate_documents)
    graph.add_node("reflect", reflect_on_output)
    graph.add_node("user_review", user_review)

    # ========================================
    # TIER 4: Research & Analysis Sub-Agents (M&A DD)
    # ========================================
    graph.add_node("financial_analyst", financial_analyst)
    graph.add_node("business_intelligence_analyst", business_intelligence_analyst)
    graph.add_node("company_profile_analyst", company_profile_analyst)
    graph.add_node("macro_officer", macro_officer)

    # ========================================
    # EDGES: Entry Point
    # ========================================
    graph.add_edge(START, "main_supervisor")

    # ========================================
    # EDGES: Main Supervisor -> Officers
    # ========================================
    graph.add_conditional_edges(
        "main_supervisor",
        route_main_supervisor,
        {
            "research_analysis_officer": "research_analysis_officer",
            "personality_analysis_officer": "personality_analysis_officer",
            "document_generation_officer": "document_generation_officer",
            "FINISH": END,
        },
    )

    # ========================================
    # EDGES: Research Officer -> Sub-Agents (4-tier)
    # ========================================
    graph.add_conditional_edges(
        "research_analysis_officer",
        route_officer,
        {
            "financial_analyst": "financial_analyst",
            "business_intelligence_analyst": "business_intelligence_analyst",
            "company_profile_analyst": "company_profile_analyst",
            "macro_officer": "macro_officer",
            "report_to_supervisor": "main_supervisor",
        },
    )
    # Sub-agents report back to Research Officer
    graph.add_edge("financial_analyst", "research_analysis_officer")
    graph.add_edge("business_intelligence_analyst", "research_analysis_officer")
    graph.add_edge("company_profile_analyst", "research_analysis_officer")
    graph.add_edge("macro_officer", "research_analysis_officer")

    # ========================================
    # EDGES: Personality Officer -> Workers
    # ========================================
    graph.add_conditional_edges(
        "personality_analysis_officer",
        route_officer,
        {
            "analyze_profile": "analyze_profile",
            "report_to_supervisor": "main_supervisor",
        },
    )
    # Workers report back to their officer
    graph.add_edge("analyze_profile", "personality_analysis_officer")

    # ========================================
    # EDGES: Document Officer -> Workers
    # ========================================
    graph.add_conditional_edges(
        "document_generation_officer",
        route_officer,
        {
            "generate_docs": "generate_docs",
            "reflect": "reflect",
            "user_review": "user_review",
            "report_to_supervisor": "main_supervisor",
        },
    )
    # Workers report back to their officer
    graph.add_edge("generate_docs", "document_generation_officer")
    graph.add_edge("reflect", "document_generation_officer")
    graph.add_edge("user_review", "document_generation_officer")

    # Compile the agent
    return graph.compile()
