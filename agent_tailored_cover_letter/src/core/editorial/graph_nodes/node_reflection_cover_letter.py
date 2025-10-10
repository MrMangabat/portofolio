# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_reflection_cover_letter.py

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


def node_reflection_cover_letter(state: CoverLetterGraphState) -> Dict[str, Any]:
    """
    Surgical revision node that updates only violated sections of the cover letter.

    Purpose:
        Performs targeted section-level revisions based on editorial violations,
        preserving unchanged sections for efficiency and consistency.

    Capabilities:
        - Extracts violated sections from editorial_violations
        - Generates replacement text only for flagged sections
        - Preserves original content for non-violated sections
        - Maintains full CoverLetterResult structure

    Reasoning:
        More efficient than full regeneration when only specific sections need fixes.
        Reduces LLM token usage and preserves quality of already-valid sections.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    iteration = state.get("iterations", 0)

    logger.info("=" * 80)
    logger.info("NODE: node_reflection_cover_letter - Starting surgical revision")
    logger.info("Iteration: %s", iteration)
    logger.info("=" * 80)

    # 1️⃣ Get current cover letter and violations
    current_cover_letter: Dict[str, Any] = state.get("cover_letter_output", {})
    violations_raw: List[str] = state.get("editorial_violations", [])
    violation_log: Dict[str, Any] = state.get("generation_violation_log", {})

    if not violations_raw:
        logger.info("⚠️  No violations to fix - skipping reflection")
        return {
            "agent_trace": [f"NODE: reflection_cover_letter @ {timestamp} - SKIPPED (no violations)"]
        }

    logger.info("Current cover letter sections:")
    for section, content in current_cover_letter.items():
        logger.info("  • %s: %d chars", section, len(str(content)) if content else 0)

    logger.info("Violations to address: %d", len(violations_raw))

    # 2️⃣ Extract violated sections from latest violation log
    latest_iteration_key = f"iteration_{iteration}"
    violated_sections = set()

    if latest_iteration_key in violation_log:
        for violation in violation_log[latest_iteration_key].get("violations", []):
            violated_sections.add(violation.get("section"))

    logger.info("Sections flagged for revision: %s", violated_sections)

    # 3️⃣ Setup parser
    parser = PydanticOutputParser(pydantic_object=CoverLetterResult)
    format_instructions = parser.get_format_instructions()

    # 4️⃣ Build surgical revision prompt
    SYSTEM_TEMPLATE = """
    You are performing targeted revision of a cover letter based on editorial feedback.

    Your task:
    - Review the violations listed below
    - Update ONLY the sections that were flagged
    - Preserve all other sections EXACTLY as they appear in the original
    - Ensure revised sections follow all 12 rules + 8 language rules

    Original cover letter:
    Company: {company_name}
    Job Title: {job_title}
    Introduction: {introduction}
    Motivation: {motivation}
    Bullet Point 1: {bulletpoint_1}
    Bullet Point 2: {bulletpoint_2}
    Bullet Point 3: {bulletpoint_3}
    Bullet Point 4: {bulletpoint_4}
    Thank You: {thank_you}

    Detected violations (flagged sections ONLY):
    {editorial_violations_log}

    Violated sections to revise: {violated_sections}

    User constraints:
    - Banned words: {not_wanted_words}
    - Banned sentences: {not_wanted_sentences}
    - Language: {language_detected}

    Job description (for context):
    {job_description}

    User's CV (for context):
    {cv}

    User's skills (for context):
    {my_skills}

    Analysis output (for context):
    {analysis_output}

    IMPORTANT RULES:
    - For sections NOT in the violated list, return the EXACT original text
    - For violated sections, apply the editorial feedback and rewrite
    - Maintain the same tone and style as the original
    - Do NOT add new information not present in CV/skills
    - Follow all language rules (no boilerplate, clichés, self-assessment, etc.)

    {format_instructions}
    """

    # 5️⃣ Build prompt
    reflection_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=SYSTEM_TEMPLATE,
                input_variables=[
                    "company_name", "job_title", "introduction", "motivation",
                    "bulletpoint_1", "bulletpoint_2", "bulletpoint_3", "bulletpoint_4",
                    "thank_you", "editorial_violations_log", "violated_sections",
                    "not_wanted_words", "not_wanted_sentences", "language_detected",
                    "job_description", "cv", "my_skills", "analysis_output"
                ],
                partial_variables={"format_instructions": format_instructions}
            )
        )
    ])

    # 6️⃣ Prepare inputs
    prompt_inputs = {
        "company_name": current_cover_letter.get("company_name", ""),
        "job_title": current_cover_letter.get("job_title", ""),
        "introduction": current_cover_letter.get("introduction", ""),
        "motivation": current_cover_letter.get("motivation", ""),
        "bulletpoint_1": current_cover_letter.get("bulletpoint_1", ""),
        "bulletpoint_2": current_cover_letter.get("bulletpoint_2", ""),
        "bulletpoint_3": current_cover_letter.get("bulletpoint_3", ""),
        "bulletpoint_4": current_cover_letter.get("bulletpoint_4", ""),
        "thank_you": current_cover_letter.get("thank_you", ""),
        "editorial_violations_log": violation_log.get(latest_iteration_key, {}),
        "violated_sections": ", ".join(violated_sections),
        "not_wanted_words": state.get("words_to_avoid", []),
        "not_wanted_sentences": state.get("sentences_to_avoid", []),
        "language_detected": state.get("language_detected", ""),
        "job_description": state.get("job_description", ""),
        "cv": state.get("cv", ""),
        "my_skills": state.get("skills", []),
        "analysis_output": state.get("analysis_output", ""),
    }

    logger.info("Surgical revision inputs prepared:")
    logger.info("  • Violated sections: %s", violated_sections)
    logger.info("  • Preserved sections: %s",
                set(current_cover_letter.keys()) - violated_sections)

    # 7️⃣ Run LCEL chain
    logger.info("Invoking LLM for surgical revision...")
    llm = LLMClient().get_model("gpt")
    chain = reflection_prompt | llm | parser
    result: CoverLetterResult = chain.invoke(prompt_inputs)

    logger.info("✓ Surgical revision complete")
    logger.info("  • Company: %s", result.company_name)
    logger.info("  • Job title: %s", result.job_title)

    # 8️⃣ Build AIMessage
    out = (
        f"Company: {result.company_name}\n"
        f"Job Title: {result.job_title}\n"
        f"Intro: {result.introduction}\n"
        f"Motivation: {result.motivation}\n"
        f"Bullet 1: {result.bulletpoint_1}\n"
        f"Bullet 2: {result.bulletpoint_2}\n"
        f"Bullet 3: {result.bulletpoint_3}\n"
        f"Bullet 4: {result.bulletpoint_4}\n"
        f"Thank you: {result.thank_you}"
    )
    updated_message = AIMessage(content=f"[ReflectionRevision]:\n{out}")

    # 9️⃣ Append messages
    filled_messages = reflection_prompt.invoke(prompt_inputs).messages
    updated_msgs: List[BaseMessage] = state.get("messages", []) + filled_messages + [updated_message]

    # 🔟 Add to revision history
    new_revision_entry = {
        "iteration": iteration,
        "timestamp": timestamp,
        "cover_letter": result.dict(),
        "revision_type": "surgical",
        "sections_revised": list(violated_sections),
    }

    # 1️⃣1️⃣ Trace update
    new_trace = f"NODE: reflection_cover_letter @ {timestamp} - Revised: {', '.join(violated_sections)}"
    logger.info("Adding trace: %s", new_trace)

    # 1️⃣2️⃣ Clear violations for next audit cycle
    logger.info("Clearing editorial_violations for next audit cycle")

    logger.info("=" * 80)
    logger.info("NODE: reflection_cover_letter - Complete")
    logger.info("  • Sections revised: %d", len(violated_sections))
    logger.info("  • Sections preserved: %d", len(current_cover_letter) - len(violated_sections))
    logger.info("=" * 80)

    return {
        "cover_letter_output": result.dict(),
        "generation": result,
        "messages": updated_msgs,
        "agent_trace": [new_trace],
        "cover_letter_revision_history": [new_revision_entry],
        "editorial_violations": [],  # Clear for next audit
    }
