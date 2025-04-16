import sys
from pathlib import Path

# 🚀 FORCE absolute path to `/src/`
current_file = Path(__file__).resolve()
src_directory = current_file.parent
backend_root = current_file.parents[3]  # Go up 3 levels to reach `/portofolio/`
src_path = backend_root / "backend" / "aiml_models" / "agent_teams" / "agent_tailored_cover_letter" / "src"

sys.path.append(str(src_path))

from langgraph.graph import StateGraph
from langgraph.graph.schema import create_state_type
from src.core.company_analysis.agent_service_class_company_analysis import AgentServiceClassCompanyAnalysis
from src.core.generation.agent_generate_cover_letter import GenerateCoverLetterAgent
from src.core.editorial.agent_editorial_validator import EditorialValidatorAgent
from src.infrastructure.correction_client import CorrectionsClient
from src.infrastructure.llm_client import LLMClient
from src.core.company_analysis.components.analysis_prompt_builder import AnalysisPromptBuilder
from src.core.company_analysis.components.analysis_respose_parser import JobAnalysisResultParser
from src.core.data_models.analysis_result_model import JobAnalysisResult

# Define shared LangGraph state
CoverLetterState = create_state_type("CoverLetterState", {
    "job_description": str,
    "analysis_output": JobAnalysisResult,
    "cover_letter_text": str,
    "editorial_notes": str,
    "final_pdf_path": str
})

def build_cover_letter_flow() -> StateGraph:
    corrections_client = CorrectionsClient()
    llm_client = LLMClient()

    company_analysis_agent = AgentServiceClassCompanyAnalysis(
        corrections_client=corrections_client,
        prompt_builder=AnalysisPromptBuilder(),
        response_parser=JobAnalysisResultParser(),
        llm_client=llm_client
    )

    cover_letter_generator = GenerateCoverLetterAgent()
    editorial_validator = EditorialValidatorAgent()

    graph = StateGraph(CoverLetterState)

    graph.add_node("analyse_vacancy", company_analysis_agent.analyze_job_vacancy)
    graph.add_node("generate_application", cover_letter_generator.generate_cover_letter)
    graph.add_node("editorial_agent", editorial_validator.validate_output)
    graph.add_node("create_pdf", lambda state: {**state, "final_pdf_path": "placeholder/path/final.pdf"})

    graph.set_entry_point("analyse_vacancy")
    graph.add_edge("analyse_vacancy", "generate_application")
    graph.add_edge("generate_application", "editorial_agent")
    graph.add_edge("editorial_agent", "create_pdf")
    graph.set_finish_point("create_pdf")

    return graph.compile()

job_description = """
Data Scientist til Fraud Detection & AI Solutions
Kan du dykke dybt i data? Har du styr på Machine Learning-modeller, SQL og Python? Og vil du arbejde med landets mest interessante datagrundlag? Så er du den Data Scientist, vi søger til afdelingen Fraud Detection & AI Solutions.
Vil du være med til at fremtidssikre velfærdssamfundet med teknologier som ML, NLP og Computer Vision?
I Digital Solutions får vi velfærden til at fungere. Vi spiller en afgørende rolle i digitaliseringen af det danske samfund, fordi vi står bag de systemer, der får to ud af tre velfærdskroner ud til danskerne. 
Her er vi lige nu på udkig efter en Data Scientist til afdelingen Fraud Detection & AI Solutions, hvor vi bl.a. sikrer en koordineret indsats i forhold til kontrol af fejludbetalinger og snyd med offentlige ydelser. 
Derudover spiller vi en vigtig rolle i arbejdet med effektivisering af forretningens processer ved brug af teknologier som Machine Learning, NLP, Computer vision og lignende teknologier. Siden sidste år har vi kortlagt et (kæmpe)stort NLP-potentiale på tværs af ATP, og nu arbejder vi på at udvikle og implementere løsningerne, så vi sikrer en effektiv udbetaling.
I jobbet som Data Scientist er det mere konkret dig, der: 
Forstår forretningens behov på tæt hold.
For at udvikle de bedste løsninger er det vigtigt at forstå forretningens behov. Derfor kommer du til at arbejde tæt sammen med forskellige teams for at afdække deres behov og omsætte dem til datadrevne løsninger.
Udvikler avancerede modeller i Python
Du er med til at udvikle statistiske modeller i Python, der er baseret på Machine Learning ved brug af både træningsdata og unsupervised metoder.
Vedligeholder og monitorerer vores modeller
For at sikre, at vores modeller fungerer optimalt, bliver du ansvarlig for løbende monitorering og vedligeholdelse. Her holder bl.a. øje med, hvorvidt modellerne opfører sig som forventet og tilpasser dem efter behov.
Er med fra udvikling til produktion
Vi arbejder med best practices fra softwareudvikling for at gøre overgangen fra udvikling til produktion så gnidningsfri som muligt. Du er derfor med til at sikre, at vores løsninger bringes sikkert fra udvikling til produktion i vores scrum-setup.
Udvikler og implementerer NLP-løsninger
Sidst, men ikke mindst, kommer du til at spille en central rolle i udviklingen af NLP-løsninger og sørger for, at de bliver produktionssat og taget i brug af vores interne kunder.
Har du styr på SQL og Python?
Der kan være flere veje til rollen som Data Scientist, men vi forestiller os, at du har en relevant kandidatgrad inden for matematik, statistik, fysik, computer science, ingeniørvidenskab eller lignende. Hvis du har et par års erfaring, er det en fordel.
Derudover er du:
erfaren når det kommer til dataanalyse og udvikling af Machine Learning-imodeller
en haj til Python, SQL og lignende (en fordel, ikke et krav)
med til at skabe resultater i samarbejde med andre
god til at finde enkle løsninger på komplekse udfordringer.
Vil du være en del af et unikt it-fagligt fællesskab?
I Fraud Detection & AI er vi en del af enheden Data i Digital Solutions. Vi brænder for data og de muligheder, data kan skabe. Som landets største udbetalingshus administrerer ATP to ud af tre velfærdskroner i Danmark. 
Vi arbejder med et unikt datagrundlag, som giver os særlige muligheder – både for at lave dybdegående analyser og for at udvikle datadrevne løsninger.
Du bliver en del af en afdeling med mere end 40 dygtige kolleger, der arbejder som Data Scientists, Software Developers, Data Analysts og forretningsansvarlige. Du kommer især til at arbejde tæt sammen med afdelingens dygtige tekniske specialister, som arbejder med Data Science og softwareudvikling i full-stack-løsninger. 
Vi arbejder i et fagligt stærkt miljø, hvor vi deler viden og hjælper hinanden med at udvikle os – både teknisk og personligt.
I ATP er barren sat højt, både når det gælder ambitioner og trivsel. Vi tror på et arbejdsliv i balance. Det kræver fleksibilitet med plads til den enkelte - og det har vi.
    """
def main() -> None:
    corrections_client = CorrectionsClient()
    llm_client = LLMClient()

    agent = AgentServiceClassCompanyAnalysis(
        corrections_client=corrections_client,
        prompt_builder=AnalysisPromptBuilder(),
        response_parser=JobAnalysisResultParser(),
        llm_client=llm_client
    )

    

    # try:
    final_result = agent.analyze_job_vacancy(job_description)
    print("\n✅ Final Analysis Result (JobAnalysisResult):")
    print(type(final_result))
    print(f"Company name: {final_result.company_name}\n")
    print(f"Job title; {final_result.job_title}\n")
    print(f"Analysis output; {final_result.analysis_output}\n")
    print(f"REQUIREMETNTS NEEDED; {final_result.employees_skills_requirement}\n")
    # except Exception as e:
    #     print(f"\n🚨 Analysis Process Failed: {e}")

if __name__ == "__main__":
    main()
