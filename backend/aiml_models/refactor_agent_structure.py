import os
import shutil

BASE_DIR = os.path.abspath('agent_tailored_cover_letter')

FOLDER_STRUCTURE = [
    'src/api',
    'src/config',
    'src/core/cover_letter/graph',
    'src/core/company_analysis',
    'src/core/editorial',
    'src/core/supervisor',
    'src/infrastructure',
    'src/monitoring',
    'src/resources/prompts',
    'src/resources/templates/jobtemplates',
    'src/resources/templates/prompt_templates',
    'src/tests'
]

FILE_MOVES = {
    # API & Config
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/agent_api/agent_main.py': 'src/api/agent_main.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/agent_api/routes.py': 'src/api/cover_letter_routes.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/agent_api/agent_data_models.py': 'src/api/api_data_models.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/config_top_level/config.py': 'src/config/config.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/config_top_level/config.yaml': 'src/config/config.yaml',
    
    # LangGraph Nodes
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_check_latex_syntax.py': 'src/core/cover_letter/graph/node_check_latex_syntax.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_context_validation.py': 'src/core/cover_letter/graph/node_context_validation.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_create_latex_pdf.py': 'src/core/cover_letter/graph/node_create_latex_pdf.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_decide_to_continue.py': 'src/core/cover_letter/graph/node_decide_to_continue.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_decide_to_correct.py': 'src/core/cover_letter/graph/node_decide_to_correct.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_generate_cover_letter.py': 'src/core/cover_letter/graph/node_generate_cover_letter.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_generate_vacancy_analysis.py': 'src/core/cover_letter/graph/node_generate_vacancy_analysis.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_graph_state.py': 'src/core/cover_letter/graph/node_graph_state.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_initial_check.py': 'src/core/cover_letter/graph/node_initial_check.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_retrieve_cover_letters.py': 'src/core/cover_letter/graph/node_retrieve_cover_letters.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_secondary_check.py': 'src/core/cover_letter/graph/node_secondary_check.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/langgraph_flow_functions/node_semantic_control_loop.py': 'src/core/cover_letter/graph/node_semantic_control_loop.py',

    # Cover Letter Logic
    'backend/aiml_models/llm_agents/generate_cover_letter.py': 'src/core/cover_letter/cover_letter_generation.py',
    'backend/aiml_models/llm_agents/job_analysis.py': 'src/core/cover_letter/job_analysis.py',
    'backend/aiml_models/llm_agents/validation_chain.py': 'src/core/cover_letter/validation_chain.py',

    # Infrastructure
    'backend/aiml_models/llm_agents/LLM_model.py': 'src/infrastructure/llm_client.py',
    'backend/aiml_models/retrieve_documents/retrieve_cv.py': 'src/infrastructure/cv_loader.py',
    'backend/aiml_models/retrieve_documents/retrieve_templates.py': 'src/infrastructure/template_loader.py',

    # Monitoring
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/monitoring/error_handler.py': 'src/monitoring/error_handler.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/monitoring/event_tracking.py': 'src/monitoring/event_tracking.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/monitoring/logging_config.py': 'src/monitoring/logging_config.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/monitoring/model_monitor.py': 'src/monitoring/model_monitor.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/monitoring/observability.py': 'src/monitoring/observability.py',

    # Prompts
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/prompts/analyse_vacant_position_prompt.py': 'src/resources/prompts/analyse_vacant_position_prompt.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/prompts/generate_cover_letter_prompt.py': 'src/resources/prompts/generate_cover_letter_prompt.py',
    'backend/aiml_models/agent_teams/agent_tailored_cover_letter/prompts/sentence_word_validation_prompt.py': 'src/resources/prompts/sentence_word_validation_prompt.py'
}

def create_folders():
    for folder in FOLDER_STRUCTURE:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

def move_files():
    for src, dest in FILE_MOVES.items():
        src_path = os.path.abspath(src)
        dest_path = os.path.join(BASE_DIR, dest)

        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
        else:
            print(f"⚠️ Warning: {src_path} does not exist, skipping.")

def scaffold_supervisor():
    with open(os.path.join(BASE_DIR, 'src/core/supervisor/supervisor_graph.py'), 'w') as f:
        f.write("# Placeholder for Supervisor Graph combining all agents\n")

    with open(os.path.join(BASE_DIR, 'src/core/supervisor/supervisor_logic.py'), 'w') as f:
        f.write("# Placeholder for Supervisor Logic helpers\n")

if __name__ == "__main__":
    print(f"🚀 Creating new folder structure in: {BASE_DIR}")
    create_folders()

    print("📦 Moving files into correct locations...")
    move_files()

    print("🤖 Scaffolding supervisor logic...")
    scaffold_supervisor()

    print("✅ Migration complete! 🚀")
