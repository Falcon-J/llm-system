"""
Simple error check - test imports only
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test critical imports"""
    print("🔍 Testing critical imports...")
    
    try:
        print("1. Testing main module...")
        import main
        print("   ✅ main.py imports successfully")
    except Exception as e:
        print(f"   ❌ main.py import failed: {e}")
        return False
    
    try:
        print("2. Testing config...")
        from src.core.config import get_settings
        settings = get_settings()
        print("   ✅ config imports and works")
    except Exception as e:
        print(f"   ❌ config import failed: {e}")
        return False
    
    try:
        print("3. Testing services...")
        from src.services.llm_service import LLMService
        from src.services.document_processor import DocumentProcessor
        from src.services.embedding_service import EmbeddingService
        from src.services.retrieval_service import RetrievalService
        print("   ✅ All services import successfully")
    except Exception as e:
        print(f"   ❌ Service import failed: {e}")
        return False
    
    try:
        print("4. Testing models...")
        from src.models.schemas import DocumentSchema  # Replace with actual needed names
        print("   ✅ Models import successfully")
    except Exception as e:
        print(f"   ❌ Models import failed: {e}")
        return False
    
    print("\n🎉 All critical imports working!")
    return True

def test_basic_functionality():
    """Test basic functionality without API key"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        print("1. Testing document processor...")
        from src.services.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print("   ✅ DocumentProcessor created successfully")
    except Exception as e:
        print(f"   ❌ DocumentProcessor failed: {e}")
        return False
    
    try:
        print("2. Testing fallback embedding...")
        from src.services.fallback_embedding import FallbackEmbeddingService
        fallback = FallbackEmbeddingService()
        print("   ✅ FallbackEmbeddingService created successfully")
    except Exception as e:
        print(f"   ❌ FallbackEmbeddingService failed: {e}")
        return False
    
    print("\n🎉 Basic functionality working!")
    return True

if __name__ == "__main__":
    print("🚀 HackRx Project Error Check")
    print("=" * 40)
    
    imports_ok = test_imports()
    basic_ok = test_basic_functionality()
    
    print("\n" + "=" * 40)
    if imports_ok and basic_ok:
        print("✅ ALL TESTS PASSED!")
        print("🎯 Your project is ready for deployment!")
        print("\n📋 Next steps:")
        print("   1. Set OPENAI_API_KEY environment variable")
        print("   2. Run: uvicorn main:app --host 0.0.0.0 --port 8000")
        print("   3. Test with: python test_production.py")
    else:
        print("❌ Some tests failed")
        print("🔧 Please fix the errors above")
