"""
Minimal Railway health check test
"""
import os
import sys
import asyncio

# Set environment variables for testing
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["AUTH_TOKEN"] = "test-token"

def test_basic_app():
    """Test basic FastAPI app creation"""
    try:
        print("Testing basic app creation...")
        
        # Import FastAPI components
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("✅ FastAPI imports work")
        
        # Test config
        from src.core.config import get_settings
        settings = get_settings()
        print(f"✅ Config loads - port: {settings.port}")
        
        # Create minimal app
        app = FastAPI(title="Test App")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/")
        async def root():
            return {"status": "healthy"}
            
        print("✅ Basic app created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_basic_app():
        print("✅ Basic app test passed!")
    else:
        print("❌ Basic app test failed!")
        sys.exit(1)
