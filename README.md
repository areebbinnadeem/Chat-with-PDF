# 📚 PDFBot: AI-Powered Multi-Document Chat Assistant

PDFBot is a Streamlit-based AI assistant that allows users to chat with multiple PDF documents simultaneously. It leverages Google's **Gemini Pro** model and **FAISS** for efficient semantic search, enabling multi-turn contextual conversations over large volumes of text.

![PDFBotScreenshot](assets\pdfbot.PNG)

---

## 🚀 Features

- 🔍 Chat with multiple PDFs using natural language
- ⚡ Fast semantic search powered by **HuggingFace Embeddings** + **FAISS**
- 🧠 Context-aware, multi-turn conversation via memory-augmented chains
- 🔐 Environment-safe with `.env` support and secure API integration
- 🖥️ Clean and modern chat UI with Streamlit + custom HTML/CSS templates

---

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **LLM**: Google Gemini (via `langchain_google_genai`)
- **Embeddings**: `BAAI/bge-small-en-v1.5` (Hugging Face)
- **Vector Store**: FAISS
- **Utilities**: PyPDF2, dotenv, LangChain

---

## 📂 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/areebbinnadeem/Chat-with-PDF.git
   cd Chat-with-PDF

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt

3. **Set up your environment variables**
   Create a .env file and add your Gemini API Key:
   ```bash
   GEMINI_API_KEY=your_google_api_key_here

4. **Run the app**
   ```bash
   streamlit run app.py

