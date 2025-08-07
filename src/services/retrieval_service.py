"""
Retrieval service that orchestrates document retrieval and answer generation
"""

import logging
from typing import List, Tuple, Union
from src.services.embedding_service import EmbeddingService, SimpleVectorStore
from src.services.fallback_embedding import FallbackEmbeddingService, FallbackVectorStore
from src.services.llm_service import LLMService
from src.core.config import get_settings
from src.core.exceptions import RetrievalError

logger = logging.getLogger(__name__)


class RetrievalService:
    """Service for orchestrating the retrieval and answer generation process"""
    
    def __init__(self, embedding_service: Union[EmbeddingService, FallbackEmbeddingService], llm_service: LLMService):
        self.settings = get_settings()
        self.embedding_service = embedding_service
        self.llm_service = llm_service
    
    async def retrieve_relevant_chunks(
        self, 
        question: str, 
        vector_store: Union[SimpleVectorStore, FallbackVectorStore], 
        chunks: List[str]
    ) -> List[Tuple[str, float, int]]:
        """
        Retrieve relevant chunks for a given question
        
        Args:
            question: The question to find relevant chunks for
            vector_store: FAISS vector store
            chunks: Original text chunks
            
        Returns:
            List of relevant chunks with similarity scores
            
        Raises:
            RetrievalError: If retrieval fails
        """
        try:
            logger.info(f"Retrieving relevant chunks for question: {question[:100]}...")
            
            # Search for similar chunks - type checked at runtime
            from src.services.embedding_service import EmbeddingService
            from src.services.fallback_embedding import FallbackEmbeddingService
            
            if isinstance(self.embedding_service, EmbeddingService):
                relevant_chunks = await self.embedding_service.search_similar(
                    query=question,
                    vector_store=vector_store,  # type: ignore
                    chunks=chunks,
                    k=self.settings.max_results
                )
            elif isinstance(self.embedding_service, FallbackEmbeddingService):
                relevant_chunks = await self.embedding_service.search_similar(
                    question, vector_store, chunks, self.settings.max_results  # type: ignore
                )
            else:
                raise RetrievalError("Unknown embedding service type")
            
            if not relevant_chunks:
                logger.warning("No relevant chunks found above similarity threshold")
                # If no chunks meet threshold, return top chunks anyway
                if isinstance(self.embedding_service, EmbeddingService):
                    relevant_chunks = await self.embedding_service.search_similar(
                        query=question,
                        vector_store=vector_store,  # type: ignore
                        chunks=chunks,
                        k=min(3, len(chunks))
                    )
                elif isinstance(self.embedding_service, FallbackEmbeddingService):
                    relevant_chunks = await self.embedding_service.search_similar(
                        question, vector_store, chunks, min(3, len(chunks))  # type: ignore
                    )
            
            logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks")
            return relevant_chunks
            
        except Exception as e:
            logger.error(f"Failed to retrieve relevant chunks: {e}")
            raise RetrievalError(f"Chunk retrieval failed: {str(e)}")
    
    async def process_query_with_explanation(
        self, 
        question: str, 
        vector_store: SimpleVectorStore, 
        chunks: List[str]
    ) -> dict:
        """
        Process a query and provide detailed explanation
        
        Args:
            question: The question to process
            vector_store: FAISS vector store
            chunks: Original text chunks
            
        Returns:
            Dictionary with answer, explanation, and metadata
        """
        try:
            logger.info(f"Processing query with explanation: {question[:100]}...")
            
            # Step 1: Extract structured query information
            structured_query = await self.llm_service.extract_structured_query(question)
            
            # Step 2: Retrieve relevant chunks
            relevant_chunks = await self.retrieve_relevant_chunks(question, vector_store, chunks)
            
            # Step 3: Evaluate clause logic
            clause_texts = [chunk[0] for chunk in relevant_chunks]
            logic_evaluation = await self.llm_service.evaluate_clause_logic(question, clause_texts)
            
            # Step 4: Generate final answer
            answer = await self.llm_service.generate_answer(question, relevant_chunks)
            
            return {
                "answer": answer,
                "structured_query": structured_query,
                "logic_evaluation": logic_evaluation,
                "relevant_chunks": [
                    {
                        "text": chunk[0],
                        "similarity_score": chunk[1],
                        "chunk_id": chunk[2]
                    } for chunk in relevant_chunks
                ],
                "metadata": {
                    "total_chunks_searched": len(chunks),
                    "relevant_chunks_found": len(relevant_chunks),
                    "similarity_threshold": self.settings.similarity_threshold
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process query with explanation: {e}")
            raise RetrievalError(f"Query processing failed: {str(e)}")
    
    async def batch_process_questions(
        self, 
        questions: List[str], 
        vector_store: SimpleVectorStore, 
        chunks: List[str]
    ) -> List[str]:
        """
        Process multiple questions efficiently
        
        Args:
            questions: List of questions to process
            vector_store: FAISS vector store
            chunks: Original text chunks
            
        Returns:
            List of answers corresponding to input questions
        """
        try:
            logger.info(f"Batch processing {len(questions)} questions")
            
            answers = []
            for i, question in enumerate(questions):
                logger.info(f"Processing question {i+1}/{len(questions)}")
                
                try:
                    # Retrieve relevant chunks
                    relevant_chunks = await self.retrieve_relevant_chunks(
                        question, vector_store, chunks
                    )
                    
                    # Generate answer
                    answer = await self.llm_service.generate_answer(question, relevant_chunks)
                    answers.append(answer)
                    
                except Exception as e:
                    logger.error(f"Error processing question {i+1}: {e}")
                    answers.append(f"Error: Unable to process question - {str(e)}")
            
            logger.info("Completed batch processing")
            return answers
            
        except Exception as e:
            logger.error(f"Failed batch processing: {e}")
            raise RetrievalError(f"Batch processing failed: {str(e)}")
    
    def calculate_confidence_score(self, relevant_chunks: List[Tuple[str, float, int]]) -> float:
        """
        Calculate confidence score based on similarity scores of relevant chunks
        
        Args:
            relevant_chunks: List of relevant chunks with similarity scores
            
        Returns:
            Confidence score between 0 and 1
        """
        if not relevant_chunks:
            return 0.0
        
        # Calculate weighted average of similarity scores
        scores = [chunk[1] for chunk in relevant_chunks]
        weights = [1.0 / (i + 1) for i in range(len(scores))]  # Higher weight for top results
        
        weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        total_weight = sum(weights)
        
        confidence = weighted_score / total_weight if total_weight > 0 else 0.0
        return min(confidence, 1.0)  # Cap at 1.0
