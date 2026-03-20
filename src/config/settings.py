"""Application settings and configuration"""

import logging
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # LLM Configuration
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    openai_model: str = Field(default="gpt-4", description="OpenAI model name")
    
    # Vector Database Configuration
    vector_db_type: Literal["pinecone", "faiss", "weaviate"] = Field(
        default="pinecone", description="Vector database type"
    )
    pinecone_api_key: str = Field(default="", description="Pinecone API Key")
    pinecone_environment: str = Field(default="us-east-1-aws", description="Pinecone environment")
    pinecone_index_name: str = Field(default="knowledge-base", description="Pinecone index name")
    
    weaviate_url: str = Field(default="http://localhost:8080", description="Weaviate URL")
    weaviate_api_key: str = Field(default="", description="Weaviate API Key")
    
    faiss_index_path: str = Field(default="./data/faiss_index", description="FAISS index path")
    
    # Embedding Configuration
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model name"
    )
    embedding_dimension: int = Field(default=384, description="Embedding dimension")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=4, description="Number of API workers")
    debug_mode: bool = Field(default=False, description="Debug mode")
    
    # Application Settings
    max_context_length: int = Field(default=4000, description="Maximum context length")
    chunk_size: int = Field(default=500, description="Text chunk size")
    chunk_overlap: int = Field(default=50, description="Chunk overlap size")
    top_k_results: int = Field(default=5, description="Top K search results")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: Literal["json", "text"] = Field(default="json", description="Log format")
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        """Validate OpenAI API key format"""
        if v and not v.startswith("sk-"):
            raise ValueError("OpenAI API key must start with 'sk-'")
        return v
    
    @field_validator("chunk_size")
    @classmethod
    def validate_chunk_size(cls, v: int) -> int:
        """Validate chunk size is reasonable"""
        if v < 100 or v > 2000:
            raise ValueError("Chunk size must be between 100 and 2000")
        return v


class LogConfig:
    """Logging configuration"""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @staticmethod
    def setup_logging(level: str = "INFO", format_type: str = "text") -> None:
        """Setup application logging"""
        logging.basicConfig(
            level=getattr(logging, level),
            format=LogConfig.format if format_type == "text" else '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
        )
