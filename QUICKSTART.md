# 🚀 Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install System Dependencies

### Tesseract OCR (for image processing)
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

### FFmpeg (for audio/video processing)
- **Windows**: Download from https://ffmpeg.org/download.html
- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

## Step 3: Configure API Key

Run the setup script:
```bash
python setup.py
```

Or manually create a `.env` file with:
```
GROQ_API_KEY=your_actual_groq_api_key
```

Get your Groq API key from: https://console.groq.com/

## Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 5: Start Using!

1. **Upload Documents**: Use the sidebar to upload files
2. **Add YouTube Videos**: Paste YouTube URLs in the YouTube tab
3. **Ask Questions**: Type in the chat to query your documents

---

## Features Overview

✨ **What You Can Do:**
- Upload and process PDFs, Word docs, text files
- Extract text from images using OCR
- Transcribe audio and video files
- Get YouTube video transcripts
- Ask questions about all your content
- Get AI-powered answers with context

🎨 **Beautiful UI:**
- Modern gradient design
- Smooth animations
- Responsive chat interface
- Real-time processing feedback

---

## Troubleshooting

**"Tesseract not found"**
- Make sure Tesseract is installed and in your PATH
- Restart your terminal after installation

**"FFmpeg not found"**
- Install FFmpeg and add to PATH
- Test with: `ffmpeg -version`

**YouTube transcript errors**
- Not all videos have transcripts available
- The app will still process video metadata

**Groq API errors**
- Check your API key in `.env`
- Verify you have API credits at https://console.groq.com/

---

Need help? Check the full README.md for detailed documentation!
