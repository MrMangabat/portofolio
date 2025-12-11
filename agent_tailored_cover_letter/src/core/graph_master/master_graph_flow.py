# /home/mangabat/projects/portofolio/backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/master_graph_flow.py
# This file builds the entire execution graph for the cover letter generation process/execution tree

# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/graph_master/master_graph_flow.py

"""quick hack, delete when the flow is stable"""
import sys
import os

# Add agent_tailored_cover_letter directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

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
import logging

# Configure logging to output INFO level to stdout with timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Node imports
from src.core.company_analysis.graph_nodes.node_generate_vacancy_analysis import generate_vacancy_analysis
from src.core.company_analysis.graph_nodes.node_get_data import node_get_data  # Unified data fetch (replaces get_skills + semantic_similarity)
from src.core.cover_letter.graph_nodes.node_generate_cover_letter import generate_cover_letter
from src.core.editorial.graph_nodes.node_audit_cover_letter import node_audit_cover_letter  # Editorial validation
from src.core.editorial.graph_nodes.node_reflection_cover_letter import node_reflection_cover_letter  # Surgical revision
from src.core.editorial.graph_nodes.node_user_in_the_loop import user_in_the_loop
from src.core.editorial.graph_nodes.node_decide_editorial_correction import decide_editorial_next_step
from agent_tailored_cover_letter.src.node_create_cover_letter_pdf import node_create_cover_letter_pdf  # PDF export

job_description = """

Job Description

Are you a student who dreams of a career in Management Consulting? Are you motivated by understanding complex business challenges and passionate about using technology to solve them? Do you want to work in the exciting cross-section between management consulting, AI & technology? If so, you might be our new Junior Consultant (Student Worker) we are looking for. 

About Us:

Devoteam is a leading international consultancy firm from Europe, specialized in technology-driven business transformation & AI, helping companies not just adapt, but lead.

For over 30 years, we've been helping clients around the world. Today, we have more than 11,000 employees across 25 countries. In Denmark alone, our team of 350 people supports a wide range of industries.

You'll join our Strategy team within Digital Impulse, our Management Consulting business unit. We are a team of Consultants passionate about helping clients navigate the digital landscape, from shaping their business strategy to designing innovative solutions. You will primarily be collaborating with other Consultants on the team during client projects, internal projects, and take part in our community of like-minded students working on various tasks.

This role is expected to be about 15 hours per week, and we will take exam periods into consideration.

If you want to learn more about life in Devoteam, meet Ida and learn about her story from Student Worker to Senior Consultant in Devoteam here.

What You’ll Do:

Client exposure - Work alongside experienced consultants on different client projects. This could include tasks like doing research, supporting data analysis, helping with deliverables, or preparing slides for client presentations. 
Business development - Contribute to project proposals and value propositions. You’ll have the chance to support the team in creating presentations and materials for new business opportunities. 
Workshop co-facilitation - Help prepare materials for client workshops. You may also get the chance to join and co-facilitate workshops, meet key stakeholders, and take part in discussions. 
Prototyping - Support the creation of low- and high fidelity prototypes. If you bring the right skills and motivation, you might even take the lead on certain parts of the development. 
Student community building - Be part of a community of fellow students, working together on different tasks within the business unit and sharing knowledge and experiences. 


What We Are Looking For:

Academic background - You are either in your last year of Bachelor's degree or your first year of Master's degree. Your studies are focused on a relevant area like Business Administration, Technology Management, Digital Management, or AI
Analytical skills - You can make sense of large amounts of information and turn it into clear insights or recommendations. 
Comfort with digital tools - You know your way around Microsoft Office and Google Suite, and you’re quick to pick up new tools and AI applications (such as ChatGPT, Gemini, or NotebookLM). 
Nice-to-have experience - it is a plus if you have previous experience with case competitions, problem-solving, or Agile & Design Thinking methodologies


To Succeed in This Role You have: 

Problem-solver mindset - You are excited by a challenge and are driven by the value you can create for clients by solving complex problems
Collaborative spirit - You thrive in a collaborative, team-oriented environment and are eager to take ownership of tasks
Proactive and curious - You have a strong interest in staying on top of the latest trends in AI, digital strategy, and business transformation
Effective communication - You can communicate clearly and effectively with colleagues and stakeholders, both in writing and verbally


What You Will Get:

This role is the perfect stepping stone to a consulting career.

Insights and experience from working on real client projects
Practical exposure to the Strategy & Digital Transformation field
Guidance and mentoring to support your development
Competitive salary to industry standard
A modern office in central Copenhagen (with flexibility to work from home)
A strong student community with support in daily tasks and fun social activities
The chance to explore new technologies and learn how to apply them in real-life solutions
Access to our canteen for lunch plus free snacks, coffee, and drinks throughout the day


Your CV and two reflection questions – No long cover letters!

To get to know you better, we have chosen to replace standard motivation letter with two short, reflective questions that you must answer in your application:

Question 1. Can you give an example of a situation where you stepped out of your comfort zone? What did you learn from it and what surprised you the most about the experience?
Question 2. Describe a time you were given a problem that felt unstructured or outside of your expertise. What did you do first, and what learnings would you bring into your future work?


Don’t worry if you don't meet every single requirement. We believe that skills can be taught, but passion and potential can't.

Our application process is designed to get to know both your personal and professional competencies. It includes relevant interviews with key stakeholders, providing you with an excellent opportunity to learn more about our team and culture.

There will typically be 2 interview rounds, which include a light 15-min 'on the spot' case or a 'take at home' case simulating a real-life client situation - allowing you to demonstrate your approach to problem-solving and toolbox.

If this sounds like your kind of place, let’s talk. Send us something - your CV, your best idea, some code, game illustration or even just a note on why this excites you. We don’t care about cover letter formalities - just show us how you think.

"""
from src.core.graph_master.initialize_graph import CoverLetterGraphState


def build_master_graph(job_offer: str) -> None:
    graph_builder = StateGraph(CoverLetterGraphState)

    # Register all graph nodes
    graph_builder.add_node("get_data", node_get_data)  # Unified data fetch (skills + corrections + semantic search + CV)
    graph_builder.add_node("analyse_vacancy", generate_vacancy_analysis)
    graph_builder.add_node("generate_cover_letter", generate_cover_letter)  # Initial generation only
    graph_builder.add_node("audit_cover_letter", node_audit_cover_letter)  # Editorial validation
    graph_builder.add_node("reflection_cover_letter", node_reflection_cover_letter)  # Surgical revision
    graph_builder.add_node("user_in_the_loop", user_in_the_loop)
    graph_builder.add_node("create_pdf", node_create_cover_letter_pdf)  # PDF export

    # Define graph flow
    graph_builder.set_entry_point("get_data")
    graph_builder.add_edge("get_data", "analyse_vacancy")
    graph_builder.add_edge("analyse_vacancy", "generate_cover_letter")
    graph_builder.add_edge("generate_cover_letter", "audit_cover_letter")

    # Conditional loop: audit → decide → (surgical revision OR proceed to human)
    graph_builder.add_conditional_edges(
        "audit_cover_letter",
        decide_editorial_next_step,
        path_map={
            "reflection_cover_letter": "reflection_cover_letter",  # Surgical revision
            "user_in_the_loop": "user_in_the_loop",  # Exit loop
        }
    )

    # After reflection, audit again
    graph_builder.add_edge("reflection_cover_letter", "audit_cover_letter")

    # After user approval, generate PDF
    graph_builder.add_edge("user_in_the_loop", "create_pdf")

    graph_builder.set_finish_point("create_pdf")

    # Runtime config
    unique_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": unique_id}}



    # Setup in-memory checkpointing
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
 
    # Initial state (using new CoverLetterGraphState with annotated accumulation)
    initial_state: CoverLetterGraphState = {
        "messages": [],
        "job_description": job_offer,
        "unique_user_input": "",  # User-specific notes for generation
        "skills": [],  # Populated by get_skills node
        "cv": "Graduated in Data Science. 3 relevant projects completed in Python and scikit-learn.",

        # Analysis outputs (populated by analyse_vacancy node)
        "matching_skills": None,
        "language_detected": "",



        # Semantic search & constraints
        "best_match_template_cover_letter": None,
        "words_to_avoid": [],
        "sentences_to_avoid": [],



        # Iteration control
        "iterations": 0,
        "max_iterations": 0,
    }

    # Execute and observe graph outputs
    logger.info("------ STARTING COVER LETTER FLOW ------")
    output = graph.invoke(initial_state, config=config)
    logger.info("Output state: %s", output)
    logger.info("--------------------------------------------------")

    # # Visual debug (optional, works only in Jupyter/IPython)
    # try:
    #     from IPython.display import Image, display
    #     display(Image(graph_builder.get_graph(xray=True).draw_mermaid_png()))
    # except Exception as e:
    #     print(f"(Graph visualization skipped) Reason: {e}")



if __name__ == "__main__":
    # from backend.services.service_cover_letter.src.event_broker.event_consumers.embedding_comsumer import start_consumer
    # from threading import Thread

    # Start consumer as a background thread (non-blocking)
    # Thread(target=start_consumer, daemon=True).start()

    build_master_graph(job_offer=job_description)

