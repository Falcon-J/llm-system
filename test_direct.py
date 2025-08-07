"""
Direct OpenRouter test - paste your API key here
"""

from openai import OpenAI

def test_with_key():
    # PASTE YOUR OPENROUTER API KEY HERE
    api_key = "sk-or-v1-YOUR_KEY_HERE"  # Replace with your actual key
    
    if api_key == "sk-or-v1-YOUR_KEY_HERE":
        print("❌ Please edit this file and paste your actual OpenRouter API key")
        print("   Replace 'sk-or-v1-YOUR_KEY_HERE' with your real key")
        return False
    
    print("🔧 Testing OpenRouter API...")
    print(f"   Key: {api_key[:20]}...")
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        print("🚀 Sending test request...")
        
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Just say 'API test successful!' to confirm this works."}
            ],
            max_tokens=20
        )
        
        content = response.choices[0].message.content
        result = content.strip() if content is not None else ""
        print(f"✅ SUCCESS: {result}")
        
        print("\n🎯 Your OpenRouter setup is working!")
        print("   Now you can run the full HackRx system")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔍 Common issues:")
        print("   - Check your API key is correct")
        print("   - Ensure you have credits on OpenRouter")
        print("   - Verify the model 'openai/gpt-4o-mini' is available")
        return False

if __name__ == "__main__":
    test_with_key()
