from transformers import pipeline

# Load the model once (takes 30-60 seconds first time, downloads ~1.6GB)
summarizer = pipeline("text2text-generation", model="facebook/bart-large-cnn")

def chunk_text(text, max_chars=1000):
    """Split text into chunks so it fits within the model's token limit."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def summarize(text):
    """Summarize a long piece of text by chunking it first."""
    chunks = chunk_text(text)
    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summaries.append(result[0]["generated_text"])
    return " ".join(summaries)