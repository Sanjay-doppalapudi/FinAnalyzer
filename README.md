# 📊 Finance Analyzer AI

A modern web application built with Streamlit that allows users to upload financial report files (PDF, DOCX, MD, TXT – up to 3 files), extract text, and generate AI-powered summaries, analyses, or answers to custom queries. Powered by OpenRouter API for intelligent processing, it delivers formatted outputs with bold, italic, tables, and descriptive charts/graphs.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

## ✨ Features

- **Multi-File Upload**: Support for up to 3 files (PDF, DOCX, MD, TXT) financial reports, with automatic text extraction using PyPDF2 (PDF) and python-docx (DOCX).
- **AI Analysis**: Query the documents using OpenRouter API (Grok model) for summaries, key metrics, trends, or custom questions across multiple files.
- **Suggested Queries**: AI-generated 3 random, relevant questions to kickstart analysis.
- **Non-Finance Warning**: Dialog popup if uploaded content is not finance-related, with option to continue anyway.
- **Formatted Outputs**: Responses in rich Markdown – bold (**key figures**), *italic* terms, tables (| Metric | Value |), and text descriptions for charts/graphs.
- **Optional Text View**: Collapsible expander to view extracted text (combined with `<endofthefile>` separators for multi-doc awareness).
- **Export Options**: Copy analysis to clipboard or download as .md file.
- **Secure Configuration**: API key managed via Streamlit secrets (no hardcoding).

## 🛠 Tech Stack

- **Frontend/UI**: Streamlit (latest version)
- **File Processing**: PyPDF2 (PDF), python-docx (DOCX)
- **AI Integration**: OpenAI client for OpenRouter API
- **Data Handling**: Pandas (for potential table outputs)
- **Visualization**: Matplotlib (for chart descriptions via AI)
- **Secrets Management**: Streamlit's `st.secrets`

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd FinAnalyzer1.0
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure the OpenRouter API key:
   - Create `.streamlit/secrets.toml` in the project root (this file is gitignored):
     ```
     openrouter_api_key = "your-openrouter-api-key-here"
     ```
   - Obtain your free API key from [OpenRouter](https://openrouter.ai/) and replace the placeholder.

4. Run the app:
   ```
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`.

### Usage

1. **Upload Files**: Select up to 3 financial report files (PDF, DOCX, MD, TXT) via the uploader.
2. **View Extracted Text** (Optional): Expand "View Extracted Text" to see combined content (separated by `<endofthefile>` for multi-doc queries).
3. **AI Analysis**:
   - If content is not finance-related, a dialog warns you with a "Continue Anyway" button.
   - Use one of the 3 AI-suggested questions (buttons) to prefill the query input.
   - Or enter your own query (e.g., "Summarize revenue trends across documents").
   - Click "Analyze" to get a formatted response.
4. **Outputs**: View results with proper Markdown formatting – no raw syntax visible. Use "Copy to Clipboard" or "Export as MD" buttons.

**Note**: For multi-document analysis, the AI is prompted to consider all files separately using the separators.

## 📝 Configuration

- **API Key**: Stored securely in `.streamlit/secrets.toml`. Never commit this file to GitHub.
- **Model**: Defaults to "x-ai/grok-4-fast:free" (configurable in code if needed).
- **Limits**: Up to 3 files; text truncated for token limits in suggestions.

## 🔒 Security

- API key is not hardcoded; use `st.secrets` for local and deployed environments.
- `.gitignore` excludes `.streamlit/secrets.toml`, `venv/`, and other sensitive files.
- For deployment (e.g., Streamlit Community Cloud), paste secrets.toml contents into the app's "Secrets" settings.

## 🤝 Contributing

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing UI framework.
- [OpenRouter](https://openrouter.ai/) for AI API access.
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF handling.
- [python-docx](https://python-docx.readthedocs.io/) for DOCX handling.

---

**Built with ❤️ for financial analysis!** Questions? Open an issue.