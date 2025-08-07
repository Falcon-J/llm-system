"""
Fallback embedding service using simple text similarity when API embeddings fail
"""

import logging
import numpy as np
from typing import List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.core.config import get_settings
from src.core.exceptions import EmbeddingError

logger = logging.getLogger(__name__)


class FallbackVectorStore:
    """Fallback vector store using TF-IDF when API embeddings fail"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.vectors = None
        self.texts = None
        self.count = 0
    
    def add_texts(self, texts: List[str]):
        """Add texts and create TF-IDF vectors"""
        self.texts = texts
        self.vectors = self.vectorizer.fit_transform(texts)
        self.count = len(texts)
    
    def search(self, query: str, k: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Search for similar texts"""
        if self.vectors is None:
            return np.array([]), np.array([])
        
        # Transform query using the same vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:k]
        top_similarities = similarities[top_indices]
        
        return top_similarities, top_indices
    
    @property
    def ntotal(self) -> int:
        """Total number of vectors"""
        return self.count


class FallbackEmbeddingService:
    """Fallback embedding service using TF-IDF when API fails"""
    
    def __init__(self):
        self.settings = get_settings()
        logger.info("Using fallback TF-IDF embedding service")
    
    async def create_vector_store(self, chunks: List[str]) -> FallbackVectorStore:
        """
        Create a vector store from text chunks using TF-IDF
        
        Args:
            chunks: List of text chunks
            
        Returns:
            FallbackVectorStore for similarity search
        """
        try:
            logger.info(f"Creating fallback vector store for {len(chunks)} chunks")
            
            vector_store = FallbackVectorStore()
            vector_store.add_texts(chunks)
            
            logger.info(f"Created fallback vector store with {vector_store.ntotal} vectors")
            return vector_store
            
        except Exception as e:
            logger.error(f"Failed to create fallback vector store: {e}")
            raise EmbeddingError(f"Fallback vector store creation failed: {str(e)}")
    
    async def search_similar(
        self, 
        query: str, 
        vector_store: FallbackVectorStore, 
        chunks: List[str], 
        k: Optional[int] = None
    ) -> List[Tuple[str, float, int]]:
        """
        Search for similar chunks using TF-IDF
        
        Args:
            query: Query text
            vector_store: Fallback vector store
            chunks: Original text chunks
            k: Number of results to return
            
        Returns:
            List of tuples (chunk_text, similarity_score, chunk_id)
        """
        try:
            if k is None:
                k = min(self.settings.max_results, len(chunks))
            
            logger.info(f"Searching for top {k} similar chunks using TF-IDF")
            
            # Search in vector store
            similarities, indices = vector_store.search(query, k)
            
            # Prepare results
            results = []
            for i, (similarity, chunk_idx) in enumerate(zip(similarities, indices)):
                if chunk_idx < len(chunks) and similarity >= self.settings.similarity_threshold * 0.5:  # Lower threshold for TF-IDF
                    results.append((
                        chunks[chunk_idx],
                        float(similarity),
                        int(chunk_idx)
                    ))
            
            logger.info(f"Found {len(results)} relevant chunks using TF-IDF")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search similar chunks with TF-IDF: {e}")
            raise EmbeddingError(f"TF-IDF similarity search failed: {str(e)}")
    
    async def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Dummy method for compatibility"""
        logger.warning("create_embeddings called on fallback service")
        return np.zeros((len(texts), 100))  # Dummy embeddings
