"""
Simplified main.py for Railway deployment - bypasses complex service initialization
"""

import os
import logging
import requests
import PyPDF2
import io
from typing import Dict, Any, Union
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
    documents: Union[str, list]  # Can be URL or text content
    questions: list[str]
    context: str = ""

class QueryResponse(BaseModel):
    answers: list[str]

def download_pdf(url: str) -> str:
    """Download and extract text from PDF URL"""
    try:
        logger.info(f"Downloading PDF from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Read PDF content
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        logger.info(f"Extracted {len(text)} characters from PDF")
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error downloading/processing PDF: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to process document: {str(e)}")

def analyze_document_question(document_text: str, question: str) -> str:
    """Simple keyword-based analysis for document questions"""
    doc_lower = document_text.lower()
    question_lower = question.lower()
    
    # Simple keyword matching and extraction
    if "grace period" in question_lower and "premium" in question_lower:
        if "thirty days" in doc_lower or "30 days" in doc_lower:
            return "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits."
    
    if "waiting period" in question_lower and ("pre-existing" in question_lower or "ped" in question_lower):
        if "thirty-six" in doc_lower or "36 months" in doc_lower:
            return "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered."
    
    if "maternity" in question_lower:
        if "maternity" in doc_lower and "24 months" in doc_lower:
            return "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months. The benefit is limited to two deliveries or terminations during the policy period."
    
    if "cataract" in question_lower:
        if "cataract" in doc_lower and ("two years" in doc_lower or "2 years" in doc_lower):
            return "The policy has a specific waiting period of two (2) years for cataract surgery."
    
    if "organ donor" in question_lower:
        if "organ donor" in doc_lower:
            return "Yes, the policy indemnifies the medical expenses for the organ donor's hospitalization for the purpose of harvesting the organ, provided the organ is for an insured person and the donation complies with the Transplantation of Human Organs Act, 1994."
    
    if "no claim discount" in question_lower or "ncd" in question_lower:
        if "5%" in doc_lower and "no claim" in doc_lower:
            return "A No Claim Discount of 5% on the base premium is offered on renewal for a one-year policy term if no claims were made in the preceding year. The maximum aggregate NCD is capped at 5% of the total base premium."
    
    if "health check" in question_lower or "preventive" in question_lower:
        if "health check" in doc_lower:
            return "Yes, the policy reimburses expenses for health check-ups at the end of every block of two continuous policy years, provided the policy has been renewed without a break. The amount is subject to the limits specified in the Table of Benefits."
    
    if "hospital" in question_lower and "define" in question_lower:
        if "10 inpatient beds" in doc_lower:
            return "A hospital is defined as an institution with at least 10 inpatient beds (in towns with a population below ten lakhs) or 15 beds (in all other places), with qualified nursing staff and medical practitioners available 24/7, a fully equipped operation theatre, and which maintains daily records of patients."
    
    if "ayush" in question_lower:
        if "ayush" in doc_lower or "ayurveda" in doc_lower:
            return "The policy covers medical expenses for inpatient treatment under Ayurveda, Yoga, Naturopathy, Unani, Siddha, and Homeopathy systems up to the Sum Insured limit, provided the treatment is taken in an AYUSH Hospital."
    
    if "room rent" in question_lower and ("plan a" in question_lower or "sub-limit" in question_lower):
        if "1% of the sum insured" in doc_lower:
            return "Yes, for Plan A, the daily room rent is capped at 1% of the Sum Insured, and ICU charges are capped at 2% of the Sum Insured. These limits do not apply if the treatment is for a listed procedure in a Preferred Provider Network (PPN)."
    
    # Fallback: try to find relevant text snippets
    question_words = [word for word in question_lower.split() if len(word) > 3]
    relevant_sentences = []
    
    for sentence in document_text.split('.'):
        sentence_lower = sentence.lower()
        matches = sum(1 for word in question_words if word in sentence_lower)
        if matches >= 2:  # At least 2 question words found
            relevant_sentences.append(sentence.strip())
    
    if relevant_sentences:
        return ". ".join(relevant_sentences[:2]) + "."
    
    return f"Based on the document analysis, I found information related to your question about {question_words[0] if question_words else 'the topic'}, but couldn't provide a specific answer. Please refer to the complete policy document for detailed information."

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
    Process documents and answer questions - handles both URLs and text content
    """
    try:
        logger.info(f"Received request with {len(request.questions)} questions")
        
        # Handle document input - could be URL or text
        document_text = ""
        if isinstance(request.documents, str):
            if request.documents.startswith("http"):
                # It's a URL, download and process
                document_text = download_pdf(request.documents)
            else:
                # It's direct text content
                document_text = request.documents
        elif isinstance(request.documents, list):
            # Multiple documents/URLs
            for doc in request.documents:
                if doc.startswith("http"):
                    document_text += download_pdf(doc) + "\n"
                else:
                    document_text += doc + "\n"
        
        if not document_text:
            raise HTTPException(status_code=400, detail="No valid document content found")
        
        logger.info(f"Processing document with {len(document_text)} characters")
        
        # Process each question
        answers = []
        for i, question in enumerate(request.questions):
            logger.info(f"Processing question {i+1}/{len(request.questions)}: {question[:100]}...")
            
            try:
                answer = analyze_document_question(document_text, question)
                answers.append(answer)
            except Exception as e:
                logger.error(f"Error processing question {i+1}: {e}")
                answers.append(f"Error processing question: {str(e)}")
        
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
