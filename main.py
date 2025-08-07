"""
Main FastAPI application for the LLM-Powered Intelligent Query-Retrieval System
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.models.schemas import QueryResponse
from src.models.schemas import QueryRequest
 # Change 'QueryInput' to the actual class name if different
from src.services.document_processor import DocumentProcessor
from src.services.embedding_service import EmbeddingService
from src.services.fallback_embedding import FallbackEmbeddingService
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService
from src.core.config import get_settings
from src.core.exceptions import DocumentProcessingError, EmbeddingError, LLMError

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
settings = get_settings()

# Global services - properly typed
document_processor: Union[DocumentProcessor, None] = None
embedding_service: Union[EmbeddingService, FallbackEmbeddingService, None] = None
llm_service: Union[LLMService, None] = None
retrieval_service: Union[RetrievalService, None] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global document_processor, embedding_service, llm_service, retrieval_service
    
    logger.info("Initializing services...")
    
    try:
        # Initialize services
        document_processor = DocumentProcessor()
        llm_service = LLMService()
        
        # Try to initialize embedding service, fallback if needed
        try:
            embedding_service = EmbeddingService()
            logger.info("Using OpenAI/OpenRouter embedding service")
        except Exception as e:
            logger.warning(f"OpenAI embedding service failed: {e}")
            logger.info("Using fallback TF-IDF embedding service")
            embedding_service = FallbackEmbeddingService()
        
        retrieval_service = RetrievalService(embedding_service, llm_service)
        
        logger.info("All services initialized successfully")
        
        # Yield to start the application
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        # Still yield to allow the app to start (health checks can report the error)
        yield
    finally:
        logger.info("Shutting down services...")


# Create FastAPI app
app = FastAPI(
    title="LLM-Powered Intelligent Query-Retrieval System",
    description="An intelligent document processing and query retrieval system for insurance, legal, HR, and compliance domains",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify the authentication token"""
    if credentials.credentials != settings.auth_token:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials


@app.get("/")
async def root():
    """Root endpoint - simple health check for Railway"""
    return {
        "message": "LLM-Powered Intelligent Query-Retrieval System",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check - no auth required for Railway"""
    try:
        # Basic health check that Railway can use
        return {
            "status": "healthy",
            "version": "1.0.0",
            "services": {
                "document_processor": document_processor is not None,
                "embedding_service": embedding_service is not None,
                "llm_service": llm_service is not None,
                "retrieval_service": retrieval_service is not None
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.post("/hackrx/run", response_model=QueryResponse)
async def run_query_retrieval(
    request: QueryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
) -> QueryResponse:
    """
    Main endpoint for processing documents and answering questions
    
    Args:
        request: QueryRequest containing document text/context and questions
        credentials: Authentication credentials
        
    Returns:
        QueryResponse with answers and explanations
    """
    try:
        logger.info(f"Processing request with {len(request.questions)} questions")
        
        # Check services are initialized
        if not document_processor or not embedding_service or not llm_service or not retrieval_service:
            raise HTTPException(status_code=500, detail="Services not properly initialized")
        
        # Step 1: Process documents
        logger.info("Step 1: Processing documents...")
        if request.documents:
            # Use provided document text directly
            document_content = request.documents
        else:
            # If no documents provided, use context or raise error
            if request.context:
                document_content = request.context
            else:
                raise HTTPException(status_code=400, detail="Either documents or context must be provided")
        
        # Step 2: Create embeddings and build vector store
        logger.info("Step 2: Creating embeddings...")
        chunks = document_processor.chunk_text(document_content)
        vector_store = await embedding_service.create_vector_store(chunks)
        
        # Step 3: Process each question
        logger.info("Step 3: Processing questions...")
        answers = []
        
        for i, question in enumerate(request.questions):
            logger.info(f"Processing question {i+1}/{len(request.questions)}: {question[:100]}...")
            
            try:
                # Retrieve relevant chunks
                relevant_chunks = await retrieval_service.retrieve_relevant_chunks(
                    question, vector_store, chunks
                )
                
                # Generate answer using LLM
                answer = await llm_service.generate_answer(question, relevant_chunks)
                answers.append(answer)
                
            except Exception as e:
                logger.error(f"Error processing question {i+1}: {e}")
                answers.append(f"Error processing question: {str(e)}")
        
        logger.info("Successfully processed all questions")
        return QueryResponse(answers=answers)
        
    except DocumentProcessingError as e:
        logger.error(f"Document processing error: {e}")
        raise HTTPException(status_code=400, detail=f"Document processing failed: {str(e)}")
        
    except EmbeddingError as e:
        logger.error(f"Embedding error: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding service failed: {str(e)}")
        
    except LLMError as e:
        logger.error(f"LLM error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM service failed: {str(e)}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable for Railway compatibility
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )
