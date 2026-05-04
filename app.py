import streamlit as st
from extractor import extract_text
import tempfile
import os
from summarizer import summarize, export_summary_pdf
from quiz_generator import generate_mcq_quiz

def load_css(file_path):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("styles.css not found - running without custom styles")

load_css("styles.css")

st.set_page_config(page_title="Memora", page_icon="📚", layout="wide")
st.title("📚 Memora")
st.subheader("Upload a file (pdf, docx, png, jpg, jpeg), and we'll summarize and quiz you!")

uploaded_file = st.file_uploader(
    "Upload a file",
    type=["pdf", "docx", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    # Temporarily save the file so extractor can read it
    extension = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Outputs a spinner with a temporary message while executing the block
    with st.spinner("Loading. Extracting the text..."):
        try:
            text = extract_text(tmp_path)

            # Make sure we actually got text back
            if not text or not text.strip():
                st.error("No text could be extracted from this file. Try a different file.")
            else:
                st.success("Text extracted successfully!")

                with st.expander("View extracted text"):
                    st.write(text)

                st.session_state["extracted_text"] = text


        except Exception as e:
            st.error(
                f"Could not extract text. If you uploaded an image, make sure it's a photo of handwritten/printed text — not a slide or diagram. Error: {e}")
        finally:
            # Always clean up the temp file even if something crashes
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

if "extracted_text" in st.session_state:
    if st.button("✨ Summarize"):
        with st.spinner("Summarizing... this may take a minute"):
            summary = summarize(st.session_state["extracted_text"])

            # Only save and display if summarization actually worked
            if summary:
                st.subheader("📝 Summary")
                st.write(summary)
                st.session_state["summary"] = summary
            else:
                st.error("Summarization returned empty. Try again.")

if "summary" in st.session_state:
    pdf_bytes = export_summary_pdf(st.session_state["summary"])

    # Only show download button if PDF was generated successfully
    if pdf_bytes:
        st.download_button(
            label="📄 Download Summary as PDF",
            data=bytes(pdf_bytes),
            file_name="summary.pdf",
            mime="application/pdf"
        )

if "summary" in st.session_state:
    st.divider()
    if st.button("📝 Generate Quiz"):
        with st.spinner("Generating quiz questions..."):
            questions = generate_mcq_quiz(st.session_state["summary"])

            # Only save if we actually got questions back
            if questions:
                st.session_state["questions"] = questions
            else:
                st.error("No questions were generated. Try again.")

if "questions" in st.session_state and st.session_state["questions"]:
    st.subheader("🧠 Quiz Time!")
    user_answers = {}

    for index, question in enumerate(st.session_state["questions"]):
        # Displays the question as a radio component and displays each response
        st.markdown(f"**Q{index + 1}: {question['question']}**")
        user_answers[index] = st.radio(
            f"Select answer for Q{index + 1}",
            options=list(question["options"].keys()),
            format_func=lambda option_letters, question_object=question: f"{option_letters}) {question_object['options'][option_letters]}",
            key=f"q_{index}",
            label_visibility="collapsed"
        )

    if st.button("Submit Quiz"):
        score = 0
        for index, question in enumerate(st.session_state["questions"]):
            # Verifies if the user chosen answer is correct
            correct = question["answer"]
            chosen = user_answers[index]
            if chosen == correct:
                st.success(f"Q{index + 1}: ✅ Correct!")
                score += 1
            else:
                st.error(f"Q{index + 1}: ❌ Wrong — Correct Answer: {correct}) {question['options'].get(correct, '')}")

        st.markdown(f"### 🎯 Score: {score}/{len(st.session_state['questions'])}")

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center;'>Made by Faris Zulfequar 👨‍💻</p>",
    unsafe_allow_html=True
)