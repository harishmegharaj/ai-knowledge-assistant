# Development Makefile for AI Knowledge Assistant

.PHONY: help install dev test lint format clean run-api run-cli

help:
	@echo "Available commands:"
	@echo "  make setup         - Full setup with venv creation"
	@echo "  make install       - Install dependencies (requires venv)"
	@echo "  make dev           - Install dev dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean up generated files"
	@echo "  make run-api       - Run API server"
	@echo "  make run-cli       - Run CLI"
	@echo "  make coverage      - Generate coverage report"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"

setup:
	python install.py

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -rf htmlcov/ .coverage

run-api:
	python -m uvicorn src.api.main:app --reload

run-cli:
	python -m src.api.cli

coverage:
	pytest tests/ --cov=src --cov-report=html
	open htmlcov/index.html

docker-build:
	docker build -t ai-assistant:latest .

docker-run:
	docker run -p 8000:8000 --env-file .env ai-assistant:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

all: install dev test lint
	@echo "✓ All checks passed!"
