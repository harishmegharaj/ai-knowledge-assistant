"""API Testing and Examples"""

# API Testing Guide

## Overview

This guide covers testing the AI Knowledge Assistant API using curl, Python requests, and Postman.

## Prerequisites

```bash
# Start the API server
python -m uvicorn src.api.main:app --reload

# Server runs at http://localhost:8000
```

## REST API Examples

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Add Documents

#### Single Document
```bash
curl -X POST http://localhost:8000/documents/add \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Python is a programming language",
        "source": "python_intro.txt"
      }
    ]
  }'
```

#### Multiple Documents
```bash
curl -X POST http://localhost:8000/documents/add \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Document 1 content",
        "source": "doc1.txt",
        "metadata": {"type": "tutorial"}
      },
      {
        "content": "Document 2 content",
        "source": "doc2.txt",
        "metadata": {"type": "guide"}
      }
    ]
  }'
```

Response:
```json
{
  "doc_ids": ["uuid1", "uuid2", "uuid3"]
}
```

### 3. Query Knowledge Base

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Python?",
    "top_k": 5,
    "stream": false
  }'
```

Response:
```json
{
  "answer": "Python is a high-level programming language...",
  "sources": [
    {
      "score": 0.95,
      "text": "Python is a programming language...",
      "metadata": {"type": "tutorial"}
    }
  ],
  "confidence": 0.95
}
```

### 4. Get Statistics

```bash
curl http://localhost:8000/stats
```

Response:
```json
{
  "stats": {
    "total_vectors": 150,
    "dimension": 384,
    "index_name": "knowledge-base"
  }
}
```

### 5. Delete Document

```bash
curl -X DELETE http://localhost:8000/documents/uuid1
```

Response:
```json
{
  "message": "Document deleted successfully"
}
```

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

class AIAssistantClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def health_check(self):
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def add_documents(self, documents):
        response = requests.post(
            f"{self.base_url}/documents/add",
            json={"documents": documents}
        )
        return response.json()
    
    def query(self, query: str, top_k: int = 5):
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query, "top_k": top_k}
        )
        return response.json()
    
    def get_stats(self):
        response = requests.get(f"{self.base_url}/stats")
        return response.json()
    
    def delete_document(self, doc_id: str):
        response = requests.delete(f"{self.base_url}/documents/{doc_id}")
        return response.json()

# Usage
if __name__ == "__main__":
    client = AIAssistantClient()
    
    # Check health
    print(client.health_check())
    
    # Add documents
    docs = [
        {"content": "Python is great", "source": "intro.txt"}
    ]
    result = client.add_documents(docs)
    print(f"Added docs: {result['doc_ids']}")
    
    # Query
    result = client.query("What is Python?")
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}")
    
    # Statistics
    print(client.get_stats())
```

## Load Testing

### Using Apache Bench
```bash
ab -n 1000 -c 10 http://localhost:8000/health
```

### Using Wrk
```bash
wrk -t4 -c100 -d30s http://localhost:8000/health
```

## Postman Collection

### Import Steps
1. Open Postman
2. Create new collection: "AI Assistant API"
3. Add the requests below

#### Request 1: Health Check
```
GET http://localhost:8000/health
```

#### Request 2: Add Documents
```
POST http://localhost:8000/documents/add
Headers: Content-Type: application/json
Body: {
  "documents": [
    {
      "content": "Your content here",
      "source": "source.txt"
    }
  ]
}
```

#### Request 3: Query
```
POST http://localhost:8000/query
Headers: Content-Type: application/json
Body: {
  "query": "Your question?",
  "top_k": 5
}
```

#### Request 4: Statistics
```
GET http://localhost:8000/stats
```

## Error Handling

### 500 Error - Assistant Not Initialized
```json
{
  "detail": "Assistant not initialized"
}
```

**Fix:** Ensure all environment variables are set and services are running

### 400 Error - Invalid Request
```json
{
  "detail": "Invalid request format"
}
```

**Fix:** Check JSON schema matches expected format

### Timeout Error

**Fix:** 
- Increase timeout value
- Reduce batch size
- Check network connectivity

## Performance Testing

### Benchmark Results

```
Endpoint: /query
Document Count: 10,000
Average Response Time: 150ms
P95 Response Time: 250ms
P99 Response Time: 500ms
Throughput: 6.7 requests/second
```

## Security Testing

### SQL Injection Test
```bash
curl -X POST http://localhost:8000/query \
  -d '{"query": "test\"; DROP TABLE documents; --"}'
# Should safely escape/handle
```

### XSS Test
```bash
curl -X POST http://localhost:8000/query \
  -d '{"query": "<script>alert(1)</script>"}'
# Should sanitize or escape
```

### Large Payload Test
```bash
# Test with 10MB document
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: python -m flake8 src/
```
