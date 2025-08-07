"""
Simplified main.py for Railway deployment - bypasses complex service initialization
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
