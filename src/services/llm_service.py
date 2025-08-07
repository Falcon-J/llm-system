"""
LLM service for generating answers using OpenAI GPT models
"""

import logging
from typing import List, Tuple
from openai import OpenAI

from src.core.config import get_settings
from src.core.exceptions import LLMError

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM-based answer generation and processing"""
    
    def __init__(self):
        self.settings = get_settings()
        
        # Validate API key is present
        if not self.settings.openai_api_key:
            raise LLMError("OPENAI_API_KEY environment variable is required")
        
        try:
            self.client = OpenAI(
                api_key=self.settings.openai_api_key,
                base_url=self.settings.openai_base_url,
                timeout=30.0  # Add timeout for Railway
            )
            self.model = self.settings.llm_model
            self.max_tokens = self.settings.max_tokens
            self.temperature = self.settings.temperature
            
            logger.info(f"LLM service initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise LLMError(f"Failed to initialize LLM service: {str(e)}")
    
    async def generate_answer(
        self, 
        question: str, 
        relevant_chunks: List[Tuple[str, float, int]]
    ) -> str:
        """
        Generate an answer based on the question and relevant document chunks
        
        Args:
            question: The question to answer
            relevant_chunks: List of (chunk_text, similarity_score, chunk_id)
            
        Returns:
            Generated answer
            
        Raises:
            LLMError: If answer generation fails
        """
        try:
            logger.info(f"Generating answer for question: {question[:100]}...")
            
            # Prepare context from relevant chunks
            context = self._prepare_context(relevant_chunks)
            
            # Create prompt
            prompt = self._create_answer_prompt(question, context)
            
            # Generate answer using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer = response.choices[0].message.content
            if answer is None:
                raise LLMError("No content received from LLM")
            answer = answer.strip()
            logger.info("Successfully generated answer")
            
            return answer
            
        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            raise LLMError(f"Answer generation failed: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for answer generation"""
        return """You are an expert AI assistant specializing in document analysis for insurance, legal, HR, and compliance domains. 

Your task is to provide accurate, precise, and well-explained answers based on the provided document context. 

Key requirements:
1. Answer questions based ONLY on the provided context
2. Be precise and specific with details like numbers, dates, percentages, and conditions
3. If the context doesn't contain enough information, clearly state that
4. Provide clear, professional explanations
5. Use the exact terminology from the documents
6. Structure your answers logically
7. Do not make assumptions beyond what's explicitly stated in the context

Format your responses as clear, professional answers that would be appropriate for insurance, legal, or compliance professionals."""
    
    def _prepare_context(self, relevant_chunks: List[Tuple[str, float, int]]) -> str:
        """
        Prepare context from relevant chunks
        
        Args:
            relevant_chunks: List of (chunk_text, similarity_score, chunk_id)
            
        Returns:
            Formatted context string
        """
        if not relevant_chunks:
            return "No relevant context found."
        
        context_parts = []
        for i, (chunk_text, score, chunk_id) in enumerate(relevant_chunks):
            context_parts.append(f"Context {i+1} (Relevance: {score:.3f}):\n{chunk_text}\n")
        
        return "\n".join(context_parts)
    
    def _create_answer_prompt(self, question: str, context: str) -> str:
        """
        Create the prompt for answer generation
        
        Args:
            question: The question to answer
            context: The context from relevant chunks
            
        Returns:
            Formatted prompt
        """
        return f"""Based on the following document context, please answer the question accurately and completely.

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
- Answer based ONLY on the provided context
- Be specific with details like numbers, dates, conditions, and requirements
- If the context doesn't provide enough information to answer completely, state that clearly
- Use exact terminology from the documents
- Provide a clear, professional response

ANSWER:"""
    
    async def extract_structured_query(self, natural_query: str) -> dict:
        """
        Extract structured information from a natural language query
        
        Args:
            natural_query: Natural language query
            
        Returns:
            Structured query information
        """
        try:
            prompt = f"""Extract the key components from this query and structure them:

Query: "{natural_query}"

Please identify:
1. Main topic/subject
2. Specific conditions or requirements asked about
3. Type of information requested (coverage, limits, conditions, etc.)
4. Any specific terms or concepts mentioned

Respond in JSON format with these fields: topic, conditions, info_type, key_terms"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at parsing insurance, legal, and compliance queries. Extract structured information from natural language queries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            # Note: In a production system, you'd want to parse this JSON properly
            return {"raw_response": response.choices[0].message.content}
            
        except Exception as e:
            logger.error(f"Failed to extract structured query: {e}")
            return {"error": str(e)}
    
    async def evaluate_clause_logic(
        self, 
        question: str, 
        relevant_clauses: List[str]
    ) -> dict:
        """
        Evaluate logical relationships between clauses for decision making
        
        Args:
            question: The question being asked
            relevant_clauses: List of relevant document clauses
            
        Returns:
            Evaluation results with reasoning
        """
        try:
            clauses_text = "\n\n".join([f"Clause {i+1}: {clause}" for i, clause in enumerate(relevant_clauses)])
            
            prompt = f"""Analyze these clauses to answer the question and provide logical reasoning:

QUESTION: {question}

RELEVANT CLAUSES:
{clauses_text}

Please provide:
1. A direct answer to the question
2. Logical reasoning explaining how the clauses support your answer
3. Any conditions, limitations, or requirements that apply
4. Confidence level in your answer (1-10)

Structure your response clearly with these sections."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in analyzing insurance policies, legal documents, and compliance materials. Provide logical, well-reasoned analysis of document clauses."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.1
            )
            
            return {
                "evaluation": response.choices[0].message.content,
                "clauses_analyzed": len(relevant_clauses)
            }
            
        except Exception as e:
            logger.error(f"Failed to evaluate clause logic: {e}")
            raise LLMError(f"Clause evaluation failed: {str(e)}")
