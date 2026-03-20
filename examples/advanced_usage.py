"""Advanced usage examples"""

import asyncio
import logging
from pathlib import Path
from typing import List

from src.config import Settings
from src.ai_assistant import AIAssistant
from src.ai_assistant.document_processor import DocumentProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_1_basic_usage():
    """Example 1: Basic usage - Add documents and query"""
    print("\n" + "="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Add sample documents
    documents = [
        {
            "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+. "
                      "It's based on standard Python type hints and uses Starlette for the web part.",
            "source": "fastapi_intro.txt",
        },
    ]
    
    texts, metadata = DocumentProcessor.process_documents(documents)
    doc_ids = await assistant.add_documents(texts, metadata)
    print(f"Added {len(doc_ids)} documents")
    
    # Query
    result = await assistant.query("What is FastAPI?")
    print(f"\nQuery: What is FastAPI?")
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.2f}")


async def example_2_batch_processing():
    """Example 2: Batch processing multiple documents"""
    print("\n" + "="*60)
    print("Example 2: Batch Processing")
    print("="*60)
    
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Process multiple documents at once
    documents = [
        {"content": f"Document {i}: Content about topic {i}", "source": f"doc_{i}.txt"}
        for i in range(5)
    ]
    
    texts, metadata = DocumentProcessor.process_documents(documents)
    doc_ids = await assistant.add_documents(texts, metadata)
    print(f"Batch processed {len(documents)} documents into {len(doc_ids)} chunks")


async def example_3_custom_chunking():
    """Example 3: Custom document chunking settings"""
    print("\n" + "="*60)
    print("Example 3: Custom Chunking")
    print("="*60)
    
    settings = Settings()
    settings.chunk_size = 200  # Smaller chunks
    settings.chunk_overlap = 20
    
    long_document = """
    This is a very long document that will be split into smaller chunks.
    """ * 20
    
    documents = [{"content": long_document, "source": "long_doc.txt"}]
    texts, metadata = DocumentProcessor.process_documents(
        documents,
        chunk_size=200,
        chunk_overlap=20,
    )
    
    print(f"Original text length: {len(long_document)}")
    print(f"Number of chunks: {len(texts)}")
    print(f"Average chunk size: {sum(len(t) for t in texts) / len(texts):.0f}")


async def example_4_advanced_querying():
    """Example 4: Advanced querying with different parameters"""
    print("\n" + "="*60)
    print("Example 4: Advanced Querying")
    print("="*60)
    
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Query with different parameters
    query = "Your question here"
    
    # Few results with high confidence
    result_precise = await assistant.query(query, top_k=2)
    print(f"Precise search (top_k=2): Confidence={result_precise['confidence']:.2f}")
    
    # Many results for broader context
    result_broad = await assistant.query(query, top_k=10)
    print(f"Broad search (top_k=10): Found {len(result_broad['sources'])} sources")


async def example_5_statistics_and_monitoring():
    """Example 5: Get statistics and monitor the system"""
    print("\n" + "="*60)
    print("Example 5: Statistics & Monitoring")
    print("="*60)
    
    settings = Settings()
    assistant = AIAssistant(settings)
    
    stats = await assistant.get_stats()
    print("\nAssistant Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


async def example_6_document_management():
    """Example 6: Manage documents - add, query, delete"""
    print("\n" + "="*60)
    print("Example 6: Document Management")
    print("="*60)
    
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Add documents
    documents = [{"content": "Sample content", "source": "sample.txt"}]
    texts, metadata = DocumentProcessor.process_documents(documents)
    doc_ids = await assistant.add_documents(texts, metadata)
    print(f"Added document IDs: {doc_ids}")
    
    # Query to confirm they're indexed
    result = await assistant.query("Sample")
    print(f"Query returned {len(result['sources'])} results")
    
    # Delete documents
    success = await assistant.delete_documents(doc_ids)
    print(f"Deletion successful: {success}")


async def example_7_vector_db_switching():
    """Example 7: Switch between different vector databases"""
    print("\n" + "="*60)
    print("Example 7: Vector Database Switching")
    print("="*60)
    
    print("\nThe assistant supports switching databases via configuration:")
    print("1. Set VECTOR_DB_TYPE=pinecone  (cloud, scalable)")
    print("2. Set VECTOR_DB_TYPE=faiss     (local, fast)")
    print("3. Set VECTOR_DB_TYPE=weaviate  (open-source)")
    print("\nNo code changes needed - just update .env and restart!")


async def example_8_error_handling():
    """Example 8: Error handling and edge cases"""
    print("\n" + "="*60)
    print("Example 8: Error Handling")
    print("="*60)
    
    try:
        settings = Settings()
        assistant = AIAssistant(settings)
        
        # Empty query
        result = await assistant.query("")
        print("Empty query result:", result["answer"][:50])
        
    except Exception as e:
        logger.error(f"Error occurred: {e}")


async def example_9_streaming_responses():
    """Example 9: Streaming responses for long answers"""
    print("\n" + "="*60)
    print("Example 9: Streaming Responses")
    print("="*60)
    
    settings = Settings()
    assistant = AIAssistant(settings)
    
    # Query with streaming enabled
    print("Streaming response: ", end="")
    result = await assistant.query("Sample question", stream=True)
    print(f"\n(Full response: {len(result['answer'])} characters)")


async def example_10_production_setup():
    """Example 10: Production setup recommendations"""
    print("\n" + "="*60)
    print("Example 10: Production Setup")
    print("="*60)
    
    print("""
Production Setup Checklist:

1. Environment Configuration
   □ All API keys in .env (not committed)
   □ Proper log levels set
   □ Error handling configured

2. Vector Database
   □ Pinecone account created (or Weaviate deployed)
   □ API credentials configured
   □ Index/collection initialized

3. API Server
   □ CORS configured for your domains
   □ Rate limiting implemented
   □ Authentication added

4. Monitoring
   □ Logging configured
   □ Error tracking (e.g., Sentry)
   □ Performance metrics

5. Security
   □ Environment variables secured
   □ Input validation enabled
   □ TLS/SSL configured
   □ Regular dependency updates

6. Testing
   □ Unit tests passing
   □ Integration tests passing
   □ Load testing done
   □ Edge cases tested

7. Deployment
   □ Docker container built
   □ CI/CD pipeline configured
   □ Database backups setup
   □ Monitoring alerts configured
    """)


async def main():
    """Run all examples"""
    examples = [
        example_1_basic_usage,
        example_2_batch_processing,
        # example_3_custom_chunking,
        # example_4_advanced_querying,
        # example_5_statistics_and_monitoring,
        # example_6_document_management,
        example_7_vector_db_switching,
        # example_8_error_handling,
        # example_9_streaming_responses,
        example_10_production_setup,
    ]
    
    print("\n" + "="*60)
    print("AI Knowledge Assistant - Advanced Examples")
    print("="*60)
    
    for example in examples:
        try:
            await example()
        except Exception as e:
            logger.error(f"Error in {example.__name__}: {e}")
        
        # Small delay between examples
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
