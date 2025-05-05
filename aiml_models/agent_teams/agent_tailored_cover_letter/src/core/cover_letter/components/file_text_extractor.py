# aiml_models/agent_teams/agent_tailored_cover_letter/src/core/cover_letter/components/file_text_extractor.py
from typing import Optional
from io import BytesIO
from PyPDF2 import PdfReader
import docx

from typing import Optional
from io import BytesIO
from PyPDF2 import PdfReader
import docx

class FileTextExtractor:
    """
    Purpose:
        Handles extraction of clean text from uploaded PDF and DOCX files.
    
    Capabilities:
        - Extracts text using PyPDF2 (default).
        - Placeholder for future docling2 PDF extraction support.
        - Extracts text from Word (.docx) files using python-docx.
    
    Reasoning:
        Allows swapping between fast-but-dirty (PyPDF2) and future accurate NLP-based (docling2) extraction.
    """

    @staticmethod
    def extract_text(file_stream: BytesIO, filename: str, method: str = "pypdf2") -> Optional[str]:
        """
        Extracts text from supported files.

        Args:
            file_stream (BytesIO): Raw stream of the uploaded file.
            filename (str): Name of the file to infer type.
            method (str): Extraction backend ("pypdf2" or "docling").

        Returns:
            Optional[str]: Cleaned plain text or None.
        """
        if filename.lower().endswith(".pdf"):
            if method == "pypdf2":
                return FileTextExtractor._extract_pdf_text_pypdf2(file_stream)
            elif method == "docling":
                return FileTextExtractor._extract_pdf_text_docling(file_stream)
            else:
                print(f"Unsupported PDF extraction method: {method}")
                return None

        elif filename.lower().endswith(".docx"):
            return FileTextExtractor._extract_docx_text(file_stream)

        else:
            print(f"Unsupported file format: {filename}")
            return None

    @staticmethod
    def _extract_pdf_text_pypdf2(file_stream: BytesIO) -> Optional[str]:
        try:
            reader = PdfReader(file_stream)
            return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        except Exception as e:
            print(f"[PyPDF2] PDF extraction failed: {e}")
            return None

    @staticmethod
    def _extract_pdf_text_docling(file_stream: BytesIO) -> Optional[str]:
        """
        Placeholder for future use of docling2 (or similar) to extract structured PDF content.
        """
        print("[DOC2] PDF extraction method is not yet implemented.")
        return None  # Replace with actual logic later

    @staticmethod
    def _extract_docx_text(file_stream: BytesIO) -> Optional[str]:
        try:
            doc = docx.Document(file_stream)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            print(f"DOCX extraction failed: {e}")
            return None
