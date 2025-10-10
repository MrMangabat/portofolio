# backend/aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/graph_nodes/node_generate_cover_letter.py

from datetime import datetime
from typing import Dict, Any, List
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate

from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.data_models.cover_letter_model import CoverLetterResult
from src.infrastructure.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


def generate_cover_letter(state: CoverLetterGraphState) -> Dict[str, Any]:
    """
    LangGraph node to generate a personalized cover letter (initial generation only).

    Purpose:
        Converts job insights, user CV, skills, and preferences into a formal cover letter using GPT.
        This node handles ONLY initial generation. Revisions are handled by node_reflection_cover_letter.

    Capabilities:
        - Loads format instructions via PydanticOutputParser
        - Enforces banned words/sentences
        - Logs detailed trace and appends AIMessage to conversation state
        - Returns structured CoverLetterResult

    Reasoning:
        Fully aligned with LCEL prompt-chain-parser style for transparency and retry handling.
        Separation of concerns: generation vs. surgical revision.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    iteration = state.get("iterations", 0)

    logger.info("=" * 80)
    logger.info("NODE: node_generate_cover_letter - Starting initial cover letter generation")
    logger.info("Iteration: %s", iteration)
    logger.info("=" * 80)

    # 1️⃣ Setup parser and instructions
    parser = PydanticOutputParser(pydantic_object=CoverLetterResult)
    format_instructions = parser.get_format_instructions()

    # 2️⃣ Initial generation prompt template
    logger.info("🆕 INITIAL GENERATION MODE: Creating cover letter from scratch")
    SYSTEM_TEMPLATE = """
        You are a professional writer, whos aim is to assist in writing cover letter for job seekers.
        For you to have a better understanding of the job, you will first get the job description, previous experiences and a analysis of the job description.

        Strict rules to follow:
        Rule 1: Get heavy inspiration from the following template provided by the jobseeker.
        Rule 2: The cover letter can only overlap a maximum of 30 percent with the jobseekers CV. This is to ensure that the cover letter is unique and not a copy of the CV and provide you with previous experiences of importance.
        Rule 3: Grammatical correctness is a MUST.
        Rule 4: English language is equal to EILTS C1 score
        Rule 5: The template job application must be in English in the job description is in English.
        Rule 6: Ensure all the information is relevant to the job description and the jobseeker's skills.
        Rule 7: The cover letter must be written in the personal tone, identified in Rule 1 while also being casual business professional.
        Rule 8: You are NOT allowed BY ANY MEANS to assume or generate any information about the jobseeker that is not provided in the CV, their skills or
        Rule 9: Adhere and listen carefully to the jobseekers personal message. This is important to ensure that the cover letter is unique and not a copy of the CV.
        Rule 10: The jobseeker will provide a list of words, phrases or sentences that they do not want to be useed in the cover letter.
        Rule 11: The generated applications must be in the detected language of the job description. If the job description is in Danish, the cover letter must be in Danish. If the job description is in English, the cover letter must be in English.
        Rule 12: The output can NOT be with bullet points
        All rules must be followed strictly and are of equal importance.

        Language constraints:
        Do not generate any phrasing that falls into these categories or resembles them in structure or meaning.
        You may not reword, restate, or soften the expressions — they are forbidden in all forms.

        Language Rule 1: Boilerplate expressions
        Overly generic phrases frequently used in job applications.

        Language Rule 2: Formulaic language
        Templated sentence structures that appear across many applications, lacking originality or nuance.

        Language Rule 3: Cliché phrases
        Overused expressions that have lost clarity, credibility, or sincerity.

        Language Rule 4: Self-assessing superlative claims
        Statements where the speaker makes a strong evaluative claim about themselves without external support.

        Language Rule 5: Empty or evaluative assertions
        Subjective statements of enthusiasm, confidence, or value that lack concrete evidence or action.

        Language Rule 6: Paraphrastic suitability claims
        Avoid paraphrastic variants or semantic equivalents of any statement that implies the jobseeker is a fit, match, or ideal candidate for the role, especially when based on traits, experience, or conclusions not externally supported.

        Language Rule 7: Banned terms (user-defined)
        The following specific words or expressions must be treated as violations of Rules 1–6 and are forbidden in any form:
        {not_wanted_words}

        Language Rule 8: Banned sentences (user-defined)
        The following full sentences — and any semantic paraphrases of them — are forbidden and must not appear in any generated output:
        {not_wanted_sentences}

        Detected language of the job description:
        {language_detected}

        Your task is to write a cover letter for the jobseeker based on the job description:
        {job_position}

        The previous analysis of the job description and the jobseeker's skills is as follows:
        {analysis_output}

        Important information about the jobseeker:
        {my_skills}

        The jobseeker's CV is as follows:
        {cv}

        Jobseeker template cover letter:
        {semilarity_jobtemplate}

        Personal message from the jobseeker:
        {personal_message}

        Introduction section:
        Write short and concise introduction of who the jobseeker is.

        Motivational section:
        Write it short and apply corrolated values between jobseeker and company internal and external values.
        Given the jobseekers previous experiences, professional and personal interests, provide value proportion to the company that the jobseeker can bring to the company.

        Bullet points section:
        Write a concise paragraph to introduce the bullet points.
        Write 3-4 bullet points with the following information - These bullet points can only be a raw string format:
        - The jobseeker's previous experiences and skills that are relevant to the job description.
        - The jobseeker's personal interests and how they relate to the job description.
        - The jobseeker's professional interests and how they add value to the company.
        - Continued learning.

        Thank you section:
        Write a short and concise thank you note to set up a coffee.

        {format_instructions}
        """

    # 3️⃣ Build prompt (initial generation only - no revision variables)
    cover_letter_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=SYSTEM_TEMPLATE,
                input_variables=[
                    "job_position", "cv", "my_skills", "analysis_output", "skills_match",
                    "semilarity_jobtemplate", "personal_message", "not_wanted_words",
                    "not_wanted_sentences", "language_detected"
                ],
                partial_variables={"format_instructions": format_instructions}
            )
        )
    ])

    # 4️⃣ Prepare input data (initial generation only)
    prompt_inputs = {
        "job_position": state.get("job_description", ""),
        "cv": state.get("cv", ""),
        "my_skills": state.get("skills", []),
        "analysis_output": state.get("analysis_output", ""),
        "skills_match": state.get("matching_skills", {}),
        "semilarity_jobtemplate": state.get("best_match_template_cover_letter", ""),
        "personal_message": state.get("unique_user_input", ""),
        "not_wanted_words": state.get("words_to_avoid", []),
        "not_wanted_sentences": state.get("sentences_to_avoid", []),
        "language_detected": state.get("language_detected", ""),
    }

    logger.info("Prompt inputs prepared:")
    logger.info("  • Job description length: %d chars", len(prompt_inputs["job_position"]))
    logger.info("  • CV length: %d chars", len(prompt_inputs["cv"]))
    logger.info("  • Skills count: %d", len(prompt_inputs["my_skills"]))
    logger.info("  • Language detected: %s", prompt_inputs["language_detected"])

    # 5️⃣ Run LCEL chain
    logger.info("Invoking LLM chain...")
    llm = LLMClient().get_model("gpt")
    chain = cover_letter_prompt | llm | parser
    result: CoverLetterResult = chain.invoke(prompt_inputs)

    logger.info("✓ Cover letter generated successfully")
    logger.info("  • Company: %s", result.company_name)
    logger.info("  • Job title: %s", result.job_title)
    logger.info("  • Introduction length: %d chars", len(result.introduction))
    logger.info("  • Motivation length: %d chars", len(result.motivation))

    # 6️⃣ Build AIMessage
    out = (
        f"Intro: {result.introduction}\n"
        f"Motivation: {result.motivation}\n"
        f"Bullet 1: {result.bulletpoint_1}\n"
        f"Bullet 2: {result.bulletpoint_2}\n"
        f"Bullet 3: {result.bulletpoint_3}\n"
        f"Bullet 4: {result.bulletpoint_4}\n"
        f"Thank you: {result.thank_you}"
    )
    updated_message = AIMessage(content=f"[CoverLetterGeneration]:\n{out}")

    # 7️⃣ Format messages for trace
    filled_messages = cover_letter_prompt.invoke(prompt_inputs).messages
    updated_msgs: List[BaseMessage] = state.get("messages", []) + filled_messages + [updated_message]

    # 8️⃣ Add to revision history (mark as initial generation)
    new_revision_entry = {
        "iteration": iteration,
        "timestamp": timestamp,
        "cover_letter": result.dict(),
        "revision_type": "initial",
    }

    # 9️⃣ Trace update
    new_trace = f"NODE: generate_cover_letter @ {timestamp} - Initial generation"
    logger.info("Adding trace: %s", new_trace)
    logger.info("=" * 80)
    logger.info("NODE: generate_cover_letter - Complete (Initial Generation)")
    logger.info("=" * 80)

    return {
        "cover_letter_output": result.dict(),
        "generation": result,
        "messages": updated_msgs,
        "agent_trace": [new_trace],
        "cover_letter_revision_history": [new_revision_entry],
    }
