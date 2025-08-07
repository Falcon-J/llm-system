#!/usr/bin/env python3
"""
Simple health check test script
"""
import requests
import time
import sys

def test_health_endpoint(base_url="http://localhost:8000"):
    """Test the health endpoints"""
    try:
        # Test root endpoint
        print("Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=30)
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root response: {response.json()}")
        
        # Test health endpoint
        print("\nTesting health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=30)
        print(f"Health endpoint status: {response.status_code}")
        print(f"Health response: {response.json()}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("Connection failed - is the server running?")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # If URL provided as argument, use it
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Testing health endpoints at {url}")
    if test_health_endpoint(url):
        print("✅ Health checks passed!")
    else:
        print("❌ Health checks failed!")
        sys.exit(1)
