"""Vector Database interface and abstract base class"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple


class VectorStoreInterface(ABC):
    """Abstract base class for vector storage implementations"""
    
    @abstractmethod
    async def add_texts(
        self, texts: List[str], metadata: List[Dict[str, Any]] = None, **kwargs
    ) -> List[str]:
        """Add texts to the vector store
        
        Args:
            texts: List of text strings to add
            metadata: Optional list of metadata dicts
            
        Returns:
            List of document IDs
        """
        pass
    
    @abstractmethod
    async def search(
        self, query: str, k: int = 5, **kwargs
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for similar texts
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (text, score, metadata) tuples
        """
        pass
    
    @abstractmethod
    async def delete(self, ids: List[str], **kwargs) -> bool:
        """Delete texts by ID
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics
        
        Returns:
            Dictionary with store statistics
        """
        pass
