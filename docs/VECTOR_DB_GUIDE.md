# Vector Database Comparison & Setup Guide

## Overview

This assistant supports three popular vector databases: Pinecone, FAISS, and Weaviate. Each has different strengths and use cases.

## 1. Pinecone (Cloud-Based)

### Pros
- ✅ Fully managed (no infrastructure)
- ✅ Scales automatically
- ✅ Global availability
- ✅ Metadata filtering
- ✅ Best for production at scale

### Cons
- ❌ Costs money
- ❌ Requires internet connection
- ❌ Less control over infrastructure
- ❌ API rate limits

### Setup
```bash
1. Create account at https://www.pinecone.io
2. Create an API key
3. Create an index (e.g., "knowledge-base")
4. Add to .env:
   PINECONE_API_KEY=your_key_here
   PINECONE_ENVIRONMENT=us-east-1-aws
   PINECONE_INDEX_NAME=knowledge-base
   VECTOR_DB_TYPE=pinecone
```

### Best For
- Production deployments
- Large-scale applications (100K+ documents)
- Teams with budget
- Global distribution needs

### Pricing
- Free tier: 1 index, 1M vectors
- Paid: $1/month per index + compute

### Configuration Tuning
```python
# Advanced Pinecone settings
index_config = {
    "dimension": 384,  # Match embedding dimension
    "metric": "cosine",  # or "euclidean", "dotproduct"
    "spec": ServerlessSpec(cloud="aws", region="us-east-1")
}
```

## 2. FAISS (Local Storage)

### Pros
- ✅ Completely free
- ✅ No network required
- ✅ Fast local operations
- ✅ Perfect for development
- ✅ Works offline

### Cons
- ❌ Stores locally (limited by disk/RAM)
- ❌ Single machine (not distributed)
- ❌ No built-in backup
- ❌ Limited metadata support

### Setup
```bash
# CPU version (recommended for most)
pip install faiss-cpu

# GPU version (faster for large operations)
pip install faiss-gpu

# Add to .env:
FAISS_INDEX_PATH=./data/faiss_index
VECTOR_DB_TYPE=faiss
```

### Best For
- Development and testing
- Small to medium projects
- Prototyping
- Learning
- Cost-sensitive deployments

### File Structure
```
your_project/
├── data/
│   ├── faiss_index.faiss    # Vector index
│   └── faiss_index.pkl       # Metadata
```

### Configuration Tuning
```python
# FAISS index types
import faiss

# Different index types for different use cases:
# IndexFlatL2: Exhaustive search, guaranteed exact results
# IndexHNSW: Fast approximate search (good default)
# IndexIVFFlat: Scalable for 1M+ vectors
```

## 3. Weaviate (Self-Hosted or Cloud)

### Pros
- ✅ Open-source option available
- ✅ Rich query capabilities
- ✅ GraphQL API
- ✅ Built-in classification
- ✅ Enterprise features

### Cons
- ❌ Operational overhead if self-hosted
- ❌ More complex setup
- ❌ Steeper learning curve
- ❌ Cloud version is expensive

### Setup - Local (Docker)
```bash
# Start Weaviate locally
docker run -d \
  -p 8080:8080 \
  -p 50051:50051 \
  semitechnologies/weaviate:latest

# Add to .env:
WEAVIATE_URL=http://localhost:8080
VECTOR_DB_TYPE=weaviate
```

### Setup - Cloud
```bash
1. Go to https://console.weaviate.cloud
2. Create an account
3. Deploy cluster
4. Get cluster URL and API key
5. Add to .env:
   WEAVIATE_URL=https://your-cluster.weaviate.network
   WEAVIATE_API_KEY=your_key_here
```

### Best For
- Enterprise deployments
- Complex querying needs
- Hybrid search (vector + keyword)
- Organizations preferring open-source

### Pricing
- Self-hosted: Free (you manage infrastructure)
- Cloud: ~$100-500/month depending on scale

## Comparison Table

| Feature | Pinecone | FAISS | Weaviate |
|---------|----------|-------|----------|
| Cost | Paid | Free | Free (self) / Paid (cloud) |
| Setup Complexity | Easy | Easy | Medium |
| Maintenance | None | Low | Medium-High |
| Scalability | Unlimited | Limited | High |
| Multi-machine | Yes | No | Yes |
| Metadata Support | Excellent | Basic | Excellent |
| Query Filtering | Yes | No | Yes |
| Vector Count | 100M+ | 10M+ | 100M+ |
| Speed | Fast | Very Fast | Fast |
| Online Learning | Yes | No | Yes |

## Migration Guide

### FAISS → Pinecone
```python
# Read from FAISS
faiss_store = FAISSVectorStore("./data/faiss_index")
texts, scores, metadata = await faiss_store.search("*", k=all)

# Write to Pinecone
pinecone_store = PineconeVectorStore(...)
await pinecone_store.add_texts(texts, metadata)
```

### Pinecone → FAISS
```python
# Query all from Pinecone
# Export and import to FAISS
# (Similar to above, reverse direction)
```

## Performance Benchmarks

Approximate performance on 100K document chunks:

| Operation | Pinecone | FAISS | Weaviate |
|-----------|----------|-------|----------|
| Add 100K docs | 2 min | 30 sec | 5 min |
| Query (top-5) | 50ms | 10ms | 100ms |
| Memory Usage | Cloud | 1-5GB | 5-10GB |
| Network | Required | None | Optional |

## Recommended Configurations

### Development
```bash
VECTOR_DB_TYPE=faiss
FAISS_INDEX_PATH=./data/faiss_index
# Fast iteration, no cost
```

### Staging
```bash
VECTOR_DB_TYPE=weaviate
WEAVIATE_URL=http://localhost:8080
# Test production-like setup
```

### Production (Small)
```bash
VECTOR_DB_TYPE=faiss
# If scale < 10M vectors
# Cost-effective and fast
```

### Production (Large)
```bash
VECTOR_DB_TYPE=pinecone
PINECONE_ENVIRONMENT=us-east-1-aws
# Scales automatically, reliable
```

## Switching Databases

The factory pattern makes switching easy:

```python
# Just change environment variable
VECTOR_DB_TYPE=pinecone  # → uses Pinecone
VECTOR_DB_TYPE=faiss     # → uses FAISS
VECTOR_DB_TYPE=weaviate  # → uses Weaviate

# No code changes needed!
```

## Troubleshooting

### Pinecone Issues
- Connection refused: Check API key and network
- Index not found: Create index first
- Rate limited: Upgrade plan or reduce batch size

### FAISS Issues
- Out of memory: Use a smaller embedding model or delete old indexes
- Index corrupted: Delete `.faiss` and `.pkl` files and rebuild
- Index too large: Consider migrating to Pinecone

### Weaviate Issues
- Connection refused: Ensure container is running
- Schema mismatch: Delete collection and reinit
- Slow queries: Add indexes on frequently filtered fields

## Decision Making Guide

**Choose FAISS if:**
- Building MVP/prototype
- Have limited budget
- Small dataset (< 10M vectors)
- Running locally

**Choose Weaviate if:**
- Need open-source option
- Want advanced query features
- Have infrastructure team
- Need on-premises solution

**Choose Pinecone if:**
- Production deployment
- Large scale (> 10M vectors)
- Want full SaaS benefits
- Have budget for cloud

## Next Steps

1. Try with FAISS locally for development
2. When scaling, choose Pinecone or Weaviate
3. Use factory pattern for easy migration
4. Monitor performance and costs
5. Optimize chunk size and embedding model
