"""API deployment guide"""

# Deployment Guide

## 1. Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Environment
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Run
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  ai-assistant:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - VECTOR_DB_TYPE=pinecone
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - PINECONE_ENVIRONMENT=us-east-1-aws
      - PINECONE_INDEX_NAME=knowledge-base
    volumes:
      - ./data:/app/data
    restart: always

  # Optional: Weaviate service
  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
```

## 2. Environment-Specific Configurations

### Development (.env.dev)
```
DEBUG_MODE=true
LOG_LEVEL=DEBUG
VECTOR_DB_TYPE=faiss
```

### Staging (.env.staging)
```
DEBUG_MODE=false
LOG_LEVEL=INFO
VECTOR_DB_TYPE=weaviate
```

### Production (.env.prod)
```
DEBUG_MODE=false
LOG_LEVEL=WARNING
VECTOR_DB_TYPE=pinecone
```

## 3. Kubernetes Deployment

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-assistant
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-assistant
  template:
    metadata:
      labels:
        app: ai-assistant
    spec:
      containers:
      - name: ai-assistant
        image: ai-assistant:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 4. Reverse Proxy Configuration

### Nginx
```nginx
upstream ai-assistant {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://ai-assistant;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check
    location /health {
        proxy_pass http://ai-assistant;
    }
}
```

## 5. Monitoring Setup

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
queries_total = Counter('queries_total', 'Total queries')
query_duration = Histogram('query_duration_seconds', 'Query duration')
documents_total = Counter('documents_total', 'Total documents added')
```

### Health Checks
```bash
# Local health check
curl http://localhost:8000/health

# Remote health check
curl https://api.example.com/health
```

## 6. Scaling Considerations

### Horizontal Scaling
- Run multiple instances behind load balancer
- Use shared vector database (Pinecone/Weaviate)
- Share session state via Redis if needed

### Vertical Scaling
- Increase container memory/CPU
- Use larger embedding models selectively
- Cache frequent queries

## 7. Monitoring & Logging

### ELK Stack Integration
```yaml
# Send logs to Elasticsearch
logging:
  handlers:
    elasticsearch:
      class: logging_es.ElasticsearchHandler
      es_hosts: ['localhost']
```

### CloudWatch Integration
```python
import watchtower
handler = watchtower.CloudWatchLogHandler()
logger.addHandler(handler)
```

## 8. Security Best Practices

### API Authentication
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/query")
async def query(request: QueryRequest, credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    # Validate token
    pass
```

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/query")
@limiter.limit("10/minute")
async def query(request: QueryRequest):
    pass
```

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

## 9. Performance Tuning

### Database Connection Pooling
```python
# Use connection pooling for better performance
engine = create_engine(
    "postgresql://user:password@localhost/dbname",
    pool_size=20,
    max_overflow=40,
)
```

### Caching Layer
```python
from functools import lru_cache

@lru_cache(maxsize=128)
async def get_frequent_documents(query: str):
    # Cache frequently used queries
    pass
```

## 10. Disaster Recovery

### Backup Strategy
```bash
# Regular backups of vector store
0 2 * * * /app/backup.sh >> /var/log/backup.log 2>&1

# Backup parameters
- Daily incremental backups
- Weekly full backups
- 30-day retention policy
- Test restores monthly
```

### Failover Setup
```yaml
# Active-passive failover
Primary: ai-assistant-1 (prod-cluster-1)
Standby: ai-assistant-2 (prod-cluster-2)
Heartbeat every 5 seconds
Failover timeout: 30 seconds
```
