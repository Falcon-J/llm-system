"""
Utility functions for text processing and analysis
"""

import re
import string
from typing import List, Dict, Set
from collections import Counter


class TextAnalyzer:
    """Utility class for text analysis and processing"""
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3, max_keywords: int = 20) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            min_length: Minimum keyword length
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of important keywords
        """
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split into words
        words = text.split()
        
        # Filter words by length and remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'our',
            'their', 'not', 'no', 'yes', 'can', 'may', 'might', 'must', 'shall'
        }
        
        filtered_words = [
            word for word in words 
            if len(word) >= min_length and word not in stop_words
        ]
        
        # Count word frequency
        word_counts = Counter(filtered_words)
        
        # Return most common words
        return [word for word, _ in word_counts.most_common(max_keywords)]
    
    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """
        Calculate simple text similarity using word overlap
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        # Extract keywords from both texts
        keywords1 = set(TextAnalyzer.extract_keywords(text1))
        keywords2 = set(TextAnalyzer.extract_keywords(text2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(keywords1.intersection(keywords2))
        union = len(keywords1.union(keywords2))
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def extract_entities(text: str) -> Dict[str, List[str]]:
        """
        Extract basic entities from text (numbers, dates, etc.)
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of entity types and their values
        """
        entities = {
            'numbers': [],
            'percentages': [],
            'dates': [],
            'money': [],
            'time_periods': []
        }
        
        # Extract numbers
        numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', text)
        entities['numbers'] = numbers
        
        # Extract percentages
        percentages = re.findall(r'\b\d+(?:\.\d+)?%\b', text)
        entities['percentages'] = percentages
        
        # Extract money amounts
        money = re.findall(r'[\$€£¥]\s*\d+(?:,\d{3})*(?:\.\d{2})?', text)
        entities['money'] = money
        
        # Extract basic date patterns
        dates = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b', text)
        entities['dates'] = dates
        
        # Extract time periods
        time_periods = re.findall(r'\b\d+\s*(?:days?|weeks?|months?|years?|hours?|minutes?)\b', text, re.IGNORECASE)
        entities['time_periods'] = time_periods
        
        return entities
    
    @staticmethod
    def clean_for_embedding(text: str) -> str:
        """
        Clean text specifically for embedding generation
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text optimized for embeddings
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Normalize quotes and dashes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        return text.strip()


class DocumentMetrics:
    """Utility class for calculating document metrics"""
    
    @staticmethod
    def calculate_readability_score(text: str) -> float:
        """
        Calculate a simple readability score
        
        Args:
            text: Input text
            
        Returns:
            Readability score (higher = more readable)
        """
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        
        if sentences == 0 or words == 0:
            return 0.0
        
        avg_sentence_length = words / sentences
        
        # Simple score: shorter sentences are more readable
        # Scale from 0-100, where 100 is most readable
        score = max(0, 100 - (avg_sentence_length - 10) * 2)
        return min(score, 100)
    
    @staticmethod
    def calculate_complexity_score(text: str) -> float:
        """
        Calculate text complexity based on various factors
        
        Args:
            text: Input text
            
        Returns:
            Complexity score (0-1, higher = more complex)
        """
        words = text.split()
        if not words:
            return 0.0
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Count complex words (>6 characters)
        complex_words = sum(1 for word in words if len(word) > 6)
        complex_ratio = complex_words / len(words)
        
        # Count sentences
        sentences = text.count('.') + text.count('!') + text.count('?')
        avg_sentence_length = len(words) / max(sentences, 1)
        
        # Combine factors into complexity score
        complexity = (
            (avg_word_length - 4) / 10 * 0.3 +  # Word length factor
            complex_ratio * 0.4 +  # Complex words factor
            (avg_sentence_length - 15) / 30 * 0.3  # Sentence length factor
        )
        
        return max(0, min(complexity, 1))
    
    @staticmethod
    def extract_document_stats(text: str) -> Dict[str, int]:
        """
        Extract basic document statistics
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of document statistics
        """
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        paragraphs = len([p for p in text.split('\n') if p.strip()])
        
        return {
            'characters': len(text),
            'words': len(words),
            'sentences': sentences,
            'paragraphs': paragraphs,
            'avg_words_per_sentence': len(words) / max(sentences, 1),
            'avg_chars_per_word': len(text.replace(' ', '')) / max(len(words), 1)
        }
