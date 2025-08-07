# 🚀 HackRx LLM Query-Retrieval System

An intelligent document processing system that answers questions from PDFs, DOCX, and email documents using OpenRouter's GPT-4 models with semantic search.

## 🎯 Competition Features

- **Document Processing**: PDF, DOCX, Email support
- **Semantic Search**: Vector similarity with TF-IDF fallback  
- **LLM Integration**: OpenRouter/OpenAI GPT-4 compatible
- **Competition API**: Exact `/hackrx/run` endpoint format
- **Production Ready**: Railway deployment configured

## 🚀 Quick Start

### Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd hackrx-llm-system

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY=sk-or-v1-your-openrouter-key

# Run locally
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Railway Deployment

1. Push code to GitHub
2. Connect repository to Railway
3. Set environment variable: `OPENAI_API_KEY=your-openrouter-key`
4. Deploy automatically

## 🎯 API Usage

### Competition Endpoint: `POST /hackrx/run`

```bash
curl -X POST "https://your-app.railway.app/hackrx/run" \
  -H "Authorization: Bearer hackrx-api-token-2024" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
    "questions": [
      "What is the grace period for premium payment?",
      "Does this policy cover maternity expenses?"
    ]
  }'
```

**Response:**
```json
{
  "answers": [
    "A grace period of thirty days is provided...",
    "Yes, the policy covers maternity expenses..."
  ]
}
```

## 🛠️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenRouter API key (sk-or-v1-...) | ✅ |
| `PORT` | Server port (auto-set by Railway) | ❌ |

## 🧪 Testing

```bash
# Test deployment
python test_production.py

# Health check
curl https://your-app.railway.app/health
```

## 📁 Project Structure

```
hackrx-llm-system/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── railway.json              # Railway configuration
├── Procfile                   # Process definition
├── src/
│   ├── core/                  # Configuration & exceptions
│   ├── models/                # API request/response models
│   └── services/              # Core business logic
└── tests/                     # Test suite
```

## 🏆 Competition Compliance

✅ **Exact API Format**: POST /hackrx/run  
✅ **Authentication**: Bearer token validation  
✅ **Document Processing**: PDF, DOCX, Email  
✅ **Semantic Search**: Vector similarity  
✅ **Professional Responses**: Domain-specific prompts  
✅ **Error Handling**: Comprehensive error responses  

## 🎯 Built for HackRx Competition

This system is specifically designed for the HackRx competition requirements with focus on insurance, legal, HR, and compliance document processing.
"# llm-system" 
