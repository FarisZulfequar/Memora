import docx
import pdfplumber
from PIL import Image
import pytesseract


def extract_from_pdf(file_path):
    """Extract text from PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_from_docx(file_path):
    """Extract text from a Word document."""
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    return text.strip()

def extract_from_image(file_path):
    """Extract text from a handwritten/printed image using OCR."""
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text.strip()