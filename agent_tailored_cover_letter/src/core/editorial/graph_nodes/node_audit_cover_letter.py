# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_audit_cover_letter.py

from datetime import datetime
from typing import Dict, Any, List
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate

from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.data_models.editorial_model import EditorialResult
from src.infrastructure.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)


def node_audit_cover_letter(state: CoverLetterGraphState) -> Dict[str, Any]:
    """
    Editorial compliance node that validates generated cover letter against all rules.

    Purpose:
        Checks the generated cover letter for rule violations (grammar, tone, banned words,
        hallucinations, etc.) and returns structured violation reports.

    Capabilities:
        - Validates against 12 main rules + 8 language rules
        - Detects exact offending text spans for each violation
        - Logs violations with structured metadata (rule_id, section, error_type)
        - Tracks violations in editorial_violations for conditional routing

    Reasoning:
        Provides precise feedback for the editorial loop. The generate_cover_letter node
        uses this feedback in revision mode to fix specific issues.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    iteration = state.get("iterations", 0)

    logger.info("=" * 80)
    logger.info("NODE: node_audit_cover_letter - Starting editorial review")
    logger.info("Iteration: %s", iteration)
    logger.info("=" * 80)

    # 1️⃣ Setup parser
    parser = PydanticOutputParser(pydantic_object=EditorialResult)
    format_instructions: str = parser.get_format_instructions()

    # 2️⃣ Build prompt
    SYSTEM_TEMPLATE = """
        You are an editorial compliance specialist.
        Your sole purpose is to verify or repair a draft cover-letter so that it obeys every rule and language constraint below.
        You will be asked to extract the exact span of text that caused each violation. This will be used to improve future generations.

        Strict rules to follow:
        Rule 1: Get heavy inspiration from the following template provided by the jobseeker.
        Rule 2: The cover letter can only overlap a maximum of 30 percent with the jobseekers CV. This is to ensure that the cover letter is unique and not a copy of the CV and provide you with previous experiences of importance.
        Rule 3: Grammatical correctness is a MUST.
        Rule 4: English language is equal to EILTS C1 score
        Rule 5: The template job application must be in English in the job description is in English.
        Rule 6: Ensure all the information is relevant to the job description and the jobseeker's skills.
        Rule 7: Tone = personal (as in Rule 1) **and** casual-business professional.
        Rule 8: You are NOT allowed BY ANY MEANS to assume, infer, or generate any information about the jobseeker that is not present in:
            – the provided CV
            – their explicitly listed skills
            – the personal message
            If any claim appears that is unsupported by those, it must be flagged as a hallucination.

        Rule 9: Adhere and listen carefully to the jobseekers personal message. This is important to ensure that the cover letter is unique and not a copy of the CV.
        Rule 10: The jobseeker will provide a list of words, phrases or sentences that they do not want to be useed in the cover letter.
        Rule 11: The generated applications must be in the detected language of the job description. If the job description is in Danish, the cover letter must be in Danish. If the job description is in English, the cover letter must be in English.
        Rule 12: The output can NOT contain bullet points
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

        Users CV:
        {cv}

        Detected language of the job description:
        {language_detected}

        Personal message from the jobseeker:
        {personal_message}

        The jobseeker's skills are:
        {my_skills}

        YOUR TASKS AND OBJECTIVES:
        VALIDATION:
        Check the draft cover-letter against every Rule 1-12 and Language Rule 1-8.
        Reject or flag if lexical overlap with the CV exceeds 30 % → Rule 2 violation.
        Detect any banned words or sentences (Rule 10, Language Rule 7 & 8).
        Confirm the letter is written in the detected language **{language_detected}** (Rule 11).
        Verify IELTS C1-level grammar (Rule 3) and a "personal yet casual-business" tone (Rule 7).
        Ensure no invented facts about the jobseeker (Rule 8) and that all content is job-relevant (Rule 6).
        Ensure **no bullet-point formatting** ("-", "•", numbered lists, etc.) is present (Rule 12).

        VIOLATION LOGGING:
        For **every** breach create a `RuleViolation` object with:
        rule_id        – "Rule 3", "Language Rule 4", …
        section        – company_name | job_title | introduction | motivation | bulletpoint_1 | bulletpoint_2 | bulletpoint_3 | bulletpoint_4 | thank_you
        error_type – choose from:
        overlap | grammar | tone | invalid_phrase | hallucination | language | invalid_word
        offending_text – must be the **exact literal span** from the draft that caused the violation.
        - Include only the minimal clause, phrase, or sentence that violates the rule.
        - This will be used for debugging and regeneration — **precision is critical**.
        - Example: if the sentence is "I have expertise in Kubernetes and cloud infrastructure"
            and `expertise` is banned due to Rule 10, then offending_text = "I have expertise in Kubernetes and cloud infrastructure".
        explanation    – concise natural-language reason (≤ 50 words)

        The generated cover letter for audit is:
        {generated_cover_letter}

        {format_instructions}
    """

    audit_cover_letter_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=SYSTEM_TEMPLATE,
                input_variables=[
                    "job_position", "generated_cover_letter", "cv", "my_skills",
                    "analysis_output", "skills_match", "personal_message",
                    "not_wanted_words", "not_wanted_sentences", "language_detected"
                ],
                partial_variables={"format_instructions": format_instructions}
            )
        )
    ])

    # 3️⃣ Prepare inputs
    prompt_inputs = {
        "job_position": state.get("job_description", ""),
        "generated_cover_letter": state.get("cover_letter_output", ""),
        "cv": state.get("cv", ""),
        "my_skills": state.get("skills", []),
        "analysis_output": state.get("analysis_output", ""),
        "skills_match": state.get("matching_skills", {}),
        "personal_message": state.get("unique_user_input", ""),
        "not_wanted_words": state.get("words_to_avoid", []),
        "not_wanted_sentences": state.get("sentences_to_avoid", []),
        "language_detected": state.get("language_detected", ""),
    }

    logger.info("Starting editorial validation...")
    logger.info("  • Cover letter sections to check: %d", 9)  # company, title, intro, motiv, 4 bullets, thanks
    logger.info("  • Rules to validate: %d", 20)  # 12 main + 8 language

    # 4️⃣ Run LCEL chain
    llm = LLMClient().get_model("gpt")
    chain = audit_cover_letter_prompt | llm | parser
    result: EditorialResult = chain.invoke(prompt_inputs)

    logger.info("✓ Editorial validation complete")
    logger.info("  • Violations found: %d", len(result.violated_rules))

    if result.violated_rules:
        logger.warning("⚠️  VIOLATIONS DETECTED:")
        for idx, violation in enumerate(result.violated_rules, 1):
            logger.warning("  %d. [%s] %s in '%s': %s",
                          idx, violation.rule_id, violation.error_type,
                          violation.section, violation.explanation[:50])
    else:
        logger.info("✓ No violations found - cover letter passes all rules!")

    # 5️⃣ Build AIMessage
    violation_summary = "\n".join([
        f"  - [{v.rule_id}] {v.section}: {v.error_type} - {v.explanation[:50]}"
        for v in result.violated_rules
    ])
    updated_message = AIMessage(
        content=f"[EditorialAudit] Found {len(result.violated_rules)} violations:\n{violation_summary}"
    )

    # 6️⃣ Append messages
    updated_messages = state.get("messages", []) + [updated_message]

    # 7️⃣ Create new trace entry (auto-accumulated)
    new_trace = f"NODE: audit_cover_letter @ {timestamp}"
    logger.info("Adding trace: %s", new_trace)

    # 8️⃣ Update violation log for this iteration (auto-merged via add_to_dict)
    new_violation_log_entry = {
        f"iteration_{iteration}": {
            "timestamp": timestamp,
            "violations": [v.dict() for v in result.violated_rules],
            "violation_count": len(result.violated_rules),
        }
    }

    logger.info("=" * 80)
    logger.info("NODE: audit_cover_letter - Complete")
    logger.info("  • Total violations: %d", len(result.violated_rules))
    logger.info("  • Needs revision: %s", "YES" if result.violated_rules else "NO")
    logger.info("=" * 80)

    return {
        "messages": updated_messages,
        "agent_trace": [new_trace],
        "editorial_violations": [str(v) for v in result.violated_rules],  # For conditional routing
        "generation_violation_log": new_violation_log_entry,
    }
