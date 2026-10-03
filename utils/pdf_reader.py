"""
Document ingestion and text extraction utilities.
Supports PDF, TXT, and DOCX files.
"""

import io
from typing import Tuple, Optional
import pypdf
import docx

def extract_text_from_file(uploaded_file) -> Tuple[bool, str, Optional[str]]:
    """
    Extract text from an uploaded Streamlit file object.
    
    Returns:
        (success: bool, text_or_error: str, filename: str)
    """
    if uploaded_file is None:
        return False, "No file uploaded.", None

    filename = uploaded_file.name
    lower_name = filename.lower()

    try:
        if lower_name.endswith(".pdf"):
            reader = pypdf.PdfReader(uploaded_file)
            extracted_pages = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(f"--- Page {i+1} ---\n" + page_text)
            full_text = "\n\n".join(extracted_pages).strip()
            if not full_text:
                return False, "The uploaded PDF appears to be empty or contains scanned images without selectable text.", filename
            return True, full_text, filename

        elif lower_name.endswith(".txt"):
            content_bytes = uploaded_file.read()
            # Try utf-8 first, fallback to latin-1
            try:
                full_text = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                full_text = content_bytes.decode("latin-1", errors="replace")
            return True, full_text.strip(), filename

        elif lower_name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            full_text = "\n\n".join(paragraphs).strip()
            if not full_text:
                return False, "The uploaded DOCX document contains no text.", filename
            return True, full_text, filename

        else:
            return False, "This file type is not supported. Please upload PDF, TXT, or DOCX.", filename

    except Exception as e:
        return False, f"Failed to read file: {str(e)}", filename
