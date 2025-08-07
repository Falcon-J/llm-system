"""
Pydantic models for request/response schemas
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class QueryRequest(BaseModel):
    """Request model for query processing"""
    
    documents: str = Field(
        ..., 
        description="URL to the document (PDF, DOCX, or email)",
        example="https://example.com/policy.pdf"
    )
    questions: List[str] = Field(
        ..., 
        min_items=1,
        description="List of questions to answer based on the document",
        example=[
            "What is the grace period for premium payment?",
            "Does this policy cover maternity expenses?"
        ]
    )


class QueryResponse(BaseModel):
    """Response model for query processing"""
    
    answers: List[str] = Field(
        ...,
        description="List of answers corresponding to the input questions",
        example=[
            "A grace period of thirty days is provided for premium payment.",
            "Yes, the policy covers maternity expenses with specific conditions."
        ]
    )


class DocumentChunk(BaseModel):
    """Model for document chunks"""
    
    content: str = Field(..., description="The text content of the chunk")
    chunk_id: int = Field(..., description="Unique identifier for the chunk")
    metadata: Optional[dict] = Field(default={}, description="Additional metadata for the chunk")


class RelevantChunk(BaseModel):
    """Model for relevant chunks with similarity scores"""
    
    content: str = Field(..., description="The text content of the chunk")
    chunk_id: int = Field(..., description="Unique identifier for the chunk")
    similarity_score: float = Field(..., description="Similarity score between 0 and 1")
    metadata: Optional[dict] = Field(default={}, description="Additional metadata")


class AnswerExplanation(BaseModel):
    """Model for answer explanations"""
    
    answer: str = Field(..., description="The generated answer")
    reasoning: str = Field(..., description="Explanation of how the answer was derived")
    relevant_chunks: List[RelevantChunk] = Field(
        ..., 
        description="Chunks used to generate the answer"
    )
    confidence_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Confidence score for the answer"
    )
