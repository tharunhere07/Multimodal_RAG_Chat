"""
Test script to verify all dependencies are installed correctly
"""
import sys

def test_imports():
    print("🔍 Testing Dependencies...\n")
    print("=" * 60)
    
    tests = [
        ("Streamlit", "streamlit"),
        ("LlamaIndex Core", "llama_index.core"),
        ("LlamaIndex Groq", "llama_index.llms.groq"),
        ("LlamaIndex Embeddings", "llama_index.embeddings.huggingface"),
        ("Python-dotenv", "dotenv"),
        ("PyPDF2", "PyPDF2"),
        ("Python-docx", "docx"),
        ("Pillow (PIL)", "PIL"),
        ("Pytesseract", "pytesseract"),
        ("MoviePy", "moviepy.editor"),
        ("SpeechRecognition", "speech_recognition"),
        ("Pydub", "pydub"),
        ("YouTube Transcript API", "youtube_transcript_api"),
        ("yt-dlp", "yt_dlp"),
        ("ChromaDB", "chromadb"),
        ("Sentence Transformers", "sentence_transformers"),
        ("Groq", "groq"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
    ]
    
    passed = 0
    failed = []
    
    for name, module in tests:
        try:
            __import__(module)
            print(f"✅ {name:<30} OK")
            passed += 1
        except ImportError as e:
            print(f"❌ {name:<30} FAILED")
            failed.append((name, str(e)))
    
    print("\n" + "=" * 60)
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    
    if failed:
        print("\n⚠️  Failed imports:")
        for name, error in failed:
            print(f"   - {name}: {error}")
        print("\n💡 Run: pip install -r requirements.txt")
    else:
        print("\n🎉 All dependencies installed successfully!")
    
    # Test system dependencies
    print("\n" + "=" * 60)
    print("\n🔧 Testing System Dependencies...\n")
    
    # Test Tesseract
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR               OK")
    except Exception as e:
        print("❌ Tesseract OCR               NOT FOUND")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Test FFmpeg
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✅ FFmpeg                      OK")
        else:
            print("❌ FFmpeg                      NOT FOUND")
    except Exception:
        print("❌ FFmpeg                      NOT FOUND")
        print("   Install from: https://ffmpeg.org/download.html")
    
    # Check .env file
    print("\n" + "=" * 60)
    print("\n⚙️  Configuration Check...\n")
    
    import os
    if os.path.exists('.env'):
        print("✅ .env file                   EXISTS")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        groq_key = os.getenv('GROQ_API_KEY')
        if groq_key and groq_key != 'your_groq_api_key_here':
            print("✅ GROQ_API_KEY                SET")
        else:
            print("⚠️  GROQ_API_KEY                NOT SET")
            print("   Edit .env and add your Groq API key")
            print("   Get it from: https://console.groq.com/")
    else:
        print("⚠️  .env file                   NOT FOUND")
        print("   Run: python setup.py")
    
    print("\n" + "=" * 60)
    
    if failed or not os.path.exists('.env'):
        print("\n❌ Setup incomplete. Please fix the issues above.")
        return False
    else:
        print("\n✅ All checks passed! Ready to run the app.")
        print("\n🚀 Start the app with: streamlit run app.py")
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
