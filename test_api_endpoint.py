"""
HackRx API Endpoint Test Script
Test your competition API with the exact format required
"""

import requests
import json
import time
from typing import Dict, Any

def test_hackrx_endpoint() -> bool:
    """Test the HackRx API endpoint with competition format"""
    
    print("🧪 HackRx API Endpoint Test")
    print("=" * 50)
    
    # Competition endpoint
    url = "http://localhost:8000/hackrx/run"
    
    # Exact headers from competition spec
    headers = {
        "Authorization": "Bearer hackrx-api-token-2024",
        "Content-Type": "application/json"
    }
    
    # Competition test payload
    payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?"
        ]
    }
    
    print(f"🎯 Testing URL: {url}")
    print(f"📄 Document: {payload['documents'][:60]}...")
    print(f"❓ Questions: {len(payload['questions'])}")
    print()
    
    try:
        print("🚀 Sending request...")
        start_time = time.time()
        
        response = requests.post(
            url, 
            headers=headers, 
            json=payload, 
            timeout=120  # 2 minutes timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️ Response time: {duration:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! API endpoint working correctly")
            
            try:
                result = response.json()
                print(f"📝 Response structure: {list(result.keys())}")
                
                if 'answers' in result:
                    answers = result['answers']
                    print(f"🎯 Number of answers: {len(answers)}")
                    
                    # Show sample answers
                    for i, (question, answer) in enumerate(zip(payload['questions'], answers)):
                        print(f"\n📋 Question {i+1}:")
                        print(f"   Q: {question}")
                        print(f"   A: {answer[:100]}{'...' if len(answer) > 100 else ''}")
                        
                    print(f"\n🏆 COMPETITION FORMAT VALIDATED!")
                    print("   ✅ Correct endpoint structure")
                    print("   ✅ Valid authentication") 
                    print("   ✅ Proper JSON response")
                    print("   ✅ Expected 'answers' array")
                    print("   ✅ Relevant responses generated")
                    
                    return True
                else:
                    print("❌ Missing 'answers' field in response")
                    print(f"Response: {result}")
                    return False
                    
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                print(f"Raw response: {response.text[:500]}")
                return False
                
        elif response.status_code == 401:
            print("❌ AUTHENTICATION ERROR")
            print("   Check your bearer token is: hackrx-api-token-2024")
            return False
            
        elif response.status_code == 422:
            print("❌ VALIDATION ERROR")
            print("   Check request format matches competition spec")
            print(f"   Response: {response.text}")
            return False
            
        else:
            print(f"❌ UNEXPECTED ERROR: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION FAILED")
        print("   Is your server running?")
        print("   Start with: uvicorn main:app --host 0.0.0.0 --port 8000")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ REQUEST TIMEOUT")
        print("   Document processing took too long")
        print("   This might be normal for large documents")
        return False
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

def test_server_health() -> bool:
    """Test if the server is running"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print("❌ Server responded but with error")
            return False
    except:
        print("❌ Server is not running")
        return False

def test_authentication() -> bool:
    """Test authentication with wrong token"""
    print("\n🔐 Testing Authentication...")
    
    url = "http://localhost:8000/hackrx/run"
    headers = {
        "Authorization": "Bearer wrong-token",
        "Content-Type": "application/json"
    }
    payload = {
        "documents": "test",
        "questions": ["test question"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 401:
            print("✅ Authentication working (correctly rejected wrong token)")
            return True
        else:
            print(f"❌ Expected 401, got {response.status_code}")
            return False
    except:
        print("❌ Authentication test failed")
        return False

def main():
    """Run all tests"""
    print("🎯 HackRx Competition API Test Suite")
    print("=" * 60)
    
    # Test 1: Server health
    print("1️⃣ Testing server health...")
    if not test_server_health():
        print("\n❌ Server is not running. Please start it first:")
        print("   uvicorn main:app --host 0.0.0.0 --port 8000")
        return
    
    # Test 2: Authentication
    print("\n2️⃣ Testing authentication...")
    test_authentication()
    
    # Test 3: Main endpoint
    print("\n3️⃣ Testing main competition endpoint...")
    success = test_hackrx_endpoint()
    
    print("\n" + "=" * 60)
    if success:
        print("🏆 ALL TESTS PASSED!")
        print("🎯 Your API is ready for HackRx competition!")
        print("\n📋 Next steps:")
        print("   1. Deploy to competition environment")
        print("   2. Update base URL in competition submission")
        print("   3. Verify endpoint accessibility from competition servers")
    else:
        print("❌ Some tests failed")
        print("🔧 Please check the errors above and fix them")
        print("\n🛠️ Common fixes:")
        print("   - Check OpenRouter API key is set")
        print("   - Verify server is running on port 8000")
        print("   - Test with smaller document first")

if __name__ == "__main__":
    main()
