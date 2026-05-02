import streamlit as st
from extractor import extract_text
import tempfile
import os

st.set_page_config(page_title="Study Buddy", page_icon="📚", layout="wide")

st.title("📚 Study Buddy")
st.subheader("Upload various of files (pdf, docx, png, jpg, jpeg), and we'll summarize and quiz you!")

uploaded_file = st.file_uploader(
    "Upload a file",
    type=["pdf", "docx", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    # Temporarily save the file so extractor can read it
    fileextension = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=fileextension) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Loading. Extracting the text"):
        try:
            text = extract_text(tmp_path)
            st.success("Text extracted went good")

            with st.expander("View extracted text"):
                st.write(text)

            st.session_state["extracted_text"] = text


        except Exception as e:
            st.error(f"Something went wrong with the extraction: {e}")

        finally:
            os.unlink(tmp_path)  # Clean up temp file

if "extracted_text" in st.session_state:
    if st.button("✨ Summarize"):
        with st.spinner("Summarizing... this may take a minute"):
            from summarizer import summarize
            summary = summarize(st.session_state["extracted_text"])
            st.subheader("📝 Summary")
            st.write(summary)
            st.session_state["summary"] = summary

if "summary" in st.session_state:
    st.divider()
    if st.button("🧠 Generate Quiz"):
        with st.spinner("Generating quiz questions..."):
            from quiz_generator import generate_mcq_quiz
            questions = generate_mcq_quiz(st.session_state["summary"])
            st.session_state["questions"] = questions

if "questions" in st.session_state:
    st.subheader("🧠 Quiz Time!")
    user_answers = {}

    for i, q in enumerate(st.session_state["questions"]):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        user_answers[i] = st.radio(
            f"Select answer for Q{i+1}",
            options=list(q["options"].keys()),
            format_func=lambda x, q=q: f"{x}) {q['options'][x]}",
            key=f"q_{i}",
            label_visibility="collapsed"
        )

    if st.button("✅ Submit Quiz"):
        score = 0
        for i, q in enumerate(st.session_state["questions"]):
            correct = q["answer"]
            chosen = user_answers[i]
            if chosen == correct:
                st.success(f"Q{i+1}: ✅ Correct!")
                score += 1
            else:
                st.error(f"Q{i+1}: ❌ Wrong — correct answer was **{correct}) {q['options'].get(correct, '')}**")

        st.markdown(f"### 🎯 Score: {score}/{len(st.session_state['questions'])}")