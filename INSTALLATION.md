# 🚀 Installation & Deployment Guide

## Prerequisites

Before installing, ensure you have:
- **Python 3.8+** installed
- **pip** package manager
- **Git** (optional, for cloning)
- **Internet connection** (for downloading dependencies)

## Step-by-Step Installation

### 1️⃣ Clone or Download the Project

```bash
# If using Git
git clone <your-repo-url>
cd mm2

# Or download and extract the ZIP file
```

### 2️⃣ Install Python Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Note**: This will install:
- Streamlit (UI framework)
- LlamaIndex (RAG framework)
- Groq (LLM provider)
- ChromaDB (vector database)
- Document processing libraries
- And all other dependencies

### 3️⃣ Install System Dependencies

#### A. Tesseract OCR (for Image Processing)

**Windows:**
1. Download the installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Add to PATH:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Environment Variables → Path → Add: `C:\Program Files\Tesseract-OCR`
4. Verify: `tesseract --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
tesseract --version
```

**macOS:**
```bash
brew install tesseract
tesseract --version
```

#### B. FFmpeg (for Audio/Video Processing)

**Windows:**
1. Download from: https://ffmpeg.org/download.html
2. Extract the ZIP file
3. Add the `bin` folder to PATH
4. Verify: `ffmpeg -version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg
ffmpeg -version
```

### 4️⃣ Configure API Keys

#### Get Groq API Key
1. Visit: https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

#### Configure the Application

**Option A: Using the setup script (Recommended)**
```bash
python setup.py
# Enter your Groq API key when prompted
```

**Option B: Manual configuration**
```bash
# Copy the example file
cp .env.example .env

# Edit .env file
# Replace 'your_groq_api_key_here' with your actual key
```

Example `.env` file:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5️⃣ Verify Installation

Run the test script:
```bash
python test_setup.py
```

This will check:
- ✅ All Python dependencies
- ✅ Tesseract installation
- ✅ FFmpeg installation
- ✅ .env configuration

### 6️⃣ Run the Application

```bash
streamlit run app.py
```

The application will:
- Start on `http://localhost:8501`
- Automatically open in your browser
- Create necessary directories (`uploaded_files/`, `chroma_db/`)

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError"
**Problem**: Missing Python package
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

#### "Tesseract not found"
**Problem**: Tesseract not in PATH
**Solution**:
- Verify installation: `tesseract --version`
- Check PATH configuration
- Restart terminal after installation

#### "FFmpeg not found"
**Problem**: FFmpeg not in PATH
**Solution**:
- Verify installation: `ffmpeg -version`
- Check PATH configuration
- Restart terminal after installation

#### "Invalid API key"
**Problem**: Groq API key not set or invalid
**Solution**:
- Check `.env` file exists
- Verify API key is correct
- Ensure no extra spaces in `.env`
- Test at: https://console.groq.com/

#### "Port 8501 already in use"
**Problem**: Streamlit port occupied
**Solution**:
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

#### Speech recognition errors
**Problem**: No internet connection
**Solution**:
- Ensure stable internet connection
- Google Speech Recognition requires internet

#### YouTube transcript errors
**Problem**: Video has no transcript
**Solution**:
- Not all videos have transcripts
- App will use video description as fallback

### Performance Issues

#### Slow processing
- Large files take time (especially video)
- Audio/video need internet for transcription
- First run downloads embedding models (~100MB)

#### Memory issues
- Close other applications
- Process files in smaller batches
- Clear index if too many documents

## Advanced Configuration

### Changing the LLM Model

Edit `config.py`:
```python
# Options:
GROQ_MODEL = "mixtral-8x7b-32768"     # Fast, good for general use
GROQ_MODEL = "llama2-70b-4096"        # More capable, slower
GROQ_MODEL = "llama3-8b-8192"         # Good balance
```

### Changing Embedding Model

Edit `config.py`:
```python
# Options:
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # Fast, small
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"   # Better quality
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"  # Best quality, slower
```

### Customizing Storage Locations

Edit `config.py`:
```python
UPLOAD_DIR = "./uploaded_files"        # Where uploaded files are stored
VECTOR_STORE_DIR = "./chroma_db"       # Where vector database is stored
```

### Adjusting Chunk Size

Edit `rag_engine.py`:
```python
Settings.chunk_size = 512       # Increase for more context
Settings.chunk_overlap = 50     # Increase for better continuity
```

## Deployment Options

### Local Deployment

Already covered above - run `streamlit run app.py`

### Network Deployment

Run on your local network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

Access from other devices: `http://<your-ip>:8501`

### Cloud Deployment

#### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit: https://streamlit.io/cloud
3. Connect repository
4. Add Groq API key in Secrets
5. Deploy!

#### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ffmpeg

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t multimodal-rag .
docker run -p 8501:8501 --env-file .env multimodal-rag
```

## Updating the Application

```bash
# Pull latest changes (if using Git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart the app
streamlit run app.py
```

## Uninstallation

### Remove Python packages:
```bash
pip uninstall -r requirements.txt -y
```

### Remove system dependencies:
- Uninstall Tesseract from Control Panel (Windows) / Package Manager (Linux/Mac)
- Remove FFmpeg from your system

### Delete project files:
```bash
rm -rf mm2/  # Linux/Mac
rmdir /s mm2  # Windows
```

## Security Best Practices

1. **API Keys**: Never commit `.env` to version control
2. **Updates**: Keep dependencies updated for security patches
3. **Access**: Don't expose to public internet without authentication
4. **Data**: Clear sensitive documents from `uploaded_files/`
5. **Backups**: Backup `chroma_db/` if you have valuable indexed data

## Getting Help

- **Documentation**: See `README.md` and `FEATURES.md`
- **Issues**: Check common issues above
- **Testing**: Run `python test_setup.py`
- **Community**: GitHub Issues / Discussions

## Next Steps

After installation:
1. ✅ Run `python test_setup.py` to verify
2. ✅ Start app with `streamlit run app.py`
3. ✅ Upload a test document
4. ✅ Ask a question
5. ✅ Explore features!

---

**Happy Building! 🚀**
