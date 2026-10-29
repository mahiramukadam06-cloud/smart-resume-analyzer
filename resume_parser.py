"""
resume_parser.py
-----------------
Handles reading resume files (PDF or DOCX) and converting them
into plain text so they can be analyzed.
"""

import os
from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file_path):
    """Read a PDF file and return all its text as one string."""
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(file_path):
    """Read a DOCX file and return all its text as one string."""
    text = ""
    doc = Document(file_path)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_resume_text(file_path):
    """
    Detect the file type from its extension and extract text
    using the correct method. Returns the extracted text as a string.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")


def clean_text(text):
    """Basic cleanup: lowercase, remove extra whitespace."""
    text = text.lower()
    text = " ".join(text.split())
    return text
