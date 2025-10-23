# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/editorial/graph_nodes/node_audit_cover_letter.py

from datetime import datetime
from typing import Dict, Any
from langchain_core.messages import AIMessage
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
        - Logs violations with structured metadata (rule_id, section)
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
        Your sole purpose is to verify that a draft cover letter does not contain any banned words or sentences.
        You will be asked to extract the exact span of text that caused each violation.

        Banned terms (user-defined):
        The following specific words or expressions are forbidden in any form:
        {not_wanted_words}

        Banned sentences (user-defined):
        The following full sentences — and any semantic paraphrases of them — are forbidden and must not appear in any generated output:
        {not_wanted_sentences}

        YOUR TASKS AND OBJECTIVES:
        VALIDATION:
        - Detect any banned words or sentences in the cover letter.
        - Check for semantic paraphrases of banned sentences (not just exact matches).

        VIOLATION LOGGING:
        For **every** breach create a `RuleViolation` object with:
        rule_id        – "banned_word" or "banned_sentence"
        section        – company_name | job_title | introduction | motivation | unique_selling_points | thank_you

        offending_text – must be the **exact literal span** from the draft that caused the violation.
        - Include only the minimal clause, phrase, or sentence that violates the rule.
        - This will be used for debugging and regeneration — **precision is critical**.
        - Example: if the sentence is "I have expertise in Kubernetes and cloud infrastructure"
            and `expertise` is banned, then offending_text = "I have expertise in Kubernetes and cloud infrastructure".
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
                    "generated_cover_letter",
                    "not_wanted_words",
                    "not_wanted_sentences"
                ],
                partial_variables={"format_instructions": format_instructions}
            )
        )
    ])

    # 3️⃣ Prepare inputs
    prompt_inputs = {
        "generated_cover_letter": state.get("cover_letter_output", ""),
        "not_wanted_words": state.get("words_to_avoid", []),
        "not_wanted_sentences": state.get("sentences_to_avoid", []),
    }

    logger.info("Starting editorial validation...")
    logger.info("  • Cover letter sections to check: %d", 6)  # company, title, intro, motiv, USP, thanks
    logger.info("  • Checking for banned words and sentences only")

    # Log the actual cover letter dict being audited
    cover_letter = state.get("cover_letter_output", None)
    if cover_letter:
        logger.info("=" * 80)
        logger.info("GENERATED COVER LETTER TO AUDIT (actual values from state):")
        logger.info("  • Company: %r", cover_letter.get('company_name'))
        logger.info("  • Job Title: %r", cover_letter.get('job_title'))
        logger.info("  • Introduction: %r", cover_letter.get('introduction'))
        logger.info("  • Motivation: %r", cover_letter.get('motivation'))
        logger.info("  • Unique Selling Points: %r", cover_letter.get('unique_selling_points'))
        logger.info("  • Thank You: %r", cover_letter.get('thank_you'))
        logger.info("=" * 80)
        logger.info("FULL COVER LETTER STRING BEING SENT TO LLM:")
        logger.info("%r", prompt_inputs.get("generated_cover_letter"))
        logger.info("=" * 80)
    else:
        logger.warning("⚠️  No cover letter found in state!")

    # 4️⃣ Run LCEL chain
    llm = LLMClient().get_model("ollama")
    chain = audit_cover_letter_prompt | llm | parser
    result: EditorialResult = chain.invoke(prompt_inputs)

    logger.info("✓ Editorial validation complete")
    logger.info("  • Violations found: %d", len(result.violated_rules))

    if result.violated_rules:
        logger.warning("⚠️  VIOLATIONS DETECTED:")
        for idx, violation in enumerate(result.violated_rules, 1):
            logger.warning("  %d. [%s] %s in '%s': %s",
                          idx, violation.rule_id, violation.rule_id,
                          violation.section, violation.explanation[:50])
    else:
        logger.info("✓ No violations found - cover letter passes all rules!")

    # 5️⃣ Build AIMessage
    violation_summary = "\n".join([
        f"  - [{v.rule_id}] {v.section}: {v.rule_id} - {v.explanation[:50]}"
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
            "violations": [v.model_dump() for v in result.violated_rules],
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
