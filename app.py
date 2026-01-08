"""
Streamlit App for Multimodal RAG Application
"""
import streamlit as st
import os
from pathlib import Path
import time
from typing import List

from document_processor import DocumentProcessor, get_file_type_category
from youtube_processor import YouTubeProcessor
from rag_engine import RAGEngine
from config import (
    UPLOAD_DIR, 
    SUPPORTED_TEXT_FORMATS, 
    SUPPORTED_IMAGE_FORMATS,
    SUPPORTED_AUDIO_FORMATS,
    SUPPORTED_VIDEO_FORMATS
)

# Page configuration
st.set_page_config(
    page_title="Multimodal RAG Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful chat interface
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Chat container */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* User message */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a1a;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* File uploader */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid transparent;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
        font-weight: 600;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: white;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'document_processor' not in st.session_state:
    st.session_state.document_processor = DocumentProcessor()

if 'uploaded_files_list' not in st.session_state:
    st.session_state.uploaded_files_list = []

# Main title
st.title("🤖 Multimodal RAG Chat Assistant")
st.markdown("### Powered by LlamaIndex, Groq & Streamlit")

# Sidebar
with st.sidebar:
    st.header("📚 Document Management")
    
    # Display stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", st.session_state.rag_engine.get_document_count())
    with col2:
        st.metric("Uploaded", len(st.session_state.uploaded_files_list))
    
    st.divider()
    
    # Create tabs for different upload types
    tab1, tab2 = st.tabs(["📁 Files", "🎥 YouTube"])
    
    with tab1:
        st.subheader("Upload Documents")
        
        # Show supported formats
        with st.expander("ℹ️ Supported Formats"):
            st.write("**Text Documents:**", ", ".join(SUPPORTED_TEXT_FORMATS))
            st.write("**Images:**", ", ".join(SUPPORTED_IMAGE_FORMATS))
            st.write("**Audio:**", ", ".join(SUPPORTED_AUDIO_FORMATS))
            st.write("**Video:**", ", ".join(SUPPORTED_VIDEO_FORMATS))
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=[ext[1:] for ext in SUPPORTED_TEXT_FORMATS + SUPPORTED_IMAGE_FORMATS + 
                  SUPPORTED_AUDIO_FORMATS + SUPPORTED_VIDEO_FORMATS]
        )
        
        if uploaded_files:
            if st.button("🚀 Process Files", use_container_width=True):
                with st.spinner("Processing files..."):
                    all_documents = []
                    
                    for uploaded_file in uploaded_files:
                        # Save file
                        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                        with open(file_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process file
                        try:
                            documents = st.session_state.document_processor.process_file(file_path)
                            all_documents.extend(documents)
                            st.session_state.uploaded_files_list.append({
                                'name': uploaded_file.name,
                                'type': get_file_type_category(file_path),
                                'size': uploaded_file.size
                            })
                            st.success(f"✅ Processed: {uploaded_file.name}")
                        except Exception as e:
                            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                    
                    # Add to RAG engine
                    if all_documents:
                        st.session_state.rag_engine.add_documents(all_documents)
                        st.success(f"🎉 Added {len(all_documents)} document chunks to the index!")
                        time.sleep(1)
                        st.rerun()
    
    with tab2:
        st.subheader("YouTube Videos")
        
        youtube_url = st.text_input(
            "Enter YouTube URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        if st.button("🎬 Process Video", use_container_width=True):
            if youtube_url:
                with st.spinner("Extracting transcript..."):
                    try:
                        documents = YouTubeProcessor.process_youtube_url(youtube_url)
                        st.session_state.rag_engine.add_documents(documents)
                        
                        # Add to uploaded list
                        video_id = YouTubeProcessor.extract_video_id(youtube_url)
                        st.session_state.uploaded_files_list.append({
                            'name': f"YouTube: {video_id}",
                            'type': 'youtube',
                            'size': 0
                        })
                        
                        st.success("✅ YouTube video processed successfully!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please enter a YouTube URL")
    
    st.divider()
    
    # Clear buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        if st.button("🔄 Clear Index", use_container_width=True):
            st.session_state.rag_engine.clear_index()
            st.session_state.uploaded_files_list = []
            st.success("Index cleared!")
            st.rerun()
    
    # Show uploaded files
    if st.session_state.uploaded_files_list:
        st.divider()
        st.subheader("📋 Uploaded Files")
        for idx, file_info in enumerate(st.session_state.uploaded_files_list[-5:]):  # Show last 5
            with st.expander(f"{file_info['name'][:30]}..."):
                st.write(f"**Type:** {file_info['type']}")
                if file_info['size'] > 0:
                    st.write(f"**Size:** {file_info['size'] / 1024:.2f} KB")

# Main chat interface
st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your documents..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from RAG engine
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_engine.query(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Rerun to update the chat
    st.rerun()

# Welcome message
if len(st.session_state.chat_history) == 0:
    st.info("""
    👋 **Welcome to Multimodal RAG Chat!**
    
    Get started by:
    1. Upload documents (PDF, DOCX, images, audio, video) using the sidebar
    2. Or add YouTube videos by pasting their URLs
    3. Ask questions about your content!
    
    The AI will analyze all your uploaded content and provide intelligent answers.
    """)
