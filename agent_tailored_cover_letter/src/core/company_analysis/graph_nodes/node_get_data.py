# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/company_analysis/graph_nodes/node_get_data.py

import logging
import json
import httpx
from typing import List, Dict, Optional, Literal
from datetime import datetime
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams

from src.config.service_settings import AgentSettings
from src.config.config_db_connections import QdrantConnection
from src.core.graph_master.initialize_graph import CoverLetterGraphState

logger = logging.getLogger(__name__)


def node_get_data(state: CoverLetterGraphState) -> Dict:
    """
    Unified data-fetch node for LangGraph flow.

    Purpose:
        Fetch user-defined word/sentence/skill corrections, semantic document from Qdrant,
        and placeholder CV content.

    Capabilities:
        - Calls corrections API for taboo words, overused sentences, and relevant skills
        - Performs semantic search in Qdrant using the job description as query
        - Returns a structured document and CV placeholder
        - Appends agent trace with timestamp

    Reasoning:
        Separated from LLM flow to isolate I/O-heavy preprocessing steps.
        All data dependencies loaded in one node to simplify graph flow.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    logger.info("=" * 80)
    logger.info("NODE: node_get_data - Starting unified data fetch")
    logger.info("Iteration: %s", state.get("iterations", 0))
    logger.info("=" * 80)

    # --- 1. Corrections API Fetch ---
    logger.info("Step 1: Fetching corrections from API...")
    settings = AgentSettings()
    corrections_url: str = f"http://{settings.CORRECTION_API_URL}/corrections"

    def fetch_texts(correction_type: Literal["word", "sentence", "skill"]) -> List[str]:
        logger.info("  Fetching corrections: type=%s, url=%s", correction_type, corrections_url)
        response = httpx.get(corrections_url, params={"correction_type": correction_type})
        response.raise_for_status()
        results = [item["text"] for item in response.json() if "text" in item]
        logger.info("  ✓ Fetched %d items for type '%s'", len(results), correction_type)
        return results

    words_to_avoid = fetch_texts("word")
    sentences_to_avoid = fetch_texts("sentence")
    skills = fetch_texts("skill")

    logger.info("Corrections loaded:\n%s", json.dumps({
        "words_to_avoid": words_to_avoid,
        "sentences_to_avoid": sentences_to_avoid,
        "skills": skills
    }, indent=2))

    # --- 2. Qdrant Semantic Search ---
    logger.info("Step 2: Performing semantic search in Qdrant...")

    embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    qdrant_connection = QdrantConnection()
    client: QdrantClient = qdrant_connection.client
    collection_name: str = qdrant_connection.default_collection

    job_description = state.get("job_description", "")
    logger.info("Encoding job description:\n%s", json.dumps({
        "job_description": job_description
    }, indent=2, ensure_ascii=False))

    vector: List[float] = embedding_model.encode(job_description, normalize_embeddings=False).tolist()
    logger.info("  Vector dimension: %d", len(vector))

    logger.info("  Querying Qdrant collection: %s", collection_name)
    search_results = client.query_points(
        collection_name=collection_name,
        query=vector,
        limit=1,
        with_payload=True,
        search_params=SearchParams(hnsw_ef=128)
    )

    # Extract best matching template
    best_match_template = None
    if search_results.points:
        best_match_template = search_results.points[0].payload.get('text', '')
        score = search_results.points[0].score if hasattr(search_results.points[0], 'score') else 'N/A'
        point_id = search_results.points[0].id
        logger.info("Found matching template:\n%s", json.dumps({
            "point_id": point_id,
            "score": score,
            "template_text": best_match_template,
            "payload_keys": list(search_results.points[0].payload.keys())
        }, indent=2))
    else:
        logger.warning("  ⚠ No matching templates found in Qdrant")

    # --- 3. CV Placeholder ---
    logger.info("Step 3: Loading CV content...")
    cv_text: str = """Profil
Jeg har en baggrund i Data Science og IT-økonomi og trives bedst dér, hvor analyse, teknologi, forretning og mennesket mødes. Min tilgang er praktisk og nysgerrig: Jeg finder noget spændende, dykker ned i teorien – og bygger eller tester det bagefter. Uanset om det handler om machine learning, automatisering, vektorbaseret søgning eller datastrukturer, arbejder jeg dedikeret og resultatorienteret med fokus på, hvad der også giver mening om 2–5 år.
Jeg nyder kompleksitet – især når det gælder, hvordan vi gør AI/ML-løsninger mere gennemsigtige og ansvarlige. Og når hjernen skal lufte ud, sker det gerne med kitesurfing, snowboard eller anden fysisk aktivitet.________________________________________
Uddannelse
MSc Data Science – ICT, Syddansk Universitet (2023)
•    Speciale: "A study of Natural Language Processing applied to market research"
o    Semiautomatisk PEST-analyse med vektorbaseret søgning og entity recognition
•    Fokus: Multivariat statistik, Applied Machine Learning,  Software Engineering, Visualisering

Professionsbachelor i Økonomi og IT, Erhvervsakademi Aarhus (2021)
•    Bachelorprojekt: "EnviroProcess Foundation of IT ", Enterprise Architecture as digital strategy
•    Frivilligt project: "Amazon's entry into the Danish market – e-commerce impact analysis"
•    Fokus: Strategi, digitalisering, finansiering, enterprise architecture og forretningsanalyse

International Butler Academy, 2018
European Bartender School, 2011
________________________________________
Erhvervserfaring
Projektleder (Kontrakt) – EnviroProcess Denmark A/S (2023 – 2024)
•    Ansvarlig for opførelse og montering af tekniske anlæg til svømmehal og wellness
•    Deltog selv i den praktiske udførelse på byggepladsen sammen med faggrupper
•    Koordinerede med byggeledelse, el- og VVS-installatører
•    Stod for kvalitetssikring, dokumentation og daglig fremdrift
Projektleder – EnviroProcess (2017 – 2021)
•    Ledelse af multidisciplinære teams og interessenthåndtering på tværs af interne og eksterne parter
•    Implementerede en hybrid Scrum-model til at styre opbygning og fremdrift af byggeriprojekter
•    Planlagde projektforløb med fokus på teknisk opbygning, dokumentation og klar overlevering til driftTest
Manager – TDC Hosting (2016 – 2017)
•    Identificerede applikationer med størst brugerbase og prioriterede disse for at minimere støj og sikre bred forankring
•    Indhentede opbakning fra superbrugere, slutbrugere og ledelse for at sikre accept og implementering
•    Koordinerede testforløb på tværs af Danmark, England og Indien og håndterede kulturelle forskelle i kommunikation og samarbejde
•    Øgede applikationsgodkendelser fra 17 % til 87 % ved at målrette indsatsen mod de mest kritiske systemer og stakeholders
Back Office Administrator – EnviroProcess (Periodeoverlap, støttefunktion)
________________________________________
Praktikophold
Business Process Improvement Intern – TDC Group (2019)
•    Gennemførte en value stream-analyse af driftsteknikeres arbejdsrutiner for at identificere spildtid og ineffektiv administration
o    Testede Windows-genveje og blindskrifttræning, hvilket reducerede pc-relateret opgavetid med 10–73 % for driftsteknikere
o    Foreslog en gamificeret læringsplatform som et lavomkostningsalternativ til eksisterende forslag – med potentiale til at øge produktiviteten bredt i organisationen
o    Estimerede forretningsværdi ved skalering på tværs af medarbejdere til 10–350 mio. DKK i potentiel årlig gevinst
SAP Integration Intern – Invixo Consulting (2019)
•    Arbejdede med SAP Integration Suite, SAP Datasphere og containerized provisioning agents
Data & Business Analyst Intern – Lemon Marketing & CC-Green (2024 – 2025)
•    Udarbejdede business cases med fokus på ROI, CAPEX og OPEX i konteksten af digital byggesagsbehandling
•    Opsatte og testede automatiseringsflows (Zapier, Make.com, Airtable) til udtræk af juridiske direktiver
•    Anvendte regex til mønstergenkendelse og eksperimenterede med extractive summarization af lovtekster
•    Strukturerede Airtable-database og forbehandlede data til integration i frontend
•    Foretog foranalyse af Azure-baseret backend-setup med vurdering af infrastruktur og skalerbarhed
________________________________________
Tidligere Roller (Udvalgte)
Mixologist & Duty Manager – KlarBar Cocktail Catering (2016 – 2021)
Planlægning og drift af cocktail-events, personaleansvar, indkøb og kundeoplevelse.
Mixologist – DiningSix, Scandic Hotels, Spring Street Social & Brooklyn Social (2015 – 2019)
Håndtering af driftsopgaver og cocktails i både casual og high-end bar- og restaurationsmiljøer.
________________________________________
Tekniske Kompetencer
Python, SQL, JavaScript (begynder), Docker, FastAPI, UML, PyTorch, TensorFlow, HuggingFace, Pandas, Polars, Numpy, Seaborn, SKlearn, Neo4j, Git, Regex, Azure Fundamentals
________________________________________
Sprog
Dansk (Native), Engelsk (C1)
________________________________________
Certificeringer
Microsoft Azure Fundamentals (2023)
"""
    logger.info("CV loaded:\n%s", json.dumps({
        "cv_text": cv_text
    }, indent=2, ensure_ascii=False))

    # --- Trace Update ---
    new_trace = f"NODE: node_get_data @ {timestamp}"
    logger.info("Adding trace: %s", new_trace)

    # --- Summary ---
    logger.info("=" * 80)
    logger.info("NODE: node_get_data - Data fetch complete")
    logger.info("State updates:\n%s", json.dumps({
        "skills": skills,
        "words_to_avoid": words_to_avoid,
        "sentences_to_avoid": sentences_to_avoid,
        "best_match_template_cover_letter": best_match_template if best_match_template else None,
        "cv": cv_text,
        "agent_trace": new_trace
    }, indent=2, ensure_ascii=False))
    logger.info("=" * 80)

    return {
        "skills": skills,
        "words_to_avoid": words_to_avoid,
        "sentences_to_avoid": sentences_to_avoid,
        "best_match_template_cover_letter": best_match_template,
        "cv": cv_text,
        "agent_trace": [new_trace],
    }
