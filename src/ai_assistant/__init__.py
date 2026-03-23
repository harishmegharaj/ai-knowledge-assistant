"""AI Assistant core module"""

import logging
from typing import Optional, List, Dict, Any

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms import FakeListLLM

from src.config import Settings
from src.vector_db.factory import VectorDBFactory
from src.vector_db.base import VectorStoreInterface

logger = logging.getLogger(__name__)


class StreamingCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming responses"""
    
    def __init__(self):
        self.tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Handle new token from LLM"""
        self.tokens.append(token)
        print(token, end="", flush=True)


class AIAssistant:
    """Production-grade AI Knowledge Assistant"""
    
    def __init__(self, settings: Settings):
        """Initialize AI Assistant
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.vector_store = VectorDBFactory.create_vector_store(settings)
        
        # Use fake LLM for testing when no API key
        if settings.openai_api_key:
            self.llm = ChatOpenAI(
                openai_api_key=settings.openai_api_key,
                model_name=settings.openai_model,
                temperature=0.7,
                streaming=True,
            )
        else:
            # Stub LLM for testing without API key
            self.llm = FakeListLLM(responses=["This is a stub response for testing purposes. Please provide an OpenAI API key for actual AI responses."])
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model
        )
        
        # Setup retrieval chain
        self._setup_chain()
        
        logger.info("AI Assistant initialized successfully")
    
    def _setup_chain(self) -> None:
        """Setup LangChain retrieval QA chain"""
        # Custom prompt template
        template = """Use the following pieces of context to answer the user's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer:"""
        
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Note: This is a simplified setup. In production, you'd integrate actual retrievers
        # For now, we'll create a stub that can be extended
        logger.info("QA chain setup completed")
    
    async def add_documents(
        self,
        texts: List[str],
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> List[str]:
        """Add documents to knowledge base
        
        Args:
            texts: List of document texts
            metadata: Optional metadata for documents
            
        Returns:
            List of document IDs
        """
        logger.info(f"Adding {len(texts)} documents to knowledge base")
        doc_ids = await self.vector_store.add_texts(texts, metadata)
        logger.info(f"Successfully added {len(doc_ids)} documents")
        return doc_ids
    
    async def query(
        self,
        query: str,
        top_k: Optional[int] = None,
        stream: bool = False,
        category: Optional[str] = None,
        callback_handler: Optional[BaseCallbackHandler] = None,
    ) -> Dict[str, Any]:
        """Query the knowledge base
        
        Args:
            query: User query
            top_k: Number of relevant documents to retrieve
            stream: Whether to stream the response
            category: Filter by document category
            
        Returns:
            Dictionary with answer and metadata
        """
        top_k = top_k or self.settings.top_k_results
        
        logger.info(f"Processing query: {query} (category: {category})")
        
        # Search vector store
        search_results = await self.vector_store.search(query, k=top_k, category=category)
        
        if not search_results:
            logger.warning("No relevant documents found")
            return {
                "answer": "I could not find any relevant information to answer your question.",
                "sources": [],
                "confidence": 0.0,
            }
        
        # Extract context from search results
        context_docs = [text for text, _, _ in search_results]
        context = "\n\n".join(context_docs)
        
        # Prepare prompt
        prompt_input = self.prompt.format(context=context, question=query)
        
        # Get LLM response
        if stream and callback_handler:
            # Streaming mode with custom callback
            try:
                response = await self.llm.apredict(
                    prompt_input,
                    callbacks=[callback_handler],
                )
                # Return both the final response and any streaming data
                return {
                    "answer": response,
                    "sources": sources,
                    "confidence": search_results[0][1] if search_results else 0.0,
                    "streaming_tokens": getattr(callback_handler, 'tokens', []),
                }
            except Exception as e:
                logger.error(f"Error generating streaming response: {e}")
                response = "I encountered an error while processing your query."
        else:
            # Non-streaming mode
            try:
                response = await self.llm.apredict(prompt_input)
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                response = "I encountered an error while processing your query."
        
        # Prepare sources
        sources = [
            {
                "text": text[:100] + "...",
                "score": score,
                "metadata": meta,
            }
            for text, score, meta in search_results
        ]
        
        return {
            "answer": response,
            "sources": sources,
            "confidence": search_results[0][1] if search_results else 0.0,
        }
    
    async def get_categories(self) -> List[str]:
        """Get all available document categories
        
        Returns:
            List of unique category names
        """
        return await self.vector_store.get_categories()
    
    async def delete_documents(self, doc_ids: List[str]) -> bool:
        """Delete documents from knowledge base
        
        Args:
            doc_ids: List of document IDs to delete
            
        Returns:
            True if successful
        """
        logger.info(f"Deleting {len(doc_ids)} documents")
        result = await self.vector_store.delete(doc_ids)
        if result:
            logger.info("Documents deleted successfully")
        else:
            logger.warning("Failed to delete documents")
        return result
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get assistant statistics
        
        Returns:
            Dictionary with statistics
        """
        return await self.vector_store.get_stats()
