import logging
import re
from typing import List, Optional, Tuple
import warnings

from langchain_community.llms import Ollama as OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from app.config.settings import settings
from app.services.document_processor import DocumentProcessor

warnings.filterwarnings("ignore")

class RAGService:
    """
    Retrieval-Augmented Generation service.
    Follows SRP - Handles RAG pipeline logic.
    Follows DIP - Depends on abstractions (interfaces).
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.document_processor = DocumentProcessor()
        self.llm = self._initialize_llm()
        self.retrieval_chain = None
        self._initialize_rag_chain()
    
    def _initialize_llm(self):
        """Initialize the Ollama language model."""
        try:
            self.logger.info(f"Initializing Ollama LLM with model: {settings.ollama_model}")
            return OllamaLLM(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model,
                temperature=0.5
            )
        except Exception as e:
            self.logger.error(f"Error initializing Ollama LLM: {str(e)}")
            raise
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the LLM response for better readability."""
        if not response:
            return response
        
        # Remove excessive newlines and whitespace
        cleaned = response.strip()
        
        # Replace multiple newlines with single newlines
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
        
        # Replace single newlines with spaces (except for intentional paragraph breaks)
        cleaned = re.sub(r'(?<!\n)\n(?!\n)', ' ', cleaned)
        
        # Clean up multiple spaces
        cleaned = re.sub(r' +', ' ', cleaned)
        
        # Remove quotes around the entire response if present
        cleaned = re.sub(r'^["\']+|["\']+$', '', cleaned)
        
        # Remove section references in parentheses at the end
        cleaned = re.sub(r'\s*\([^)]*Section[^)]*\)\s*$', '', cleaned)
        
        # Clean up any remaining formatting artifacts
        cleaned = cleaned.replace('\\n', ' ').replace('\\"', '"')
        
        return cleaned.strip()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """Create a custom prompt template for the RAG chain."""
        template = """You are a helpful AI assistant that answers questions based on the provided context. 
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
        Provide a clear, concise answer without excessive formatting or newlines.

        Context:
        {context}

        Question: {question}

        Answer: """
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _initialize_rag_chain(self):
        """Initialize the RAG chain with retriever and LLM."""
        try:
            if not self.llm:
                raise ValueError("LLM not initialized")
                
            vector_store = self.document_processor.get_vector_store()
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}  # Retrieve top 3 relevant chunks
            )
            
            prompt_template = self._create_prompt_template()
            
            self.retrieval_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": prompt_template},
                return_source_documents=True
            )
            
            self.logger.info("RAG chain initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing RAG chain: {str(e)}")
            raise
    
    def get_answer(self, question: str) -> Tuple[str, List[str]]:
        """
        Get answer for a question using RAG pipeline.
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (answer, source_documents)
        """
        try:
            if not self.retrieval_chain:
                raise ValueError("RAG chain not initialized")
            
            self.logger.info(f"Processing question: {question}")
            
            # Get response from RAG chain
            result = self.retrieval_chain({"query": question})
            
            raw_answer = result.get("result", "I couldn't generate a response.")
            source_docs = result.get("source_documents", [])
            
            # Clean the response
            answer = self._clean_response(raw_answer)
            
            # Extract source information with better logging
            sources = []
            source_details = {}
            
            for doc in source_docs:
                source_info = doc.metadata.get("source", "Unknown")
                if source_info not in sources:
                    sources.append(source_info)
                
                # Count occurrences of each source
                if source_info not in source_details:
                    source_details[source_info] = 0
                source_details[source_info] += 1
            
            # Log detailed information about sources used
            self.logger.info(f"Generated answer with {len(sources)} unique sources")
            for source, count in source_details.items():
                self.logger.info(f"  - {source}: {count} chunks used")
            
            return answer, sources
            
        except Exception as e:
            self.logger.error(f"Error generating answer: {str(e)}")
            return "I'm sorry, I encountered an error while processing your question.", []
    
    def health_check(self) -> dict:
        """Check the health of the RAG service."""
        try:
            vector_store = self.document_processor.get_vector_store()
            vector_store_status = "healthy" if vector_store else "unavailable"
            
            return {
                "llm_type": "ollama",
                "ollama_model": settings.ollama_model,
                "vector_store_status": vector_store_status,
                "rag_chain_status": "initialized" if self.retrieval_chain else "not_initialized"
            }
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return {
                "llm_type": "ollama",
                "ollama_model": settings.ollama_model,
                "vector_store_status": "error",
                "rag_chain_status": "error",
                "error": str(e)
            }