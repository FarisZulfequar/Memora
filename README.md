# 📚 Memora

Memora is a student study tool that lets you upload your notes or textbook and automatically summarizes them and generates a quiz to test your knowledge.

## Try it out!

https://memora-d6yx7q2jhmqfu2rjm8djsw.streamlit.app/

## Features
- Supports PDF, Word docs, and handwritten notes (images)
- AI-powered summarization
- Auto-generated multiple choice quizzes
- Download your summary as a PDF

## Tech Stack
- Python
- Streamlit
- Google Gemini API
- pdfplumber, python-docx, pytesseract

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env`
4. Get a free Gemini API key at https://aistudio.google.com, paste it in `.env` as `GEMINI_API_KEY=your_key_here`
5. Activate your virtual environment: `source .venv/bin/activate`
6. Run: `streamlit run app.py`

Programmer: Faris Zulfequar
