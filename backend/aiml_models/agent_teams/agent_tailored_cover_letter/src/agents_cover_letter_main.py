import sys
from pathlib import Path

current_file = Path(__file__).resolve()
src_directory = current_file.parent
sys.path.append(str(src_directory))

from infrastructure.correction_client import CorrectionsClient
from infrastructure.llm_client import LLMClient
from core.company_analysis.agent_service_class_company_analysis import AgentServiceClassCompanyAnalysis
from core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from core.company_analysis.components.analysis_rules_validator import AnalysisRulesValidator


def main() -> None:
    corrections_client = CorrectionsClient()
    llm_client = LLMClient(model="llama3.2:3b")

    agent = AgentServiceClassCompanyAnalysis(
        corrections_client=corrections_client,
        prompt_builder=AnalysisPromptBuilder(),
        response_parser=JobAnalysisResultParser(),
        rules_validator=AnalysisRulesValidator(),
        llm_client=llm_client
    )

    job_description = """
    We are looking for a Data Scientist to join our team.
    The ideal candidate should have experience in Python, SQL, and Machine Learning.
    """

    # try:
    final_result = agent.analyze_job_vacancy(job_description)
    print("\n✅ Final Analysis Result (JobAnalysisResult):")
    print(final_result.model_dump_json(indent=2))
    # except Exception as e:
    #     print(f"\n🚨 Analysis Process Failed: {e}")

if __name__ == "__main__":
    main()
