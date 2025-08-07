"""
Quick OpenRouter API test
"""

import os
from openai import OpenAI

def test_openrouter():
    print("🔧 Testing OpenRouter API Key...")
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OPENAI_API_KEY found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        # Initialize OpenRouter client
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        print("🚀 Testing simple chat completion...")
        
        # Simple test
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'Hello from OpenRouter!' if this works."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ Success! Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_openrouter()
