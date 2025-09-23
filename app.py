import streamlit as st
import PyPDF2
import io
import openai

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        # Read the uploaded file
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        
        # Extract text from each page
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error extracting text: {e}")
    
    return text


def generate_suggestions(extracted_text):
    """
    Generate 3 suggested questions using AI.
    """
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["openrouter_api_key"],
    )
    
    system_prompt = "You are a Finance Analyzer AI. Generate exactly 3 relevant, random questions for analyzing the provided financial report text. Output as a numbered list: 1. Question one\n2. Question two\n3. Question three"
    
    try:
        response = client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Financial report text:\n{extracted_text[:2000]}"},  # Truncate for token limit
            ],
            max_tokens=300,
        )
        content = response.choices[0].message.content
        # Parse numbered list
        lines = [line.strip() for line in content.split('\n') if line.strip().startswith(('.', '1.', '2.', '3.'))]
        suggestions = [line.split('.', 1)[1].strip() if '.' in line else line.strip() for line in lines[:3]]
        return suggestions if len(suggestions) == 3 else ["What are the key financial metrics?", "Summarize revenue trends.", "Analyze profitability."]
    except Exception as e:
        return ["What are the key financial metrics?", "Summarize revenue trends.", "Analyze profitability."]


def set_query(question):
    st.session_state.query = question
    st.rerun()


def analyze_with_ai(extracted_text, query):
    """
    Analyze the extracted text using OpenRouter API.
    """
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["openrouter_api_key"],
    )
    
    system_prompt = """You are a Finance Analyzer AI. Analyze the provided financial report text and answer the user's query.
    
    Respond in raw, well-formatted Markdown without escaping syntax. Use **bold** for key figures (e.g., **Revenue: $1M**), *italic* for terms, | tables | for financial data (e.g., | Metric | Value |), and describe charts/graphs in text or simple markdown representations. Include newlines for readability. Do not use backticks or escapes for markdown; output pure markdown for proper rendering."""
    
    try:
        response = client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Financial report text:\n{extracted_text}\n\nUser query: {query}"},
            ],
            max_tokens=2000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in AI analysis: {e}"

# Streamlit app
st.title("Finance Analyzer AI")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF financial report", type="pdf")

if uploaded_file is not None:
    if "extracted_text" not in st.session_state:
        with st.spinner("Extracting text from PDF..."):
            st.session_state.extracted_text = extract_text_from_pdf(uploaded_file)
    
    extracted_text = st.session_state.extracted_text
    
    with st.expander("View Extracted Text", expanded=False):
        st.text_area("Extracted Content", extracted_text, height=300, disabled=True)

    st.subheader("AI Analysis")
    
    if extracted_text and 'suggestions' not in st.session_state:
        with st.spinner("Generating suggestions..."):
            st.session_state.suggestions = generate_suggestions(extracted_text)
    
    if 'suggestions' in st.session_state:
        st.write("Suggested queries:")
        cols = st.columns(3)
        for i, suggestion in enumerate(st.session_state.suggestions):
            cols[i].button(suggestion, on_click=set_query, args=(suggestion,), key=f"sug_{i}")
    
    query = st.text_input("Enter your query", value=st.session_state.get('query', ''), key='query')
    
    if st.button("Analyze"):
        if not query.strip():
            st.warning("Please enter a query to analyze.")
        else:
            with st.spinner("Analyzing with AI..."):
                analysis = analyze_with_ai(extracted_text, query)
            
            st.markdown("### Analysis Result")
            st.markdown(analysis)