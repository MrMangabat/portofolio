# /home/mangabat/projects/portofolio/backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/master_graph_flow.py
# This file builds the entire execution graph for the cover letter generation process/execution tree

# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/master_graph_flow.py

"""quick hack, delete when the flow is stable"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from src.core.company_analysis.graph_nodes.node_generate_vacancy_analysis import generate_vacancy_analysis
##############################################


"""
This file builds the entire execution graph for the cover letter generation process.
It includes:
- Semantic template retrieval
- Job analysis
- Cover letter generation
- Editorial validation loop
- Agent trace logging
"""

from typing import TypedDict, List, Annotated, Dict, Any, Optional
from langgraph.graph.message import add_messages, AnyMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from pprint import pprint
import uuid

# Node imports
from src.core.company_analysis.graph_nodes.node_generate_vacancy_analysis import generate_vacancy_analysis
from src.core.company_analysis.graph_nodes.node_get_skills import get_skills
from src.core.cover_letter.graph_nodes.node_generate_cover_letter import generate_cover_letter
from src.core.cover_letter.graph_nodes.node_semantic_similarity import retrieve_best_matching_template
from src.core.editorial.graph_nodes.node_user_in_the_loop import user_in_the_loop
from src.core.editorial.graph_nodes.node_validate_and_correct_editorial import validate_and_correct_editorial
from src.core.editorial.graph_nodes.node_decide_editorial_correction import decide_editorial_next_step

job_description = """
Can you deliver IT projects across a large Nordic Team?
Are you driven by a passion for IT projects and a desire to manage important projects? If you're nodding yes, then you're the talent we're looking for to join our dynamic team!
Your role
Step into the role of an IT Project Manager and become the driver of our organization's changes. You will supplement our current Project Manager and your main area will be projects within IT Operations, where we have a significant amount of projects ongoing – our current priority is to integrate Finland/Estonia into the existing Nordic infrastructure. The scope is however broader – we handle infrastructure, security, HR & Customer Service related IT-projects as well as the IT-part of construction projects for new stores/new offices – as we keep expanding.
You'll collaborate closely with many stakeholders across the IT team and across the entire Nordic organization.

Your responsibilities:
Scope, plan, drive and deliver IT projects
Ensure transparency on progress, risks & cost
Creatively solve problems when they arise
Conduct project and steerco meetings, as relevant
Communication, change management and stakeholder management
Contribute to improving the project model & structures
Your new playground:
Join our Nordic IT team, which spans across Denmark, Iceland, Norway, Sweden, and is on the cusp of welcoming Finland and Estonia. With 55 stores, 5 service centers, 5500 users, and a rich tapestry of technologies like Azure, SAP S/4 Hana, Adobe Commerce (Magento), Viking POS, SD-WAN+MPLS network, 2500+ PCs, over 200 servers, and partnerships with external vendors, your work will be both challenging and rewarding.

At BAUHAUS, Nordic IT is a virtual, multicultural team of approx. 90 people that values diversity and foster a flat hierarchy, empowering you to turn your ideas into reality swiftly.

Advance your IT career with our nordic team
What we expect from you:

A minimum of five years of experience in IT project management, with a preference for backgrounds in retail or e-commerce environments
A bachelor's degree in computer science, information systems, or a related field is ideal, but we value your hands-on experience even more
A proven track record of managing projects with tangible outcomes
Excellent communication and collaboration skills, capable of articulating concerns and solutions to a diverse audience, from technical teams to senior management
A team player with a knack for building cross-functional relationships
Certifications like PRINCE2 will be considered an asset
Proficiency in English, with either Danish or Swedish language skills being a significant plus
What’s in it for you?
Join a dynamic team of experts in Denmark (Tilst) and Sweden (Stockholm), where cross-team collaboration is the key to our success
Engage in thrilling challenges within a rapidly growing business, with a focus on new technologies
Look forward to a competitive salary and benefits package
Enjoy a flexible and supportive work environment, with options for partial remote work or from one of our offices
Continuous opportunities for professional development and career advancement
Be part of a fast-growing, innovative company where your contributions will support our mission to make home improvement accessible and affordable for all
Direct reporting to Head of IT Operations – A career opportunity not to be missed
This pivotal position offers a unique opportunity to report directly to our Head of IT Operations, Niels Nielsen. As we do not have a CIO, the overall responsibility for IT is shared between the Head of IT Operations and Head of Business Applications. Based in either Tilst (Aarhus) or Järfälla (Stockholm), this role includes occasional travel, providing a blend of stability and variety."""

class testState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    job_description: str
    skills: list[str]
    analysis_output: Optional[Dict[str, Any]]
    matching_skills: Optional[Dict[str, bool]]
    cover_letter_output: Optional[Dict[str, Any]]
    generation: str
    words_to_avoid: List[str]
    sentences_to_avoid: List[str]
    best_match_template_cover_letter: Optional[str]
    cv: str
    agent_trace: Optional[List[str]]
    editorial_violations: Optional[List[str]]
    generation_violation_log: Optional[Dict[str, Any]]
    iterations: int


def build_master_graph(job_offer: str) -> None:
    graph_builder = StateGraph(testState)

    # Register all graph nodes
    graph_builder.add_node("get_skills", get_skills)
    graph_builder.add_node("semantic_similarity", retrieve_best_matching_template)
    graph_builder.add_node("analyse_vacancy", generate_vacancy_analysis)
    graph_builder.add_node("generate_cover_letter", generate_cover_letter)
    graph_builder.add_node("validate_and_correct_editorial", validate_and_correct_editorial)
    graph_builder.add_node("user_in_the_loop", user_in_the_loop)

    # Define graph flow
    graph_builder.set_entry_point("get_skills")
    graph_builder.add_edge("get_skills", "semantic_similarity")
    graph_builder.add_edge("semantic_similarity", "analyse_vacancy")
    graph_builder.add_edge("analyse_vacancy", "generate_cover_letter")
    graph_builder.add_edge("generate_cover_letter", "validate_and_correct_editorial")

    # Conditional loop after editorial
    graph_builder.add_conditional_edges(
        "validate_and_correct_editorial",
        decide_editorial_next_step,
        path_map={
            "validate_and_correct_editorial": "validate_and_correct_editorial",
            "user_in_the_loop": "user_in_the_loop",
        }
    )

    graph_builder.set_finish_point("user_in_the_loop")

    # Runtime config
    unique_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": unique_id}}



    # Setup in-memory checkpointing
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
 
    # Initial state
    
    initial_state : testState = testState(
        messages=["job_posting", job_offer],
        job_description="We are looking for a junior data scientist with strong skills in Python, machine learning, and data visualization.",
        skills=["Python", "Machine Learning", "Data Visualization"],
        analysis_output=None,
        matching_skills=None,
        cover_letter_output=None,
        generation="",
        words_to_avoid=None,
        sentences_to_avoid=None,
        best_match_template_cover_letter=None,
        cv="Graduated in Data Science. 3 relevant projects completed in Python and scikit-learn.",
        agent_trace=[],
        editorial_violations=[],
        generation_violation_log={},
        iterations=0
    )

    # Execute and observe graph outputs
    print("\n------ STARTING COVER LETTER FLOW ------\n")
    output = graph.invoke(initial_state, config=config)
    print("Output state:")
    pprint(output)
    print("--------------------------------------------------")

    # # Visual debug (optional, works only in Jupyter/IPython)
    # try:
    #     from IPython.display import Image, display
    #     display(Image(graph_builder.get_graph(xray=True).draw_mermaid_png()))
    # except Exception as e:
    #     print(f"(Graph visualization skipped) Reason: {e}")



if __name__ == "__main__":
    build_master_graph(job_offer=job_description)

