"""
Production-ready API test for Railway deployment
"""

import requests
import os

# Get base URL from environment or default to localhost
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")


def test_production_api():
    """Test the deployed API"""
    print(f"🧪 Testing API at: {BASE_URL}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            data = response.json()
            print(f"   Services: {data.get('services', {})}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: HackRx endpoint
    print("\n2️⃣ Testing HackRx competition endpoint...")
    headers = {
        "Authorization": "Bearer hackrx-api-token-2024",
        "Content-Type": "application/json"
    }
    
    payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": ["What is the grace period for premium payment?"]
    }
    
    try:
        print("   Sending request (this may take 30-60 seconds)...")
        response = requests.post(
            f"{BASE_URL}/hackrx/run", 
            headers=headers, 
            json=payload, 
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            if "answers" in data and len(data["answers"]) > 0:
                print("✅ HackRx endpoint test passed")
                print(f"   Answer preview: {data['answers'][0][:100]}...")
                return True
            else:
                print("❌ Invalid response format")
                return False
        else:
            print(f"❌ HackRx endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ HackRx endpoint error: {e}")
        return False


if __name__ == "__main__":
    success = test_production_api()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! API is ready for production.")
        print("🎯 Your HackRx system is deployment-ready!")
    else:
        print("❌ Tests failed. Check logs and configuration.")
        print("🔧 Ensure OPENAI_API_KEY is set with your OpenRouter key.")
    
    exit(0 if success else 1)
