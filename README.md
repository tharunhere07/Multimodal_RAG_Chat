# 🤖 Multimodal RAG Chat Application

A comprehensive end-to-end **Retrieval-Augmented Generation (RAG)** application that supports multiple file types and YouTube videos, built with **LlamaIndex**, **Groq LLM**, and **Streamlit**.

## ✨ Features

- 📄 **Multi-format Document Support**: PDF, DOCX, TXT, Markdown
- 🖼️ **Image Processing**: JPG, PNG, GIF, BMP (with OCR)
- 🎵 **Audio Processing**: MP3, WAV, M4A, OGG (with speech recognition)
- 🎥 **Video Processing**: MP4, AVI, MOV, MKV (extracts audio transcripts)
- 📺 **YouTube Integration**: Extract and process YouTube video transcripts
- 💬 **Beautiful Chat Interface**: Modern, gradient-styled UI
- 🚀 **Powered by Groq**: Fast inference with Mixtral/LLaMA models
- 🔍 **Vector Search**: ChromaDB for efficient document retrieval
- 🧠 **Smart Embeddings**: HuggingFace BGE embeddings

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Tesseract OCR (for image processing)
- FFmpeg (for audio/video processing)

### Installing Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### Installing FFmpeg

**Windows:**
1. Download from: https://ffmpeg.org/download.html
2. Extract and add to PATH

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

## 🔑 Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/

## 🚀 Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. **Upload Documents**:
   - Use the sidebar to upload files or add YouTube URLs
   - Click "Process Files" or "Process Video"
   - Wait for documents to be indexed

4. **Ask Questions**:
   - Type your questions in the chat input
   - Get AI-powered answers based on your documents

## 📁 Project Structure

```
mm2/
├── app.py                  # Main Streamlit application
├── rag_engine.py          # RAG implementation with LlamaIndex
├── document_processor.py  # Multi-format document processing
├── youtube_processor.py   # YouTube video processing
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
├── uploaded_files/      # Uploaded files directory (created automatically)
└── chroma_db/          # Vector store database (created automatically)
```

## 🎨 Supported File Types

| Category | Formats | Processing Method |
|----------|---------|-------------------|
| **Text** | .txt, .pdf, .docx, .md | Direct text extraction |
| **Images** | .jpg, .png, .gif, .bmp | OCR (Tesseract) |
| **Audio** | .mp3, .wav, .m4a, .ogg | Speech Recognition |
| **Video** | .mp4, .avi, .mov, .mkv | Audio extraction + Speech Recognition |
| **YouTube** | YouTube URLs | Transcript API |

## 🧩 How It Works

1. **Document Processing**:
   - Files are uploaded and processed based on their type
   - Text is extracted using appropriate methods (OCR, speech recognition, etc.)
   - Content is converted to LlamaIndex Documents

2. **Indexing**:
   - Documents are split into chunks
   - Embeddings are generated using HuggingFace models
   - Vectors are stored in ChromaDB

3. **Querying**:
   - User questions are embedded
   - Similar document chunks are retrieved
   - Groq LLM generates contextual answers

## 🔧 Customization

### Change LLM Model

Edit `config.py`:
```python
GROQ_MODEL = "llama2-70b-4096"  # or "mixtral-8x7b-32768"
```

### Change Embedding Model

Edit `config.py`:
```python
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"  # or other HuggingFace models
```

### Adjust Chunk Size

Edit `rag_engine.py`:
```python
Settings.chunk_size = 512
Settings.chunk_overlap = 50
```

## 🐛 Troubleshooting

**Issue**: Tesseract not found
- Ensure Tesseract is installed and added to PATH
- Restart terminal/IDE after installation

**Issue**: FFmpeg errors
- Verify FFmpeg installation: `ffmpeg -version`
- Check PATH configuration

**Issue**: Speech recognition fails
- Requires internet connection for Google Speech Recognition API
- Audio files must be clear and in supported formats

**Issue**: YouTube transcript not available
- Not all videos have transcripts
- App will still process video metadata and description

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💡 Tips

- For best results with images, use high-quality scans
- Audio/video files may take longer to process
- YouTube videos with auto-generated captions work best
- Clear the index periodically to manage storage

## 🌟 Acknowledgments

- **LlamaIndex** - RAG framework
- **Groq** - Fast LLM inference
- **Streamlit** - UI framework
- **ChromaDB** - Vector database
- **HuggingFace** - Embeddings

---

Made with ❤️ using LlamaIndex, Groq, and Streamlit
