"""
Simplified main.py for Railway deployment - bypasses complex service initialization
"""

import os
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "hackrx-api-token-2024")

# Request/Response models
class QueryRequest(BaseModel):
    documents: str
    questions: list[str]
    context: str = ""

class QueryResponse(BaseModel):
    answers: list[str]

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify the authentication token"""
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials

# Create FastAPI app without complex lifespan
app = FastAPI(
    title="LLM-Powered Intelligent Query-Retrieval System",
    description="An intelligent document processing and query retrieval system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Simple health check endpoint"""
    return {
        "message": "LLM-Powered Intelligent Query-Retrieval System",
        "status": "healthy",
        "version": "1.0.0",
        "port": os.getenv("PORT", "8000"),
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "Service is running"
    }

@app.post("/hackrx/run", response_model=QueryResponse)
async def run_query_retrieval(
    request: QueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
) -> QueryResponse:
    """
    Simple endpoint that provides basic responses for testing
    """
    try:
        logger.info(f"Received request with {len(request.questions)} questions")
        
        # Simple mock responses for testing
        answers = []
        for i, question in enumerate(request.questions):
            answer = f"This is a simplified response to question {i+1}: '{question[:50]}...'. The system is working correctly."
            answers.append(answer)
        
        logger.info("Successfully processed all questions")
        return QueryResponse(answers=answers)
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
