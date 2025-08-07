"""
Configuration settings for the application
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server Configuration
    port: int = int(os.getenv("PORT", 8000))  # Railway sets PORT automatically
    environment: str = os.getenv("ENVIRONMENT", "production")
    
    # Competition Authentication (DO NOT CHANGE)
    auth_token: str = "hackrx-api-token-2024"
    
    # OpenAI/OpenRouter Configuration
    openai_api_key: str
    openai_base_url: str = "https://openrouter.ai/api/v1"  # Default to OpenRouter
    llm_model: str = "openai/gpt-4o-mini"  # OpenRouter model format
    embedding_model: str = "text-embedding-3-small"  # Use smaller model for embeddings
    max_tokens: int = 500  # Optimized for competition efficiency
    temperature: float = 0.1  # Low temperature for consistent results
    
    # Document Processing
    max_doc_size_mb: int = 50
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Vector Search
    similarity_threshold: float = 0.7
    max_results: int = 10
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-detect API provider based on key format
        if self.openai_api_key.startswith('sk-or-'):
            # OpenRouter API
            self.openai_base_url = "https://openrouter.ai/api/v1"
            if self.llm_model == "gpt-4":
                self.llm_model = "openai/gpt-4o-mini"  # Use free model
        elif self.openai_api_key.startswith('sk-'):
            # Standard OpenAI API
            self.openai_base_url = "https://api.openai.com/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
