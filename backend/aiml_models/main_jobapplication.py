# backend/aiml_models/main_jobapplication.py

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from pprint import pprint
import uuid
import logging

## Internal imports
from utils import set_project_root


from common import get_llm_model

from graph_flow.graph_functions.node_graph_state import GraphState
from graph_flow.graph_functions.node_retrieve_cover_letters import retrieve_cover_letter
from graph_flow.graph_functions.node_generate_vacancy_analysis import generate_vacancy_analysis
from graph_flow.graph_functions.node_generate_cover_letter import generate_cover_letter
from graph_flow.graph_functions.node_context_validation import llm_validation
from graph_flow.graph_functions.node_initial_check import check_generation
from graph_flow.graph_functions.node_check_latex_syntax import check_latex_syntax
from graph_flow.graph_functions.node_create_latex_pdf import create_latex_pdf
from graph_flow.graph_functions.node_decide_to_continue import decide_to_continue
from graph_flow.graph_functions.node_decide_to_correct import decide_to_correct_context
from graph_flow.graph_functions.node_secondary_check import check_generation_secondary

# Call the function to set the project root and update the PYTHONPATH
ROOT = set_project_root()

do_not_use_words = [
    "abreast",
    "ardent",
    "cruisal",
    "deeply",
    "dvelve",
    "devising",
    "eager",
    "eagerly",
    "endeavors",
    "enthusiastic",
    "excited",
    "excel",
    "extensive",
    "extensively", 
    "expert",
    "expertise",
    "facets",
    "foster",
    "forefront",
    "fostering",
    "fueled",
    "fulfilling",
    "honed",
    "intricacies",
    "intricate",
    "meticulous ",
    "perfect",
    "perfectly",
    "prowess",
    "profoundly",
    "prospect",
    "realm",
    "seamlessly",
    "specialist",
    "stems",
    "strive",
    "striving",
    "superior",
    "superiority",
    "Tableau",
    "thrilled",
    "versed"
]

forbidden_sentences = [
    "I am a perfect fit for this role",
    "which is crucial",
    "crucial for this role",
    "perfectly aligned",
    "perfectly suited",
    "perfectly align",
    "which are essential for",
    "which are essential for this role",
    "mathematical modelin",
    "make me a suitable candidate for this role",
    "makes me a suitable candidate for this role",
    "make me a great fit for this role",
    "makes me a great fit for this role",
    "make me a strong fit for this position",
    "makes me a strong fit for this position",
    "make me a strong candidate for this role",
    "makes me a strong candidate for this role",
    "positions me well for this role",
    "invaluable in driving innovative AI solutions",
    "makes me a strong candidate for this role",
    "which will be valuable for the company's projects",
    "will be beneficial in delivering data driven solutions"
]

draft_skills = [
    "Business analytics",
    "Business maturity",
    "Strategy",
    "Non-technical and technical communication",
    "Algorithms & datastrucures",
    "Software Engineering",
    "detail oriented",
    "Creative thinker",
    "Problem solving",
    "Critical thinking",
    "Team player",
    "Time management",
    "Adaptability",
    "Conflict resolution",
    "Collaborative",
    "Dilligent",
    "Software development",
    "ITIL",
    "SAFe",
    "PRINCE2",
    "CMMI",
    "SCRUM",
    "Agile development",
    "UML(frequency, class or C4)",
    "Stakeholder classification",
    "Python intermediate level",
    "SQL working understanding",
    "R working understanding",
    "JavaScript working understanding",
    "Git",
    "Statistical modelling",
    "Fundamental Azure knowledge",
    "PostGres",
    "Neo4J",
    "Qdrant",
    "ANNOY",
    "Docker",
    "scraping",
    "crawling",
    "MT5",
    "Bert",
    "FinBert",
    "T5",
    "Scrapy",
    "Numpy",
    "Polars",
    "Pandas",
    "FastAPI",
    "VUE3",
    "TensorFlow2",
    "Huggingface",
    "Pytorch",
    "SonarCube",
    "Seaborn/matplotlib/Plotly",
    "PyTest",
    "SKlearn",
    "Unsupervised learning: dimensionality reduction, explorative factor analysis, K-mean..",
    "Supervised learning: Random Forests, multiple logistic regression, SVP, NNs, Classification",
]

some_job = """About the job
Are you ready to shape the future? 

Apply to our Tech Talent Program if you want to work with clients on solving their most challenging tech problems and accelerate your learning curve when applying your skills into practice. You will be part of a collaborate community of leaders and peers who are ready to mentor, coach and encourage you to be your best.

The Tech Talent Program is a two-year program, starting in March 2025, where you will receive tailored training together with other graduates, while working on one to three different projects being part of an Accenture team implementing business critical IT systems to our clients.

We are looking for passioned developers for the graduate program, who want to work in these areas and technologies:


Java, Java EE, Spring Framework, Python, C#, .NET, SQL / PLSQL, MySQL, 

Development using TDD, Clean Code, Continuous Integration and Continuous Delivery principles 

DevOps with Vagrant, Docker, Chef, Stomach, Git, Puppet and Jenkins 

Frontend development with HTML5, CSS3, REST, React.js, Angular.js, responsive design, and more 


At Accenture, we invest heavily in developing your professional skills. More than just a first step, we’re ready to help you turn your passion into an exciting career.

Four ways we’ll help you succeed and develop as a technical consultant:


 You’ll receive ongoing training that continuously extends your skills, allowing you to develop tailored expertise quickly.

 You’ll learn from day 1 as you’ll be part of projects where we implement complex technology for our international clients, transforming their business.

 During your graduate period, you’ll go through an intense learning process – with a buddy and people lead helping you figure out exactly how to develop your career. Want to be a specialist or a generalist? In Denmark or abroad? The sky is the limit.

 Opportunity to build your professional network across the organization by taking part in our communities or by joining our social events in the Graduate group, social gatherings at the office, company parties and not to forget our monthly Friday bar. We thrive to have fun at work!


What will my workday as a graduate consultant be like? 

Dependent on the client, the expectation is that you work from the client site four days a week, while at other projects you will have the possibility to work remotely from your home office or the Accenture office located in Carlsberg Byen in Copenhagen.

You will be an integral part of our projects and play a role – as you learn – in helping companies accelerate their enterprise transformation with innovative technology services to deliver lasting value. Depending on your skills and growth focus areas, you may:


Understand, design, and develop large IT solutions from a technical coding side or from the architectural side 

Work side by side with clients to understand and meet their needs 

Test advanced technology systems 

Configure standard solutions and build custom interfaces between systems 

Analyze and present complex data 

Work closely together with colleagues in our delivery centers in e.g., India, the Philippines and the Baltics throughout an implementation project 


Our client portfolio includes some of the biggest companies in Denmark across the financial sector, public sector, product industries, health industry, and resource industry. In your project you will be working with like-minded people on complex technological problems, applying the latest technology in Cloud, Security, Data, AI, Digital, Industry X, Enterprise platforms and Intelligent automation.

You’ll find yourself at the intersection of business and technology as you help our clients improve their performance and create sustainable value for their stakeholders while you grow expertise within a specific field.

We Hire For Passion And Train For Skills

What we are really looking for is a strong team player who is motivated by challenges and who is eager to learn and develop professionally. You are flexible in taking on new roles as you and your career develops and you take pride in delivering high quality on time while enjoying the ride together with your colleagues.

If that sounds like you, you will fit right in.

Furthermore, we imagine that you:


Are eager to develop your technical skills within IT development and the technologies mentioned above 

Have a good understanding of data structures and want to learn more about software architecture and data modelling 

Are finishing up your master’s degree in engineering, computer science or another discipline related to information technology – and can show us solid results from your studies 

Are fluent in English and preferably in Danish 


Ready to shape the future? 

Then submit your application no later than 11th of October 2024.

Please upload all the following documents in the CV/Resume section of the application process:


CV 

Cover Letter 

B.Sc., and M.Sc. grades 


Please note that applications without all the required documents will not be considered.


"""

def generate_cover_letter_wrapper(state: GraphState) -> GraphState:
    return generate_cover_letter(state, llm_model)


 # Update this node definition to pass the required arguments

def wrapped_validation_context_chain(state: GraphState) -> GraphState:
    return llm_validation(state, llm_model)

def graph_flow_extra_validation(job_offer: str, invalid_words: list[str], invalid_sentences: list[str]):
    # Initialize the graph
    work_flow = StateGraph(GraphState)
    # Define the nodes
    work_flow.add_node("retrieve_cover_letter", retrieve_cover_letter)
    work_flow.add_node("analyse_vacancy", generate_vacancy_analysis)
    work_flow.add_node("generate_application", generate_cover_letter_wrapper)
    work_flow.add_node("check_generation", check_generation)
    work_flow.add_node("check_generation_secondary", check_generation_secondary)
    work_flow.add_node("validation_context_chain", wrapped_validation_context_chain)
    work_flow.add_node("check_latex_syntax", check_latex_syntax)
    work_flow.add_node("create_latex_pdf", create_latex_pdf)

    # Build graph
    work_flow.set_entry_point("retrieve_cover_letter")
    work_flow.add_edge("retrieve_cover_letter", "analyse_vacancy")
    work_flow.add_edge("analyse_vacancy", "generate_application")
    work_flow.add_edge("generate_application", "check_generation")

    # First conditional edge: From check_generation to either generate_application or validation_context_chain
    work_flow.add_conditional_edges("check_generation", decide_to_continue,
        path_map={
            "generate_application": "generate_application",
            "validation_context_chain": "validation_context_chain",
        }
    )

    work_flow.add_edge("validation_context_chain", "check_generation_secondary")
    # Conditional edge from validation_context_chain to either check_generation or check_latex_syntax
    work_flow.add_conditional_edges("check_generation_secondary", decide_to_correct_context,
        path_map={
            "validation_context_chain": "validation_context_chain",  # Loop back to check_generation for further validation
            "check_latex_syntax": "check_latex_syntax",  # Proceed to the next step when conditions are met
        }
    )

    # Edge from check_latex_syntax to create_latex_pdf
    work_flow.add_edge("check_latex_syntax", "create_latex_pdf")

    # Set the finish point
    work_flow.set_finish_point("create_latex_pdf")

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

    # compile the graph
    graph = work_flow.compile(checkpointer=memory)

    

    initial_state = GraphState(
        error="",
        messages=['job_position', job_offer],
        generation="",
        iterations=0,
        context_iteration=0,
        final={},
        cover_letter_template="",
        words_to_avoid=invalid_words,
        sentences_to_avoid=invalid_sentences,
        unique_skills=draft_skills,
        cv=""
    )

    print("\n------------- INSIDE GRAPH FLOW -------------\n")

    # Pass all required arguments to validation_context_chain
    for output in graph.invoke(initial_state, config=config):
        print("------------- OUTPUT -------------")
        pprint(output)


if __name__ == "__main__":
    llm_model = get_llm_model()
    graph_flow_extra_validation(some_job, do_not_use_words, forbidden_sentences)
