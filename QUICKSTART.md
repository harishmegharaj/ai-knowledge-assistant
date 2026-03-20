# Quick Start Guide

## For First-Time Users

### Step 1: Clone and Setup (2 minutes)
```bash
cd /Users/harishashokmegharaj/reactnext/AIML
python install.py
```

### Step 2: Configure Environment (1 minute)
```bash
cp .env.example .env
# Edit .env with your API keys (OPENAI_API_KEY, VECTOR_DB settings)
```

### Step 3: Choose Database (1 minute)

**Option A: FAISS (Local - Recommended for Beginners)**
```bash
# Just use it - FAISS is the default in .env
# No additional setup needed
```

**Option B: Pinecone (Cloud)**
```bash
# 1. Create account at https://www.pinecone.io
# 2. Get your API key and environment
# 3. Update .env:
VECTOR_DB_TYPE=pinecone
PINECONE_API_KEY=your_key
```

**Option C: Weaviate (Local Docker)**
```bash
# 1. Install Docker
# 2. Run: docker run -p 8080:8080 semitechnologies/weaviate:latest
# 3. Update .env:
VECTOR_DB_TYPE=weaviate
WEAVIATE_URL=http://localhost:8080
```

### Step 4: Run Your First Query (2 minutes)

#### Using Python:
```python
import asyncio
from src.config import Settings
from src.ai_assistant import AIAssistant
from src.ai_assistant.document_processor import DocumentProcessor

async def main():
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Add a document
    docs = [{"content": "Python is awesome!", "source": "test.txt"}]
    texts, metadata = DocumentProcessor.process_documents(docs)
    await assistant.add_documents(texts, metadata)
    
    # Query it
    result = await assistant.query("What is Python?")
    print(result["answer"])

asyncio.run(main())
```

#### Using REST API:
```bash
# Start server
python -m uvicorn src.api.main:app --reload

# In another terminal, add a document
curl -X POST http://localhost:8000/documents/add \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {"content": "Python is awesome!", "source": "test.txt"}
    ]
  }'

# Query it
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Python?"}'
```

#### Using CLI:
```bash
python -m src.api.cli add_document --text "Python is awesome!" --source "test.txt"
python -m src.api.cli query --query "What is Python?"
```

## Common Issues & Quick Fixes

### "OpenAI API key not found"
→ Add `OPENAI_API_KEY=sk-...` to your `.env` file

### "No relevant documents found"
→ Make sure you added documents first with `add_documents()`

### "Connection refused"
→ Make sure Weaviate is running with `docker ps` (if using Weaviate)

### "Out of disk space"
→ Delete FAISS index: `rm -rf data/faiss_index*`

## Next Steps

1. **Read the README** for detailed documentation
2. **Check examples/** for more usage patterns
3. **Try different databases** by switching `VECTOR_DB_TYPE`
4. **Deploy to production** using docs/DEPLOYMENT.md
5. **Add authentication** for production use

## Need Help?

- 📖 Read: [README.md](README.md)
- 🗄️ Databases: [docs/VECTOR_DB_GUIDE.md](docs/VECTOR_DB_GUIDE.md)
- 🚀 Deploy: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- 🧪 Test API: [docs/API_TESTING.md](docs/API_TESTING.md)
- 🤝 Contribute: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

Enjoy! 🚀
