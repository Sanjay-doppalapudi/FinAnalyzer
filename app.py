import streamlit as st
import PyPDF2
import io
import openai
from docx import Document
from typing import Any, List

def extract_text_from_file(uploaded_file: Any) -> str:
    """
    Extract text from uploaded file based on type.
    """
    file_name = uploaded_file.name.lower()
    text = ""
    uploaded_file.seek(0)  # Reset file pointer

    try:
        if file_name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file_name.endswith('.docx'):
            doc = Document(io.BytesIO(uploaded_file.read()))
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_name.endswith(('.md', '.txt')):
            text = uploaded_file.read().decode("utf-8")
        else:
            st.warning(f"Unsupported file type: {file_name}")
            return ""
    except Exception:
        st.error(f"Error extracting text from {file_name}")

    return text


def generate_suggestions(extracted_text: str) -> List[str]:
    """
    Generate 3 suggested questions using AI.
    """
    try:
        api_key = st.secrets["openrouter_api_key"]
    except KeyError:
        st.error("OpenRouter API key not found. Please set 'openrouter_api_key' in your Streamlit secrets.")
        return ["What are the key financial metrics?", "Summarize revenue trends.", "Analyze profitability."]

    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = "You are a Finance Analyzer AI. Generate exactly 3 relevant, random questions for analyzing the provided financial report text. Output as a numbered list: 1. Question one\n2. Question two\n3. Question three"

    try:
        response = client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Financial report text:\n{extracted_text[:2000]}"},  # Truncate for token limit
            ],
            max_tokens=1000,
        )
        content = response.choices[0].message.content
        if content is None:
            st.error("API response content is None in generate_suggestions")
            return ["What are the key financial metrics?", "Summarize revenue trends.", "Analyze profitability."]
        st.write(f"Debug: Content length: {len(content)}")  # Log for validation
        # Parse numbered list
        lines = [line.strip() for line in content.split('\n') if line.strip().startswith(('.', '1.', '2.', '3.'))]
        suggestions = [line.split('.', 1)[1].strip() if '.' in line else line.strip() for line in lines[:3]]
        return suggestions if len(suggestions) == 3 else ["What are the key financial metrics?", "Summarize revenue trends.", "Analyze profitability."]
    except Exception:
        return ["What are the key financial metrics?", "Summarize revenue trends.", "Analyze profitability."]


def set_query(question: str) -> None:
    st.session_state.query = question


def analyze_with_ai(extracted_text: str, query: str) -> str:
    """
    Analyze the extracted text using OpenRouter API.
    """
    try:
        api_key = st.secrets["openrouter_api_key"]
    except KeyError:
        return "Error: OpenRouter API key not found. Please set 'openrouter_api_key' in your Streamlit secrets."

    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = """You are a Finance Analyzer AI. Analyze the provided financial report text (multiple documents separated by <endofthefile>) and answer the user's query.

    Respond in raw, well-formatted Markdown without escaping syntax. Use **bold** for key figures (e.g., **Revenue: $1M**), *italic* for terms, | tables | for financial data (e.g., | Metric | Value |), and describe charts/graphs in text or simple markdown representations. Include newlines for readability. Do not use backticks or escapes for markdown; output pure markdown for proper rendering."""

    try:
        response = client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Financial report text:\n{extracted_text}\n\nUser query: {query}"},
            ],
            max_tokens=8000,
        )
        content = response.choices[0].message.content
        if content is None:
            st.error("API response content is None in analyze_with_ai")
            return "Error: No response from AI."
        st.write(f"Debug: Analysis content length: {len(content)}")  # Log for validation
        return content
    except Exception:
        return "Error in AI analysis."

# Streamlit app
st.title("Finance Analyzer AI")

# File uploader
uploaded_files = st.file_uploader("Upload financial reports (PDF, DOCX, MD, TXT) - up to 3 files", type=["pdf", "docx", "md", "txt"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 3:
        st.warning("Only the first 3 files will be processed.")
        uploaded_files = uploaded_files[:3]

    # Check if uploaded files have changed
    current_file_names = [f.name for f in uploaded_files]
    if current_file_names != st.session_state.get('uploaded_file_names', []):
        with st.spinner("Extracting text from files..."):
            combined_text = ""
            for i, file in enumerate(uploaded_files):
                text = extract_text_from_file(file)
                combined_text += text
                if i < len(uploaded_files) - 1:
                    combined_text += "<endofthefile>\n"
            st.session_state.combined_text = combined_text
            st.session_state.uploaded_file_names = current_file_names

    combined_text = st.session_state.get('combined_text', '')

    if combined_text:
        st.subheader("Extracted Text")
        st.text_area("Combined Extracted Content from all files", combined_text, height=300, disabled=True)

    extracted_text = combined_text  # For compatibility

    st.subheader("AI Analysis")

    if combined_text and 'suggestions' not in st.session_state:
        with st.spinner("Generating suggestions..."):
            st.session_state.suggestions = generate_suggestions(combined_text)

    if 'suggestions' in st.session_state:
        st.write("Suggested queries:")
        cols = st.columns(3)
        for i, suggestion in enumerate(st.session_state.suggestions):
            cols[i].button(suggestion, on_click=set_query, args=(suggestion,), key=f"sug_{i}")

    query = st.text_input("Enter your query", key='query')

    if st.button("Analyze"):
        if not query.strip():
            st.warning("Please enter a query to analyze.")
        else:
            with st.spinner("Analyzing with AI..."):
                analysis = analyze_with_ai(combined_text, query)
                st.session_state.analysis = analysis
    if 'analysis' in st.session_state:
        st.markdown("### Analysis Result")
        st.markdown(st.session_state.analysis)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Copy to Clipboard"):
                st.html(
                    f"""
                    <script>
                    navigator.clipboard.writeText(`{str(st.session_state.analysis).replace('`', '\\`')}`);
                    alert('Copied to clipboard!');
                    </script>
                    """
                )
        with col2:
            st.download_button(
                label="Export as MD",
                data=str(st.session_state.analysis),
                file_name="financial_analysis.md",
                mime="text/markdown"
            )
else:
    # Clear session state if no files uploaded
    if 'combined_text' in st.session_state:
        del st.session_state.combined_text
    if 'uploaded_file_names' in st.session_state:
        del st.session_state.uploaded_file_names
    combined_text = ""