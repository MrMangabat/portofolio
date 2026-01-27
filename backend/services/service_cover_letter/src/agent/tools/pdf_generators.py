"""PDF generation helper functions.

Note: This is a placeholder implementation. The actual PDF generation
functions need to be implemented or imported from the original cv_resume_builder
tools module.
"""

import logging
import os

logger = logging.getLogger(__name__)


def generate_pdf(application_data: dict, company_name: str, output_name: str) -> str:
    """Generate cover letter PDF directly from application data dict.

    Args:
        application_data: Complete application data dictionary
        company_name: Company name (used for subfolder)
        output_name: Base name for output file (without extension)

    Returns:
        str: Path to generated PDF file
    """
    # Base directory for PDFs
    base_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "pdf", "not_applied_yet"
    )

    # Sanitize company name for folder
    company_folder = "".join(
        c if c.isalnum() or c in (" ", "-", "_") else "_" for c in company_name
    )
    company_folder = company_folder.strip().replace(" ", "_").lower()

    # Create company folder if it doesn't exist
    output_dir = os.path.join(base_dir, company_folder)
    os.makedirs(output_dir, exist_ok=True)

    # Full path for PDF
    pdf_path = os.path.join(output_dir, f"{output_name}.pdf")

    # TODO: Implement actual PDF generation
    # For now, save the application data as JSON for debugging
    import json

    json_path = os.path.join(output_dir, f"{output_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(application_data, f, indent=2, ensure_ascii=False)

    logger.info("Generated placeholder PDF data: %s", json_path)

    # Return the intended PDF path (even though we only created JSON for now)
    return pdf_path


def generate_cv_pdf_helper(cv_data: dict, company_name: str, output_name: str) -> str:
    """Generate CV PDF directly from data dict.

    Args:
        cv_data: Complete CV data dictionary (from master_data.json structure)
        company_name: Company name (used for subfolder)
        output_name: Base name for output file (without extension)

    Returns:
        str: Path to generated PDF file
    """
    # Base directory for PDFs
    base_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "pdf", "not_applied_yet"
    )

    # Sanitize company name for folder
    company_folder = "".join(
        c if c.isalnum() or c in (" ", "-", "_") else "_" for c in company_name
    )
    company_folder = company_folder.strip().replace(" ", "_").lower()

    # Create company folder if it doesn't exist
    output_dir = os.path.join(base_dir, company_folder)
    os.makedirs(output_dir, exist_ok=True)

    # Full path for PDF
    pdf_path = os.path.join(output_dir, f"{output_name}.pdf")

    # TODO: Implement actual CV PDF generation
    # For now, save the CV data as JSON for debugging
    import json

    json_path = os.path.join(output_dir, f"{output_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cv_data, f, indent=2, ensure_ascii=False)

    logger.info("Generated placeholder CV PDF data: %s", json_path)

    # Return the intended PDF path (even though we only created JSON for now)
    return pdf_path
