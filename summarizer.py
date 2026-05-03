import os
import google.generativeai as genai
from dotenv import load_dotenv

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

    response = model.generate_content(prompt)
    return response.text.strip()