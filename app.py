import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Load environment variables first
load_dotenv()

# Set modern environment variables (replaces TRANSFORMERS_CACHE)
os.environ['HF_HOME'] = 'F:/huggingface_cache'
os.environ['HF_DATASETS_CACHE'] = 'F:/huggingface_cache/datasets'
os.environ['HF_MODULES_CACHE'] = 'F:/huggingface_cache/modules'

css = """
<style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
    }
</style>
"""

user_template = """
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
</div>
"""

bot_template = """
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
"""

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Handle None returns
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    return FAISS.from_texts(text_chunks, embeddings)

def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.5,
        max_output_tokens=2048,
        convert_system_message_to_human=True  # Add this line
    )
    
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True
    )

def handle_userinput(user_question):
    if not st.session_state.get('conversation'):
        st.error("Please upload and process the PDF files first.")
        return

    try:
        response = st.session_state.conversation.invoke({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error processing your request: {str(e)}")

def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("PDFs processed successfully!")
                except Exception as e:
                    st.error(f"Error processing PDFs: {str(e)}")

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    main()