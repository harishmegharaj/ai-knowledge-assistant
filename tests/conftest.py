"""Test utilities"""

import pytest
from typing import Dict, Any
from unittest.mock import AsyncMock


@pytest.fixture
def mock_settings():
    """Create mock settings"""
    settings = {
        "openai_api_key": "sk-test123",
        "vector_db_type": "faiss",
        "faiss_index_path": "./test_index",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    }
    return settings


@pytest.fixture
def sample_documents() -> list[Dict[str, str]]:
    """Create sample documents for testing"""
    return [
        {
            "content": "Python is a high-level programming language",
            "source": "python_intro.txt",
        },
        {
            "content": "Machine learning is a subset of artificial intelligence",
            "source": "ml_basics.txt",
        },
    ]
