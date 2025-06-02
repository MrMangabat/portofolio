# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/api/agent_main.py
# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/api/agent_main.py

from src.core.graph_master.master_graph_flow import build_master_graph
import json
from rich import print_json



def main() -> None:
    # Step 1: Build the full LangGraph
    graph = build_master_graph()

    # Step 2: Define sample job description input (simulate real frontend call)
    test_input = {
        "job_description": (
            "ATP is hiring a Data Scientist to join our Fraud Detection and AI Solutions team. "
            "The role requires knowledge of Python, SQL, and machine learning models for detecting anomalies in large datasets."
        )
    }

    # Step 3: Run the LangGraph
    result = graph.invoke(test_input)

    # Step 4: Output the structured result
    print("\n--- FINAL STRUCTURED OUTPUT ---\n")

    # print("company_name =", result["analysis_output"].company_name)
    # print()
    # print("job_title =", result["analysis_output"].job_title)
    # print()
    # print("analysis_output =", result["analysis_output"].analysis_output)
    # print()
    # print("employees_skills_requirement =", result["analysis_output"].employees_skills_requirement)
    # print()
    # print("matching_skills =", result["analysis_output"].matching_skills)
    # Convert to dict, then JSON pretty print
    analysis_result = result["analysis_output"]
    print_json(data=analysis_result.model_dump())
    print("\n-------------------------------\n")

if __name__ == "__main__":
    main()
