import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def generate_mcq_quiz(summary, num_questions=5):
    """Generate quiz questions from a summary using Gemini."""

    prompt = f"""Based on this text, generate {num_questions} multiple choice questions.

Return ONLY a JSON array, no other text, in this exact format:
[
  {{
    "question": "question text here",
    "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
    "answer": "A"
  }}
]

Text: {summary}"""

    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if Gemini adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    questions = json.loads(raw)
    return questions