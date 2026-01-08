"""
Setup script to help configure the application
"""
import os
from pathlib import Path

def setup():
    print("🚀 Multimodal RAG Application Setup\n")
    print("=" * 50)
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n📝 Creating .env file...")
        
        groq_key = input("Enter your Groq API Key (or press Enter to skip): ").strip()
        
        with open('.env', 'w') as f:
            if groq_key:
                f.write(f"GROQ_API_KEY={groq_key}\n")
            else:
                f.write("GROQ_API_KEY=your_groq_api_key_here\n")
        
        print("✅ .env file created!")
        
        if not groq_key:
            print("\n⚠️  Important: Please edit .env and add your Groq API key")
            print("   Get your key from: https://console.groq.com/")
    else:
        print("\n✅ .env file already exists")
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    os.makedirs('uploaded_files', exist_ok=True)
    os.makedirs('chroma_db', exist_ok=True)
    print("✅ Directories created!")
    
    print("\n" + "=" * 50)
    print("\n🎉 Setup complete!\n")
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Install Tesseract OCR (for image processing)")
    print("3. Install FFmpeg (for audio/video processing)")
    print("4. Run the app: streamlit run app.py")
    print("\nSee README.md for detailed instructions.")

if __name__ == "__main__":
    setup()
