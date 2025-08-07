"""
Simple launcher for the HackRx system - Python 3.13 compatible
"""

import os
import sys
import subprocess

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🎯 HackRx LLM-Powered Intelligent Query-Retrieval System")
    print("=" * 60)
    print("🐍 Python version:", sys.version)
    print("📁 Working directory:", os.getcwd())
    
    # Check if we have the OpenAI API key
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'sk-your-openai-api-key-here':
            print("✅ OpenAI API key found")
            key_status = True
        else:
            print("⚠️  OpenAI API key not configured")
            key_status = False
    except:
        print("⚠️  Could not load environment")
        key_status = False
    
    print("\n📋 Available actions:")
    print("1. Test basic functionality")
    print("2. Start the API server") 
    print("3. Run the demo")
    print("4. Exit")
    
    choice = input("\n🔵 Enter your choice (1-4): ").strip()
    
    if choice == "1":
        test_basic()
    elif choice == "2":
        if key_status:
            start_server()
        else:
            print("❌ Cannot start server without API key")
    elif choice == "3":
        if key_status:
            run_demo()
        else:
            print("❌ Cannot run demo without API key")
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

def test_basic():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test core imports
        print("📦 Testing imports...")
        import sys
        sys.path.insert(0, '.')
        
        from src.core.config import get_settings
        from src.services.document_processor import DocumentProcessor
        from src.utils.text_utils import TextAnalyzer
        
        print("✅ Core imports successful")
        
        # Test configuration
        settings = get_settings()
        print(f"✅ Configuration loaded")
        
        # Test document processing
        processor = DocumentProcessor()
        sample_text = "This is a sample insurance policy document. The grace period is thirty days."
        chunks = processor.chunk_text(sample_text)
        print(f"✅ Text processing works: {len(chunks)} chunks")
        
        # Test text analysis
        analyzer = TextAnalyzer()
        keywords = analyzer.extract_keywords(sample_text)
        print(f"✅ Text analysis works: found {len(keywords)} keywords")
        
        print("\n🎉 All basic tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def start_server():
    """Start the FastAPI server"""
    print("\n🌐 Starting API server...")
    print("📍 Server will be at: http://localhost:8000")
    print("📚 Documentation at: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def run_demo():
    """Run the demo"""
    print("\n🚀 Running demo...")
    
    try:
        import asyncio
        import sys
        sys.path.insert(0, '.')
        
        from demo import run_demo
        asyncio.run(run_demo())
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
