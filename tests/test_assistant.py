"""Unit tests for AI Assistant"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.config import Settings
from src.ai_assistant import AIAssistant


@pytest.fixture
def settings():
    """Create test settings"""
    return Settings(
        openai_api_key="sk-test123",
        vector_db_type="faiss",
        faiss_index_path="./test_index",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    )


@pytest.mark.asyncio
async def test_add_documents():
    """Test adding documents"""
    # This is a basic test structure
    # In production, you'd mock the vector store
    pass


@pytest.mark.asyncio
async def test_query():
    """Test querying the knowledge base"""
    pass


def test_settings_validation():
    """Test settings validation"""
    # Test invalid OpenAI key format
    with pytest.raises(ValueError):
        Settings(openai_api_key="invalid_key")


def test_settings_chunk_size_validation():
    """Test chunk size validation"""
    # Too small chunk size
    with pytest.raises(ValueError):
        Settings(chunk_size=50)
    
    # Too large chunk size
    with pytest.raises(ValueError):
        Settings(chunk_size=3000)
