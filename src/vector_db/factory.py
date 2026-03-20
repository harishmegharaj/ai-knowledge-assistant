"""Vector database factory and selector"""

import logging
from typing import Optional

from src.config import Settings
from .base import VectorStoreInterface

logger = logging.getLogger(__name__)


class VectorDBFactory:
    """Factory for creating vector database instances"""
    
    @staticmethod
    def create_vector_store(settings: Settings) -> VectorStoreInterface:
        """Create vector store based on configuration
        
        Args:
            settings: Application settings
            
        Returns:
            VectorStoreInterface implementation
            
        Raises:
            ValueError: If vector DB type is not supported
        """
        db_type = settings.vector_db_type.lower()
        
        if db_type == "pinecone":
            from .pinecone_store import PineconeVectorStore
            
            return PineconeVectorStore(
                api_key=settings.pinecone_api_key,
                index_name=settings.pinecone_index_name,
                environment=settings.pinecone_environment,
                embedding_model=settings.embedding_model,
                embedding_dim=settings.embedding_dimension,
            )
        
        elif db_type == "faiss":
            from .faiss_store import FAISSVectorStore
            
            return FAISSVectorStore(
                index_path=settings.faiss_index_path,
                embedding_model=settings.embedding_model,
                embedding_dim=settings.embedding_dimension,
            )
        
        elif db_type == "weaviate":
            from .weaviate_store import WeaviateVectorStore
            
            return WeaviateVectorStore(
                url=settings.weaviate_url,
                api_key=settings.weaviate_api_key or None,
                embedding_model=settings.embedding_model,
                embedding_dim=settings.embedding_dimension,
            )
        
        else:
            raise ValueError(
                f"Unsupported vector DB type: {db_type}. "
                f"Supported types: pinecone, faiss, weaviate"
            )
