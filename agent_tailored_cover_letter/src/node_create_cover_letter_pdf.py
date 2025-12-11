# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/output/graph_nodes/node_create_cover_letter_pdf.py

from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

from src.core.graph_master.initialize_graph import CoverLetterGraphState
from src.core.data_models.cover_letter_model import CoverLetterResult
import logging

logger = logging.getLogger(__name__)


def node_create_cover_letter_pdf(state: CoverLetterGraphState) -> Dict[str, Any]:
    """
    LangGraph node to generate a PDF document from the final cover letter.

    Purpose:
        Converts the structured cover letter output into a professionally formatted PDF.

    Capabilities:
        - Extracts cover letter data from state
        - Formats sections with proper styling (bold, spacing, bullets)
        - Saves PDF to outputs directory with company_jobTitle naming
        - Logs file creation and path

    Reasoning:
        Provides a portable, professional format for job applications.
        Should be called after user_in_the_loop approves the final version.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    iteration = state.get("iterations", 0)

    logger.info("=" * 80)
    logger.info("NODE: node_create_cover_letter_pdf - Starting PDF generation")
    logger.info("Iteration: %s", iteration)
    logger.info("=" * 80)

    # 1️⃣ Extract cover letter from state
    cover_letter_dict: Dict[str, Any] = state.get("cover_letter_output", {})

    if not cover_letter_dict:
        logger.warning("⚠️  No cover_letter_output found in state - skipping PDF generation")
        return {
            "agent_trace": [f"NODE: create_cover_letter_pdf @ {timestamp} - SKIPPED (no output)"]
        }

    # Convert dict to Pydantic model for type safety
    cover_letter = CoverLetterResult(**cover_letter_dict)

    logger.info("Cover letter data extracted:")
    logger.info("  • Company: %s", cover_letter.company_name)
    logger.info("  • Job Title: %s", cover_letter.job_title)

    # 2️⃣ Setup output directory and file path
    output_dir = Path(__file__).parent.parent.parent.parent / "outputs" / "pdfs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize filename (replace spaces and special chars)
    safe_company = cover_letter.company_name.replace(" ", "_").replace("/", "-")
    safe_job_title = cover_letter.job_title.replace(" ", "_").replace("/", "-")
    file_name = f"{safe_company}_{safe_job_title}.pdf"
    file_path = output_dir / file_name

    logger.info("  • Output path: %s", file_path)

    # 3️⃣ Create PDF document
    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=20,
        leftMargin=20,
        topMargin=30,
        bottomMargin=30
    )

    # 4️⃣ Define styles
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    bold = ParagraphStyle(
        name="Bold",
        parent=normal,
        fontName="Helvetica-Bold",
        spaceAfter=4
    )
    section_title = ParagraphStyle(
        name="SectionTitle",
        parent=bold,
        spaceBefore=8,
        spaceAfter=2
    )

    elements = []

    # 5️⃣ Build document content
    # Title: Company + Job Title
    title_line = f"<b>{cover_letter.company_name}, {cover_letter.job_title}</b>"
    elements.append(Paragraph(title_line, bold))
    elements.append(Spacer(1, 8))

    def add_section(label: str, content: str):
        """Helper to add a labeled section with content."""
        if content:
            return [
                Paragraph(f"{label}:", section_title),
                Paragraph(content, normal),
                Spacer(1, 6)
            ]
        return []

    # Add main sections
    elements += add_section("Introduction", cover_letter.introduction)
    elements += add_section("Motivation", cover_letter.motivation)
    elements += add_section("Unique Selling Points", cover_letter.unique_selling_points)

    # Add thank you section
    elements += add_section("Thank You", cover_letter.thank_you)

    # 7️⃣ Build the PDF
    logger.info("Building PDF document...")
    doc.build(elements)

    logger.info("✓ PDF generated successfully")
    logger.info("  • File size: %d bytes", file_path.stat().st_size)
    logger.info("  • Full path: %s", file_path.absolute())

    # 8️⃣ Update trace
    new_trace = f"NODE: create_cover_letter_pdf @ {timestamp} - PDF saved: {file_name}"
    logger.info("Adding trace: %s", new_trace)

    logger.info("=" * 80)
    logger.info("NODE: create_cover_letter_pdf - Complete")
    logger.info("=" * 80)

    return {
        "agent_trace": [new_trace],
        # Optionally store PDF path in state for downstream use
        # "pdf_output_path": str(file_path.absolute()),
    }
