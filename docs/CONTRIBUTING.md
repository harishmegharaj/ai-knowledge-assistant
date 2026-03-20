"""Contributing Guidelines"""

# Contributing Guide

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/yourusername/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

### 2. Set Up Development Environment
```bash
python install.py
pip install -e ".[dev]"
```

### 3. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## Code Style

### Python Style Guide - PEP 8

We follow PEP 8 with these preferences:
- Line length: 100 characters
- Use type hints for all functions
- Google-style docstrings

### Format Code
```bash
black src/
isort src/
```

### Lint Code
```bash
flake8 src/
mypy src/
```

## Testing

### Run Tests
```bash
pytest tests/
pytest tests/ --cov=src  # With coverage
pytest tests/ -v  # Verbose
```

### Write Tests
- Place tests in `tests/test_*.py`
- Use `pytest` fixtures for setup
- Mock external services
- Aim for 80%+ coverage

## Documentation

### Update README
- Keep examples up-to-date
- Document new features
- Include usage examples

### Add Docstrings
```python
def function_name(param1: str, param2: int) -> str:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is invalid
    """
    pass
```

## Commit Messages

### Format
```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests

### Example
```
feat: add document deletion endpoint

Added DELETE /documents/{doc_id} endpoint to remove
documents from the knowledge base.

Closes #123
```

## Pull Request Process

### Before Submitting
1. [ ] Code formatted with `black`
2. [ ] Tests pass: `pytest`
3. [ ] Linting passes: `flake8`
4. [ ] Type checking passes: `mypy`
5. [ ] Documentation updated
6. [ ] Commit messages follow convention

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] No breaking changes
```

## Adding Features

### 1. Database Backend
1. Create `src/vector_db/xxx_store.py`
2. Inherit from `VectorStoreInterface`
3. Implement all abstract methods
4. Add tests in `tests/test_xxx_store.py`
5. Update `factory.py`
6. Document in `docs/VECTOR_DB_GUIDE.md`

### 2. API Endpoint
1. Add Pydantic model in `src/api/main.py`
2. Create route handler
3. Add error handling
4. Write tests
5. Update API documentation

### 3. CLI Command
1. Add function in `src/api/cli.py`
2. Use Click decorators
3. Format output with Rich
4. Test manual execution

## Issue Guidelines

### Report Bug
Include:
- Python version
- Environment (OS)
- Reproduction steps
- Expected vs actual behavior
- Error message/traceback
- Environment variables used

### Request Feature
Include:
- Use case description
- Expected behavior
- Example usage
- Why it's needed

## Review Process

### Code Review
- Automated checks (linting, tests)
- Manual review by maintainers
- Addressing feedback
- Final approval

### Timeline
- Small changes: 1-2 days
- Major changes: 1 week
- Emergency fixes: ASAP

## Release Process

### Version Numbering
We follow semantic versioning: `MAJOR.MINOR.PATCH`

### Steps
1. Update version in `src/__init__.py`
2. Update `CHANGELOG.md`
3. Create release branch
4. Create GitHub release
5. Publish to PyPI

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md`
- Release notes
- GitHub acknowledgments

## Questions?

- Open an issue for clarification
- Check existing issues/PRs
- Read the documentation
- Ask in discussions

Thank you for contributing!
