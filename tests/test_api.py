"""
Test script to verify the API functionality
"""

import asyncio
import json
import aiohttp
from typing import Dict, Any


class APITester:
    """Test class for the HackRx API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", auth_token: str = None):
        self.base_url = base_url
        self.auth_token = auth_token or "ead1a25870571e01ec9cb446ce203fe390a9440e6a3e800b6f5cb2aa53bb254d"
        
    async def test_health_check(self) -> Dict[str, Any]:
        """Test the health check endpoint"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.base_url}/health") as response:
                    result = await response.json()
                    print(f"Health Check Status: {response.status}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    return result
            except Exception as e:
                print(f"Health check failed: {e}")
                return {"error": str(e)}
    
    async def test_hackrx_endpoint(self, documents_url: str, questions: list) -> Dict[str, Any]:
        """Test the main hackrx/run endpoint"""
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "documents": documents_url,
            "questions": questions
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/hackrx/run",
                    headers=headers,
                    json=payload
                ) as response:
                    result = await response.json()
                    print(f"HackRx Endpoint Status: {response.status}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    return result
            except Exception as e:
                print(f"HackRx endpoint test failed: {e}")
                return {"error": str(e)}
    
    async def run_sample_test(self):
        """Run a test with the provided sample data"""
        print("=== Starting API Tests ===\n")
        
        # Test 1: Health Check
        print("1. Testing Health Check...")
        await self.test_health_check()
        print("\n" + "="*50 + "\n")
        
        # Test 2: Sample HackRx request
        print("2. Testing HackRx Endpoint with Sample Data...")
        
        documents_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
        
        sample_questions = [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]
        
        await self.test_hackrx_endpoint(documents_url, sample_questions)
        print("\n=== Tests Completed ===")


async def main():
    """Main test function"""
    tester = APITester()
    await tester.run_sample_test()


if __name__ == "__main__":
    asyncio.run(main())
