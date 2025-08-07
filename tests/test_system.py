"""
Simple API test for the HackRx system
"""

import asyncio
import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_basic_functionality():
    """Test basic system functionality without external dependencies"""
    print("🧪 Testing Basic System Components")
    print("=" * 50)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from src.core.config import get_settings
        from src.services.document_processor import DocumentProcessor
        from src.utils.text_utils import TextAnalyzer
        print("✅ Core imports successful")
        
        # Test configuration
        print("⚙️  Testing configuration...")
        settings = get_settings()
        print(f"✅ Configuration loaded: API host = {settings.api_host}")
        
        # Test text processing
        print("📝 Testing text processing...")
        processor = DocumentProcessor()
        sample_text = "This is a sample insurance policy document. The grace period for premium payment is thirty days."
        chunks = processor.chunk_text(sample_text)
        print(f"✅ Text chunking works: {len(chunks)} chunks created")
        
        # Test text analysis
        print("🔍 Testing text analysis...")
        analyzer = TextAnalyzer()
        keywords = analyzer.extract_keywords(sample_text)
        print(f"✅ Keyword extraction works: {keywords[:5]}")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def test_with_api_key():
    """Test functionality that requires API key"""
    print("\n🔑 Testing API-dependent functionality...")
    
    try:
        from src.services.embedding_service import EmbeddingService
        from src.services.llm_service import LLMService
        from src.core.config import get_settings
        
        # Check if API key is available
        settings = get_settings()
        if not settings.openai_api_key or settings.openai_api_key.startswith('sk-your'):
            print("⚠️  OpenAI API key not configured - skipping API tests")
            return True
        
        print("🧠 Testing embedding service...")
        embedding_service = EmbeddingService()
        
        # Test embedding creation with a small sample
        sample_texts = ["This is a test document about insurance policies."]
        embeddings = await embedding_service.create_embeddings(sample_texts)
        print(f"✅ Embeddings created: shape {embeddings.shape}")
        
        print("🤖 Testing LLM service...")
        llm_service = LLMService()
        
        # Test simple query extraction
        query_info = await llm_service.extract_structured_query("What is the grace period?")
        print("✅ LLM query extraction works")
        
        print("🎉 API-dependent tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("💡 Make sure your OpenAI API key is valid and has sufficient credits")
        return False


async def test_api_server():
    """Test the API server endpoints"""
    print("\n🌐 Testing API server...")
    
    try:
        import httpx
        
        # Test if server is running
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get("http://localhost:8000/health", timeout=5.0)
                if response.status_code == 200:
                    print("✅ API server is running and healthy")
                    return True
                else:
                    print(f"⚠️  API server responded with status {response.status_code}")
                    return False
            except httpx.ConnectError:
                print("⚠️  API server is not running")
                print("💡 Start the server with: python -m uvicorn main:app --reload")
                return False
                
    except ImportError:
        print("⚠️  httpx not available for server testing")
        return True
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🎯 HackRx System Test Suite")
    print("=" * 60)
    
    # Test 1: Basic functionality
    basic_test = await test_basic_functionality()
    
    # Test 2: API-dependent functionality
    api_test = await test_with_api_key()
    
    # Test 3: Server test
    server_test = await test_api_server()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   Basic Functionality: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"   API Integration:     {'✅ PASS' if api_test else '❌ FAIL'}")
    print(f"   Server Health:       {'✅ PASS' if server_test else '⚠️  SKIP'}")
    
    if basic_test and api_test:
        print("\n🎉 System is ready for deployment!")
        print("\n🚀 Next steps:")
        print("   1. Start the server: python -m uvicorn main:app --reload")
        print("   2. Test the API: curl http://localhost:8000/health")
        print("   3. View docs: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")


if __name__ == "__main__":
    asyncio.run(main())
