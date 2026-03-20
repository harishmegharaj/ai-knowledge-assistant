# AI Knowledge Assistant - Production-Grade

A production-ready AI Knowledge Assistant built with Python, LangChain, and support for multiple vector databases (Pinecone, FAISS, Weaviate).

## 🚀 Features

- **Multi-Vector Database Support**: Choose between Pinecone, FAISS (local storage), or Weaviate
- **LangChain Integration**: Powerful LLM orchestration with customizable chains
- **Production-Ready**: Comprehensive logging, error handling, and monitoring
- **Multiple Interfaces**: REST API, CLI, and Python library
- **Async/Await Support**: Fully asynchronous architecture
- **Document Processing**: Smart chunking with overlap for better context
- **Type Safety**: Full type hints throughout the codebase
- **Configuration Management**: Environment-based configuration

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key (or compatible LLM)
- Vector database account (Pinecone/Weaviate) or local storage (FAISS)

## 🔧 Installation

1. **Clone the repository**
```bash
cd /Users/harishashokmegharaj/reactnext/AIML
```

2. **Run automated setup**
```bash
python install.py
```

This will:
- Create a virtual environment
- Install all dependencies
- Verify the installation

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and preferences
```

## ⚙️ Configuration

Edit `.env` file with your settings:

```bash
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Vector Database Selection
VECTOR_DB_TYPE=pinecone  # Options: pinecone, faiss, weaviate

# Pinecone Settings (if using Pinecone)
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=knowledge-base

# Weaviate Settings (if using Weaviate)
WEAVIATE_URL=http://localhost:8080

# FAISS Settings (if using FAISS)
FAISS_INDEX_PATH=./data/faiss_index

# Application Settings
API_HOST=0.0.0.0
API_PORT=8000
MAX_CONTEXT_LENGTH=4000
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=5
```

## 🎯 Quick Start

### Using Python API

```python
import asyncio
from src.config import Settings
from src.ai_assistant import AIAssistant
from src.ai_assistant.document_processor import DocumentProcessor

async def main():
    # Initialize
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Add documents
    documents = [
        {
            "content": "Your document content here...",
            "source": "document.txt"
        }
    ]
    texts, metadata = DocumentProcessor.process_documents(documents)
    doc_ids = await assistant.add_documents(texts, metadata)
    
    # Query
    result = await assistant.query("Your question here?")
    print(result["answer"])

asyncio.run(main())
```

### Using REST API

```bash
# Start server
python -m uvicorn src.api.main:app --reload

# Add documents (in another terminal)
curl -X POST http://localhost:8000/documents/add \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Your document content",
        "source": "document.txt"
      }
    ]
  }'

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your question here?",
    "top_k": 5
  }'

# Get statistics
curl http://localhost:8000/stats

# Health check
curl http://localhost:8000/health
```

### Using CLI

```bash
# Add documents
python -m src.api.cli add_document --file document.txt --source "my-doc"

# Query
python -m src.api.cli query --query "Your question here?"

# Statistics
python -m src.api.cli stats
```

## 📁 Project Structure

```
AIML/
├── src/
│   ├── ai_assistant/           # Core assistant logic
│   │   ├── __init__.py        # Main AIAssistant class
│   │   └── document_processor.py
│   ├── api/                    # REST API and CLI
│   │   ├── main.py            # FastAPI application
│   │   ├── cli.py             # CLI interface
│   │   └── __init__.py
│   ├── vector_db/             # Vector database implementations
│   │   ├── base.py            # Abstract interface
│   │   ├── pinecone_store.py
│   │   ├── faiss_store.py
│   │   ├── weaviate_store.py
│   │   └── factory.py         # Database factory
│   ├── config/                # Configuration
│   │   ├── settings.py        # Pydantic settings
│   │   └── __init__.py
│   └── __init__.py
├── tests/                      # Unit tests
├── examples/                   # Usage examples
├── docs/                       # Documentation
├── requirements.txt
├── install.py
├── pyproject.toml
├── .env.example
└── README.md
```

## 🗄️ Vector Database Setup

### Option 1: Pinecone (Cloud)

1. Create account at [pinecone.io](https://www.pinecone.io)
2. Get API key and environment
3. Configure in `.env`

### Option 2: FAISS (Local)

```bash
pip install faiss-cpu  # or faiss-gpu for GPU support
# FAISS stores data locally - no external setup needed
```

### Option 3: Weaviate (Self-hosted or Cloud)

```bash
# For local development with Docker:
docker run -p 8080:8080 semitechnologies/weaviate:latest

# Or use Weaviate Cloud at https://console.weaviate.cloud
```

## 🧪 Testing

```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

## 📊 Performance Considerations

- **Chunk Size**: Balance between context completeness (larger) and relevance (smaller)
- **Top-K Results**: More results = better coverage but slower responses
- **Embedding Model**: Larger models are slower but more accurate
- **Batch Processing**: Process documents in batches for better performance

## 🔐 Security Best Practices

1. Never commit `.env` file with real credentials
2. Use environment variables in production
3. Implement rate limiting for API endpoints
4. Add authentication to API routes
5. Validate and sanitize user inputs
6. Keep dependencies updated

## 🚨 Error Handling

The assistant includes comprehensive error handling:

- Invalid configuration raises `ValueError`
- Missing vector store raises `HTTPException` with 500 status
- Document processing errors are logged and reported
- Query failures return graceful error messages

## 📈 Monitoring and Logging

- All operations are logged with appropriate levels (INFO, WARNING, ERROR)
- JSON logging format for production deployments
- Performance metrics available via `/stats` endpoint
- Structured logging for easy parsing

## 🤝 Contributing

1. Follow PEP 8 style guide
2. Run `black` and `flake8` before committing
3. Add tests for new features
4. Update documentation

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review example usage
3. Check logs for error messages
4. Open an issue on GitHub

## 🔄 Advanced Usage

### Custom LLM Models

```python
from langchain.chat_models import ChatOllama

# Use local Ollama models
settings.openai_model = "local-model"  
# Requires custom implementation
```

### Custom Embeddings

```python
from langchain.embeddings import OpenAIEmbeddings

# Use OpenAI embeddings instead
embedding_model = "text-embedding-3-large"
```

### Hybrid Search

Combine vector and keyword search for better results - implement custom retriever combining BM25 and semantic search.

## 📚 Additional Resources

- [LangChain Documentation](https://docs.langchain.com)
- [Pinecone Docs](https://docs.pinecone.io)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [OpenAI API Reference](https://platform.openai.com/docs)
