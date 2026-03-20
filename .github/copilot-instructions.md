"""GitHub Copilot instructions for the AI Knowledge Assistant project"""

# AI Knowledge Assistant - Development Guidelines

## Project Overview

Production-grade AI Knowledge Assistant built with:
- **Python 3.9+** (Latest stable)
- **LangChain 0.1+** for LLM orchestration
- **Vector Databases**: Pinecone, FAISS, Weaviate
- **FastAPI** for REST API
- **Async/Await** for scalability

## Code Style & Standards

- Follow PEP 8 and use `black` for formatting
- Use type hints for all functions
- 100-character line length
- Use async/await for I/O operations
- Comprehensive docstrings (Google style)

## Key Components

### Core Modules

1. **src/config/settings.py** - Pydantic configuration management
2. **src/ai_assistant/__init__.py** - Main AIAssistant class
3. **src/vector_db/*** - Database implementations (abstract + 3 concrete)
4. **src/api/main.py** - FastAPI REST endpoints
5. **src/api/cli.py** - CLI interface

### Features to Maintain

- Multi-vector database support via factory pattern
- Async document processing with chunking
- Streaming LLM responses
- Metadata preservation
- Error logging and handling

## Development Workflow

1. Create feature branch
2. Update relevant modules
3. Add tests in `tests/`
4. Run linting: `flake8 src/`
5. Format code: `black src/`
6. Run tests: `pytest tests/`
7. Submit PR with documentation

## Important Constants

- Default chunk size: 500 tokens
- Default chunk overlap: 50 tokens
- Default top-k results: 5
- Default embedding dimension: 384
- Supported Python: 3.9+

## Database Configuration

- **Pinecone**: Cloud-based, requires API key
- **FAISS**: Local storage, CPU-friendly
- **Weaviate**: Self-hosted or cloud

Switch via `VECTOR_DB_TYPE` env variable.

## Common Tasks

### Adding new vector database backend
1. Create file in `src/vector_db/xxx_store.py`
2. Inherit from `VectorStoreInterface`
3. Implement all abstract methods
4. Add to factory in `src/vector_db/factory.py`

### Adding API endpoint
1. Create Pydantic model in `src/api/main.py`
2. Add route with appropriate decorators
3. Use assistant methods for operations
4. Add error handling

### Extending CLI
1. Add command in `src/api/cli.py`
2. Use Click decorators and options
3. Use Rich console for formatting
4. Add asyncio support for async operations

## Testing Guidelines

- Mock external dependencies
- Use pytest fixtures for setup
- Test error cases and edge cases
- Aim for 80%+ code coverage
- Use async test decorators: `@pytest.mark.asyncio`

## Deployment Checklist

- [ ] All environment variables configured
- [ ] Vector database initialized
- [ ] Dependencies installed: `python install.py`
- [ ] Tests passing: `pytest tests/`
- [ ] Linting passes: `flake8 src/`
- [ ] Type checking: `mypy src/`
- [ ] API health check: `curl http://localhost:8000/health`

## Security Considerations

- Store API keys in .env (not in repo)
- Validate user inputs
- Implement rate limiting
- Add authentication to API
- Sanitize document content
- Use HTTPS in production

## Performance Tips

- Use FAISS locally for development (faster)
- Use Pinecone for production (scalable)
- Optimize chunk size for your use case
- Cache embeddings when possible
- Use batch operations for bulk documents

## Troubleshooting

### Assistant initialization fails
- Check OPENAI_API_KEY is set
- Verify vector database credentials
- Check network connectivity

### Query returns empty results
- Verify documents were added
- Check chunk size settings
- Try different top_k values

### API server won't start
- Check port availability
- Verify host/port configuration
- Check for process already running

## Useful Commands

```bash
# Run API server
python -m uvicorn src.api.main:app --reload

# Run tests
pytest tests/ -v

# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/

# Generate coverage
pytest --cov=src tests/

# CLI usage
python -m src.api.cli --help
```

## References

- Project root: `/Users/harishashokmegharaj/reactnext/AIML`
- Main config: `src/config/settings.py`
- API spec: `src/api/main.py`
- Examples: `examples/basic_usage.py`
