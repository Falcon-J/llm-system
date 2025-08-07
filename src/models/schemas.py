"""
Pydantic models for request/response schemas
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field, conlist


class QueryRequest(BaseModel):
    questions: List[str] = Field(
        ...,
        description="List of questions to be answered",
        examples=[
            ["What is the grace period for premium payment?", "Does the policy cover maternity expenses?"]
        ]
    )
    context: Optional[str] = Field(
        None,
        description="Optional context or background information for the questions"
    )
    documents: Optional[str] = Field(
        None,
        description="Optional document text to be used for answering the questions"
    )

class QueryResponse(BaseModel):
    """Response model for query processing"""
    
    answers: List[str] = Field(
        ...,
        description="List of answers corresponding to the input questions",
        examples=[
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
