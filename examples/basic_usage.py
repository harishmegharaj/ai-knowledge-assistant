"""Example usage of AI Knowledge Assistant"""

import asyncio
from src.config import Settings
from src.ai_assistant import AIAssistant
from src.ai_assistant.document_processor import DocumentProcessor


async def main():
    """Example usage"""
    
    # Initialize settings
    settings = Settings()
    
    # Create assistant
    print("Initializing AI Assistant...")
    assistant = AIAssistant(settings)
    
    # Example documents
    documents = [
        {
            "content": """
Python is a high-level, interpreted programming language known for its simplicity 
and readability. It supports multiple programming paradigms including object-oriented, 
functional, and procedural programming. Python is widely used in web development, 
data science, artificial intelligence, and automation.
            """,
            "source": "python_intro.txt",
        },
        {
            "content": """
Machine Learning is a subset of Artificial Intelligence that focuses on developing 
algorithms and statistical models that enable computers to learn from data without 
being explicitly programmed. Common ML techniques include supervised learning, 
unsupervised learning, and reinforcement learning.
            """,
            "source": "ml_basics.txt",
        },
    ]
    
    # Process documents
    print("\nProcessing documents...")
    texts, metadata = DocumentProcessor.process_documents(documents)
    
    # Add to knowledge base
    print(f"Adding {len(texts)} text chunks to knowledge base...")
    doc_ids = await assistant.add_documents(texts, metadata)
    print(f"✓ Added {len(doc_ids)} documents")
    
    # Query examples
    queries = [
        "What is Python?",
        "Explain machine learning",
        "How is Python used in AI?",
    ]
    
    print("\n" + "="*50)
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        result = await assistant.query(query, top_k=3)
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']:.2f}")
        
        if result['sources']:
            print(f"Top source: {result['sources'][0]['text'][:100]}...")
    
    # Get statistics
    print("\n" + "="*50)
    stats = await assistant.get_stats()
    print(f"\nAssistant Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
