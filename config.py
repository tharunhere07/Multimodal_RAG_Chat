"""
Configuration settings for the Multimodal RAG Application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configurations
GROQ_MODEL = "llama-3.3-70b-versatile"  # or "llama2-70b-4096"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Vector store settings
VECTOR_STORE_DIR = "./chroma_db"
COLLECTION_NAME = "multimodal_rag"

# File upload settings
UPLOAD_DIR = "./uploaded_files"
MAX_FILE_SIZE_MB = 200

# Supported file types
SUPPORTED_TEXT_FORMATS = [".txt", ".pdf", ".docx", ".doc", ".md"]
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".ogg"]
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv"]

# Create necessary directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

