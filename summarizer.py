import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from fpdf import FPDF
import streamlit as st

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def summarize(text):
    """Summarize text using Gemini."""
    prompt = f"""Summarize the following study material into clear, concise bullet points grouped by topic.
- Only include key concepts, definitions, and important facts
- Do not mention sources, authors, or where the content came from, and no 
- Use simple language a student can understand
- Group related points under short topic headings

Text:
{text}"""

    try:
        # Make sure there's actually text to summarize
        if not text or not text.strip():
            raise ValueError("No text to summarize")

        response = model.generate_content(prompt)

        # Make sure Gemini actually returned something
        if not response.text:
            raise ValueError("Gemini returned an empty response")

        return response.text.strip()

    except ValueError as e:
        st.error(f"Summarization failed: {e}")
        return ""
    except Exception as e:
        st.error(f"Something went wrong with summarization: {e}")
        return ""

def export_summary_pdf(summary_text):
    # Removes emojis so Helvetica font doesn't crash
    try:
        # Remove emojis so Helvetica font doesn't crash
        clean_text = re.sub(r'[^\x00-\x7F]+', ' ', summary_text)

        if not clean_text.strip():
            raise ValueError("No text to export")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.set_margins(15, 15, 15)
        pdf.multi_cell(0, 8, clean_text)
        return pdf.output()

    except ValueError as e:
        st.error(f"PDF export failed: {e}")
        return None
    except Exception as e:
        st.error(f"Something went wrong exporting PDF: {e}")
        return None