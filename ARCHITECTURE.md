# LLM-Powered Intelligent Query-Retrieval System

## System Architecture

This system implements a sophisticated document processing and query retrieval pipeline designed for insurance, legal, HR, and compliance domains.

### Architecture Components

```
1. Input Documents (PDF/DOCX/Email)
   ↓
2. Document Processor (Text Extraction & Chunking)
   ↓
3. Embedding Service (OpenAI + FAISS Vector Store)
   ↓
4. Query Processing (Semantic Search + LLM Analysis)
   ↓
5. Answer Generation (GPT-4 with Explainable AI)
   ↓
6. JSON Response (Structured Output)
```

## Key Features

### 🔍 **Intelligent Document Processing**

- **Multi-format Support**: PDF, DOCX, and email documents
- **Smart Text Extraction**: Handles complex layouts and formatting
- **Optimized Chunking**: Overlapping chunks for better context preservation

### 🧠 **Advanced Semantic Search**

- **OpenAI Embeddings**: High-quality text-embedding-ada-002 embeddings
- **FAISS Vector Store**: Fast and efficient similarity search
- **Adaptive Retrieval**: Dynamic threshold adjustment for optimal results

### 🤖 **LLM-Powered Analysis**

- **GPT-4 Integration**: State-of-the-art language understanding
- **Clause Matching**: Semantic similarity for legal/policy documents
- **Decision Logic**: Explainable reasoning for complex queries

### 📊 **Explainable AI**

- **Decision Rationale**: Clear explanations for each answer
- **Source Attribution**: Traceable back to specific document sections
- **Confidence Scoring**: Reliability metrics for each response

## Quick Start

### 1. Setup Environment

```bash
# Clone and setup
cd Hackrx_FINAL
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Start the Server

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh

# Manual start
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API

```bash
python tests/test_api.py
```

## API Usage

### Base URL

```
http://localhost:8000
```

### Authentication

```
Authorization: Bearer ead1a25870571e01ec9cb446ce203fe390a9440e6a3e800b6f5cb2aa53bb254d
```

### Main Endpoint: POST `/hackrx/run`

**Request:**

```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "Does this policy cover maternity expenses?"
  ]
}
```

**Response:**

```json
{
  "answers": [
    "A grace period of thirty days is provided for premium payment.",
    "Yes, the policy covers maternity expenses with specific conditions."
  ]
}
```

## Technical Implementation

### Document Processing Pipeline

1. **URL Download**: Secure document retrieval with size limits
2. **Format Detection**: Automatic file type identification
3. **Text Extraction**:
   - PDF: PyPDF2 with layout preservation
   - DOCX: python-docx for structured content
   - Email: email-reply-parser for clean content
4. **Text Cleaning**: Normalization and optimization for embeddings
5. **Chunking**: Overlapping segments for context preservation

### Embedding & Vector Search

1. **Embedding Generation**: OpenAI text-embedding-ada-002
2. **Vector Store**: FAISS IndexFlatIP for cosine similarity
3. **Search Strategy**:
   - Semantic similarity matching
   - Adaptive threshold filtering
   - Top-k retrieval with relevance scoring

### LLM Processing

1. **Query Analysis**: Structured query extraction
2. **Context Preparation**: Relevant chunk assembly
3. **Answer Generation**: GPT-4 with domain-specific prompts
4. **Reasoning**: Explainable decision logic
5. **Quality Assurance**: Confidence scoring and validation

## Performance Optimization

### Token Efficiency

- **Smart Chunking**: Optimal context window usage
- **Selective Retrieval**: Only relevant chunks sent to LLM
- **Prompt Engineering**: Minimal token usage for maximum accuracy

### Latency Optimization

- **Async Processing**: Non-blocking operations
- **Batch Operations**: Efficient multi-query handling
- **Caching Strategy**: Reusable embeddings and results

### Scalability Features

- **Modular Design**: Easily extendable components
- **Error Handling**: Graceful failure recovery
- **Resource Management**: Memory and API rate limiting

## Domain-Specific Features

### Insurance Documents

- Policy clause interpretation
- Coverage analysis
- Premium and benefit calculations
- Claims process guidance

### Legal Documents

- Contract term analysis
- Compliance checking
- Risk assessment
- Regulatory interpretation

### HR Documents

- Policy interpretation
- Benefits analysis
- Compliance verification
- Procedure guidance

## Configuration Options

### Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# OpenAI Settings
OPENAI_API_KEY=your_key_here
LLM_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
MAX_TOKENS=2000
TEMPERATURE=0.1

# Document Processing
MAX_DOC_SIZE_MB=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Vector Search
SIMILARITY_THRESHOLD=0.7
MAX_RESULTS=10
```

## Error Handling

The system includes comprehensive error handling:

- **Document Processing Errors**: Invalid files, size limits, format issues
- **Embedding Errors**: API failures, rate limits, invalid content
- **LLM Errors**: Model failures, token limits, content policy violations
- **Retrieval Errors**: Vector store issues, search failures

## Testing & Validation

### Automated Tests

```bash
# Run API tests
python tests/test_api.py

# Health check
curl http://localhost:8000/health
```

### Manual Testing

1. Start the server
2. Access http://localhost:8000/docs for Swagger UI
3. Test with sample documents and queries
4. Verify response quality and explanations

## Evaluation Metrics

The system optimizes for:

1. **Accuracy**: Precise question understanding and clause matching
2. **Token Efficiency**: Optimized LLM usage and cost-effectiveness
3. **Latency**: Fast response times for real-time applications
4. **Reusability**: Modular code for easy extension
5. **Explainability**: Clear reasoning and source attribution

## Security Considerations

- **API Authentication**: Bearer token validation
- **Input Validation**: Comprehensive request sanitization
- **Rate Limiting**: Protection against abuse
- **Error Masking**: Secure error messages
- **Data Privacy**: No persistent storage of sensitive documents

## Future Enhancements

### Planned Features

- **Multi-language Support**: International document processing
- **Advanced Analytics**: Document insights and trends
- **Custom Models**: Domain-specific fine-tuning
- **Workflow Integration**: Enterprise system connectors
- **Real-time Updates**: Live document monitoring

### Performance Improvements

- **GPU Acceleration**: Faster embedding generation
- **Distributed Processing**: Multi-node scaling
- **Advanced Caching**: Intelligent result caching
- **Streaming Responses**: Real-time answer generation

## Support & Documentation

- **API Documentation**: Available at `/docs` endpoint
- **Code Documentation**: Comprehensive inline comments
- **Error Logs**: Detailed logging for troubleshooting
- **Performance Metrics**: Built-in monitoring and analytics
