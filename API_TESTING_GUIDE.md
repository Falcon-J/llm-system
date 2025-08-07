# 🧪 Testing Your HackRx API Endpoint

## 🚀 Quick Start - Test with Python

### 1. Simple Python Test Script

```python
import requests
import json

def test_hackrx_api():
    """Test the HackRx API endpoint"""

    # API endpoint
    url = "http://localhost:8000/hackrx/run"

    # Headers (IMPORTANT: Use exact token from competition)
    headers = {
        "Authorization": "Bearer hackrx-api-token-2024",
        "Content-Type": "application/json"
    }

    # Test payload (exact format from competition)
    payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?"
        ]
    }

    print("🧪 Testing HackRx API...")
    print(f"URL: {url}")
    print(f"Questions: {len(payload['questions'])}")

    try:
        # Make the request
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        print(f"\n📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📝 Answers received: {len(result.get('answers', []))}")

            # Show sample answers
            for i, answer in enumerate(result.get('answers', [])[:2], 1):
                print(f"\n🔍 Sample Answer {i}:")
                print(f"   Q: {payload['questions'][i-1]}")
                print(f"   A: {answer[:150]}...")

            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Is your server running?")
        print("   Start with: uvicorn main:app --port 8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_hackrx_api()
```

Save this as `test_api_endpoint.py` and run: `python test_api_endpoint.py`

## 📮 Postman Setup

### Method 1: Import Collection (Easiest)

1. **Download this Postman collection:**

```json
{
  "info": {
    "name": "HackRx Competition API",
    "description": "Test collection for HackRx LLM Query-Retrieval System"
  },
  "item": [
    {
      "name": "HackRx Run Query",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer hackrx-api-token-2024",
            "type": "text"
          },
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"documents\": \"https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D\",\n  \"questions\": [\n    \"What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?\",\n    \"What is the waiting period for pre-existing diseases (PED) to be covered?\",\n    \"Does this policy cover maternity expenses, and what are the conditions?\",\n    \"What is the waiting period for cataract surgery?\"\n  ]\n}"
        },
        "url": {
          "raw": "http://localhost:8000/hackrx/run",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["hackrx", "run"]
        }
      }
    }
  ]
}
```

2. **Import to Postman:**
   - Open Postman
   - Click "Import"
   - Paste the JSON above
   - Click "Import"

### Method 2: Manual Setup

1. **Create New Request:**

   - Method: `POST`
   - URL: `http://localhost:8000/hackrx/run`

2. **Headers:**

   ```
   Authorization: Bearer hackrx-api-token-2024
   Content-Type: application/json
   ```

3. **Body (Raw JSON):**
   ```json
   {
     "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
     "questions": [
       "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
       "What is the waiting period for pre-existing diseases (PED) to be covered?",
       "Does this policy cover maternity expenses, and what are the conditions?",
       "What is the waiting period for cataract surgery?"
     ]
   }
   ```

## 🌐 Browser/cURL Testing

### cURL Command

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Authorization: Bearer hackrx-api-token-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
      "What is the grace period for premium payment?",
      "Does this policy cover maternity expenses?"
    ]
  }'
```

### PowerShell (Windows)

```powershell
$headers = @{
    'Authorization' = 'Bearer hackrx-api-token-2024'
    'Content-Type' = 'application/json'
}

$body = @{
    documents = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    questions = @(
        "What is the grace period for premium payment?",
        "Does this policy cover maternity expenses?"
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/hackrx/run" -Method POST -Headers $headers -Body $body
```

## 🔍 Testing Different Scenarios

### Test 1: Simple Question

```json
{
  "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=...",
  "questions": ["What is the grace period for premium payment?"]
}
```

### Test 2: Multiple Questions

```json
{
  "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=...",
  "questions": [
    "What is the grace period for premium payment?",
    "Does this policy cover maternity expenses?",
    "What is the waiting period for cataract surgery?"
  ]
}
```

### Test 3: Authentication Error (Wrong Token)

```json
Headers: Authorization: Bearer wrong-token
```

## 📊 Expected Response Format

**Success (200):**

```json
{
  "answers": [
    "A grace period of thirty days is provided for premium payment after the due date...",
    "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination...",
    "The policy has a specific waiting period of two (2) years for cataract surgery."
  ]
}
```

**Error (401 - Wrong Auth):**

```json
{
  "detail": "Invalid authentication token"
}
```

**Error (422 - Bad Request):**

```json
{
  "detail": "Validation error: missing required fields"
}
```

## 🛠️ Debugging Tips

1. **Server Not Responding?**

   - Check if server is running: `http://localhost:8000/docs`
   - Try different port: `http://localhost:8001/hackrx/run`

2. **Authentication Errors?**

   - Verify exact token: `hackrx-api-token-2024`
   - Check header format: `Bearer hackrx-api-token-2024`

3. **Timeout Issues?**

   - Document processing can take 30-60 seconds
   - Increase timeout in your test tool

4. **OpenRouter Issues?**
   - Check your API key has credits
   - Verify key is set in environment

## 🚀 Quick Test Checklist

- [ ] Server is running (`uvicorn main:app --port 8000`)
- [ ] OpenRouter API key is configured
- [ ] Test endpoint responds (`http://localhost:8000/docs`)
- [ ] Authentication works with correct token
- [ ] Sample request returns valid JSON
- [ ] Response has `answers` array
- [ ] Answers are relevant to questions

## 🏆 Ready for Competition!

Your API endpoint is now fully testable and ready for the HackRx competition evaluation!
