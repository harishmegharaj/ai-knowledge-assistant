"""Document processing utilities"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Utility for processing documents before adding to vector store"""
    
    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> List[str]:
        """Split text into chunks with overlap
        
        Args:
            text: Text to split
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start = end - chunk_overlap
        
        return chunks
    
    @staticmethod
    def load_file(file_path: str) -> str:
        """Load text from file
        
        Args:
            file_path: Path to file
            
        Returns:
            File content
        """
        try:
            path = Path(file_path)
            if path.suffix == ".pdf":
                logger.warning("PDF processing requires PyPDF2 or similar library")
                return ""
            elif path.suffix in [".txt", ".md"]:
                return path.read_text(encoding="utf-8")
            else:
                return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return ""
    
    @staticmethod
    def process_documents(
        documents: List[Dict[str, str]],
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> tuple[List[str], List[Dict[str, Any]]]:
        """Process list of documents
        
        Args:
            documents: List of dicts with 'content' and optional 'source'
            chunk_size: Chunk size for splitting
            chunk_overlap: Overlap for chunks
            
        Returns:
            Tuple of (chunked_texts, metadata)
        """
        texts = []
        metadata = []
        
        for doc in documents:
            content = doc.get("content", "")
            source = doc.get("source", "unknown")
            
            # Split content into chunks
            chunks = DocumentProcessor.split_text(
                content,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            
            for chunk in chunks:
                texts.append(chunk)
                metadata.append({
                    "source": source,
                    "length": len(chunk),
                    **{k: v for k, v in doc.items() if k not in ["content", "source"]},
                })
        
        logger.info(f"Processed {len(documents)} documents into {len(texts)} chunks")
        return texts, metadata
