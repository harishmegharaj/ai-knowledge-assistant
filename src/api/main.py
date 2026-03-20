"""FastAPI application"""

import logging
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import Settings, LogConfig
from src.ai_assistant import AIAssistant
from src.ai_assistant.document_processor import DocumentProcessor

# Setup logging
LogConfig.setup_logging("INFO", "json")
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Global assistant instance
assistant: Optional[AIAssistant] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI"""
    global assistant
    # Startup
    logger.info("Starting AI Knowledge Assistant API")
    try:
        assistant = AIAssistant(settings)
        logger.info("Assistant initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize assistant: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down API")


# Create FastAPI app
app = FastAPI(
    title="AI Knowledge Assistant",
    description="Production-grade AI Knowledge Assistant with LangChain and Vector Databases",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class Document(BaseModel):
    """Document model"""
    content: str = Field(..., description="Document content")
    source: Optional[str] = Field(None, description="Document source")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class QueryRequest(BaseModel):
    """Query request model"""
    query: str = Field(..., description="User query")
    top_k: Optional[int] = Field(5, description="Number of results")
    stream: Optional[bool] = Field(False, description="Stream response")


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str = Field(..., description="Generated answer")
    sources: List[dict] = Field(..., description="Source documents")
    confidence: float = Field(..., description="Confidence score")


class DocumentResponse(BaseModel):
    """Document response model"""
    doc_ids: List[str] = Field(..., description="Added document IDs")


class StatsResponse(BaseModel):
    """Statistics response model"""
    stats: dict = Field(..., description="Assistant statistics")


# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/documents/add", response_model=DocumentResponse)
async def add_documents(documents: List[Document]):
    """Add documents to knowledge base
    
    Args:
        documents: List of documents to add
        
    Returns:
        DocumentResponse with added document IDs
    """
    if not assistant:
        raise HTTPException(status_code=500, detail="Assistant not initialized")
    
    try:
        # Process documents
        docs_list = [
            {
                "content": doc.content,
                "source": doc.source or "unknown",
                **(doc.metadata or {}),
            }
            for doc in documents
        ]
        
        texts, metadata = DocumentProcessor.process_documents(
            docs_list,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        
        # Add to assistant
        doc_ids = await assistant.add_documents(texts, metadata)
        
        logger.info(f"Added {len(doc_ids)} document chunks")
        return DocumentResponse(doc_ids=doc_ids)
    
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base
    
    Args:
        request: Query request
        
    Returns:
        QueryResponse with answer and sources
    """
    if not assistant:
        raise HTTPException(status_code=500, detail="Assistant not initialized")
    
    try:
        result = await assistant.query(
            query=request.query,
            top_k=request.top_k,
            stream=request.stream,
        )
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from knowledge base
    
    Args:
        doc_id: Document ID
        
    Returns:
        Success message
    """
    if not assistant:
        raise HTTPException(status_code=500, detail="Assistant not initialized")
    
    try:
        success = await assistant.delete_documents([doc_id])
        if success:
            return {"message": "Document deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete document")
    
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats", response_model=StatsResponse)
async def get_statistics():
    """Get assistant statistics
    
    Returns:
        StatsResponse with statistics
    """
    if not assistant:
        raise HTTPException(status_code=500, detail="Assistant not initialized")
    
    try:
        stats = await assistant.get_stats()
        return StatsResponse(stats=stats)
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
    )
