"""Pinecone vector database implementation"""

import logging
from typing import List, Dict, Any, Tuple, Optional
import uuid

from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

from .base import VectorStoreInterface

logger = logging.getLogger(__name__)


class PineconeVectorStore(VectorStoreInterface):
    """Pinecone vector database implementation"""
    
    def __init__(
        self,
        api_key: str,
        index_name: str,
        environment: str = "us-east-1-aws",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        embedding_dim: int = 384,
    ):
        """Initialize Pinecone vector store
        
        Args:
            api_key: Pinecone API key
            index_name: Index name
            environment: Pinecone environment
            embedding_model: Embedding model name
            embedding_dim: Embedding dimension
        """
        self.api_key = api_key
        self.index_name = index_name
        self.embedding_dim = embedding_dim
        
        # Initialize embeddings
        self.embeddings = SentenceTransformer(embedding_model)
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=api_key)
        
        # Create or get index
        self._init_index()
        self.index = self.pc.Index(index_name)
        
        logger.info(f"Initialized Pinecone vector store: {index_name}")
    
    def _init_index(self) -> None:
        """Create Pinecone index if it doesn't exist"""
        try:
            # Check if index exists
            indexes = self.pc.list_indexes()
            index_names = [idx.name for idx in indexes]
            
            if self.index_name not in index_names:
                logger.info(f"Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dim,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
            else:
                logger.info(f"Using existing Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error initializing Pinecone index: {e}")
            raise
    
    async def add_texts(
        self,
        texts: List[str],
        metadata: List[Dict[str, Any]] = None,
        batch_size: int = 100,
        **kwargs
    ) -> List[str]:
        """Add texts to Pinecone index
        
        Args:
            texts: List of texts to add
            metadata: List of metadata dicts
            batch_size: Batch size for upserting
            
        Returns:
            List of document IDs
        """
        if metadata is None:
            metadata = [{} for _ in texts]
        
        # Generate IDs
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # Get embeddings
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.embeddings.encode(texts, convert_to_list=True)
        
        # Prepare vectors for upsert
        vectors_to_upsert = []
        for id_, embedding, text, meta in zip(ids, embeddings, texts, metadata):
            meta["text"] = text
            vectors_to_upsert.append((id_, embedding, meta))
        
        # Upsert in batches
        logger.info(f"Upserting {len(vectors_to_upsert)} vectors to Pinecone")
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i : i + batch_size]
            self.index.upsert(vectors=batch)
        
        logger.info(f"Successfully added {len(ids)} texts to Pinecone")
        return ids
    
    async def search(
        self,
        query: str,
        k: int = 5,
        **kwargs
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for similar texts in Pinecone
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (text, score, metadata) tuples
        """
        # Get query embedding
        query_embedding = self.embeddings.encode(query, convert_to_list=True)
        
        # Search Pinecone
        logger.info(f"Searching Pinecone for top {k} similar documents")
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True,
        )
        
        # Extract results
        output = []
        for match in results.matches:
            text = match.metadata.get("text", "")
            score = match.score
            meta = {k: v for k, v in match.metadata.items() if k != "text"}
            output.append((text, score, meta))
        
        return output
    
    async def delete(self, ids: List[str], **kwargs) -> bool:
        """Delete texts by ID from Pinecone
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Deleting {len(ids)} documents from Pinecone")
            self.index.delete(ids=ids)
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Pinecone index statistics
        
        Returns:
            Dictionary with index statistics
        """
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_name": self.index_name,
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
