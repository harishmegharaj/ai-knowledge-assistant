"""Weaviate vector database implementation"""

import logging
from typing import List, Dict, Any, Tuple, Optional
import uuid

from sentence_transformers import SentenceTransformer
import weaviate
from weaviate.classes.config import Configure, Property
from weaviate.classes.query import MetadataQuery

from .base import VectorStoreInterface

logger = logging.getLogger(__name__)


class WeaviateVectorStore(VectorStoreInterface):
    """Weaviate vector database implementation"""
    
    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        collection_name: str = "KnowledgeBase",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        embedding_dim: int = 384,
    ):
        """Initialize Weaviate vector store
        
        Args:
            url: Weaviate server URL
            api_key: Optional API key for authentication
            collection_name: Collection name in Weaviate
            embedding_model: Embedding model name
            embedding_dim: Embedding dimension
        """
        self.url = url
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        
        # Initialize embeddings
        self.embeddings = SentenceTransformer(embedding_model)
        
        # Initialize Weaviate client
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        self.client = weaviate.connect_to_local(
            host=url.split("://")[-1].split(":")[0],
            port=int(url.split(":")[-1]) if ":" in url else 8080,
            headers=headers,
        )
        
        # Create or get collection
        self._init_collection()
        self.collection = self.client.collections.get(collection_name)
        
        logger.info(f"Initialized Weaviate vector store: {collection_name}")
    
    def _init_collection(self) -> None:
        """Create Weaviate collection if it doesn't exist"""
        try:
            if self.client.collections.exists(self.collection_name):
                logger.info(f"Using existing Weaviate collection: {self.collection_name}")
            else:
                logger.info(f"Creating new Weaviate collection: {self.collection_name}")
                self.client.collections.create(
                    name=self.collection_name,
                    vectorizer_config=Configure.Vectorizer.none(),
                    vector_index_config=Configure.VectorIndex.hnsw(),
                    properties=[
                        Property(name="text", data_type="text"),
                        Property(name="source", data_type="text"),
                        Property(name="metadata", data_type="object"),
                    ],
                )
        except Exception as e:
            logger.error(f"Error initializing Weaviate collection: {e}")
            raise
    
    async def add_texts(
        self,
        texts: List[str],
        metadata: List[Dict[str, Any]] = None,
        **kwargs
    ) -> List[str]:
        """Add texts to Weaviate collection
        
        Args:
            texts: List of texts to add
            metadata: List of metadata dicts
            
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
        
        # Add to Weaviate
        logger.info(f"Adding {len(texts)} texts to Weaviate collection")
        with self.collection.batch.dynamic() as batch:
            for id_, text, embedding, meta in zip(ids, texts, embeddings, metadata):
                batch.add_object(
                    uuid=id_,
                    properties={
                        "text": text,
                        "source": meta.get("source", "unknown"),
                        "metadata": meta,
                    },
                    vector=embedding,
                )
        
        logger.info(f"Successfully added {len(ids)} texts to Weaviate")
        return ids
    
    async def search(
        self,
        query: str,
        k: int = 5,
        **kwargs
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for similar texts in Weaviate
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (text, score, metadata) tuples
        """
        # Get query embedding
        query_embedding = self.embeddings.encode(query, convert_to_list=True)
        
        # Search Weaviate
        logger.info(f"Searching Weaviate for top {k} similar documents")
        results = self.collection.query.near_vector(
            near_vector=query_embedding,
            limit=k,
            return_metadata=MetadataQuery(distance=True),
        ).objects
        
        # Extract results
        output = []
        for obj in results:
            text = obj.properties.get("text", "")
            score = 1.0 - obj.metadata.distance  # Convert distance to similarity
            meta = obj.properties.get("metadata", {})
            output.append((text, score, meta))
        
        return output
    
    async def delete(self, ids: List[str], **kwargs) -> bool:
        """Delete texts by ID from Weaviate
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Deleting {len(ids)} documents from Weaviate")
            for id_ in ids:
                self.collection.data.delete_by_id(id_)
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Weaviate collection statistics
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            stats = self.client.collections.get(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "url": self.url,
                "total_objects": stats.aggregate.over_all(total_count=True).total_count,
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
    
    async def get_categories(self) -> List[str]:
        """Get all unique categories in the store
        
        Returns:
            List of unique category names
        """
        try:
            # This is a simplified implementation
            # In a real Weaviate setup, you'd query the collection metadata
            return ["HR", "Legal", "Finance"]  # Placeholder
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def close(self) -> None:
        """Close Weaviate client connection"""
        if self.client:
            self.client.close()
