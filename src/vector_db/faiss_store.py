"""FAISS vector database implementation"""

import logging
import os
import pickle
from typing import List, Dict, Any, Tuple, Optional
import uuid

import numpy as np
from sentence_transformers import SentenceTransformer

from .base import VectorStoreInterface

logger = logging.getLogger(__name__)


class FAISSVectorStore(VectorStoreInterface):
    """FAISS vector database implementation for local storage"""
    
    def __init__(
        self,
        index_path: str,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        embedding_dim: int = 384,
    ):
        """Initialize FAISS vector store
        
        Args:
            index_path: Path to store FAISS index
            embedding_model: Embedding model name
            embedding_dim: Embedding dimension
        """
        import faiss
        
        self.faiss = faiss
        self.index_path = index_path
        self.embedding_dim = embedding_dim
        self.embeddings = SentenceTransformer(embedding_model)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(index_path) or ".", exist_ok=True)
        
        # Load or create index
        self._init_index()
        self.metadata_store = {}
        self._load_metadata()
        
        logger.info(f"Initialized FAISS vector store at {index_path}")
    
    def _init_index(self) -> None:
        """Initialize FAISS index"""
        index_file = f"{self.index_path}.faiss"
        
        if os.path.exists(index_file):
            logger.info(f"Loading existing FAISS index from {index_file}")
            self.index = self.faiss.read_index(index_file)
        else:
            logger.info(f"Creating new FAISS index")
            self.index = self.faiss.IndexFlatL2(self.embedding_dim)
    
    def _load_metadata(self) -> None:
        """Load metadata from file"""
        metadata_file = f"{self.index_path}.pkl"
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, "rb") as f:
                    self.metadata_store = pickle.load(f)
                logger.info(f"Loaded {len(self.metadata_store)} metadata entries")
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
                self.metadata_store = {}
    
    def _save_metadata(self) -> None:
        """Save metadata to file"""
        metadata_file = f"{self.index_path}.pkl"
        try:
            with open(metadata_file, "wb") as f:
                pickle.dump(self.metadata_store, f)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def _save_index(self) -> None:
        """Save FAISS index to file"""
        index_file = f"{self.index_path}.faiss"
        try:
            self.faiss.write_index(self.index, index_file)
            logger.info(f"Saved FAISS index to {index_file}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    async def add_texts(
        self,
        texts: List[str],
        metadata: List[Dict[str, Any]] = None,
        **kwargs
    ) -> List[str]:
        """Add texts to FAISS index
        
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
        embeddings = np.array(embeddings, dtype=np.float32)
        
        # Add to index
        logger.info(f"Adding {len(embeddings)} vectors to FAISS")
        self.index.add(embeddings)
        
        # Store metadata
        for id_, text, meta in zip(ids, texts, metadata):
            meta["text"] = text
            self.metadata_store[id_] = meta
        
        # Save to disk
        self._save_index()
        self._save_metadata()
        
        logger.info(f"Successfully added {len(ids)} texts to FAISS")
        return ids
    
    async def search(
        self,
        query: str,
        k: int = 5,
        **kwargs
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for similar texts in FAISS
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (text, score, metadata) tuples
        """
        # Get query embedding
        query_embedding = self.embeddings.encode(query, convert_to_list=True)
        query_embedding = np.array([query_embedding], dtype=np.float32)
        
        # Search FAISS
        logger.info(f"Searching FAISS for top {k} similar documents")
        distances, indices = self.index.search(query_embedding, k)
        
        # Extract results
        output = []
        stored_ids = list(self.metadata_store.keys())
        
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:  # Invalid index
                continue
            
            if idx < len(stored_ids):
                doc_id = stored_ids[idx]
                meta = self.metadata_store.get(doc_id, {})
                text = meta.get("text", "")
                score = 1.0 / (1.0 + distance)  # Convert distance to similarity score
                meta = {k: v for k, v in meta.items() if k != "text"}
                output.append((text, score, meta))
        
        return output
    
    async def delete(self, ids: List[str], **kwargs) -> bool:
        """Delete texts by ID from FAISS
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            True if successful
        """
        try:
            logger.info(f"Deleting {len(ids)} documents from FAISS")
            for id_ in ids:
                if id_ in self.metadata_store:
                    del self.metadata_store[id_]
            
            self._save_metadata()
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get FAISS index statistics
        
        Returns:
            Dictionary with index statistics
        """
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.embedding_dim,
            "index_path": self.index_path,
            "stored_documents": len(self.metadata_store),
        }
