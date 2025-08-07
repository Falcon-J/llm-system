"""
Custom exceptions for the application
"""


class BaseAppException(Exception):
    """Base exception for the application"""
    pass


class DocumentProcessingError(BaseAppException):
    """Raised when document processing fails"""
    pass


class EmbeddingError(BaseAppException):
    """Raised when embedding operations fail"""
    pass


class LLMError(BaseAppException):
    """Raised when LLM operations fail"""
    pass


class VectorStoreError(BaseAppException):
    """Raised when vector store operations fail"""
    pass


class RetrievalError(BaseAppException):
    """Raised when retrieval operations fail"""
    pass
