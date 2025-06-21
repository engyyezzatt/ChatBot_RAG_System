import os
import logging
import warnings
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.config.settings import settings

warnings.filterwarnings("ignore")

class DocumentProcessor:
    """
    Handles document loading, processing, and vector store creation.
    Follows SRP - Single responsibility for document processing.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.vector_store = None
        
    def load_documents(self, docs_path: str) -> List[Document]:
        """Load all text documents from the specified directory."""
        documents = []
        
        if not os.path.exists(docs_path):
            self.logger.error(f"Documents directory not found: {docs_path}")
            return documents
            
        try:
            for filename in os.listdir(docs_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(docs_path, filename)
                    self.logger.info(f"Loading document: {filename}")
                    
                    loader = TextLoader(file_path, encoding='utf-8')
                    file_documents = loader.load()
                    
                    # Add metadata to documents
                    for doc in file_documents:
                        doc.metadata['source'] = filename
                        doc.metadata['file_path'] = file_path
                    
                    documents.extend(file_documents)
                    
        except Exception as e:
            self.logger.error(f"Error loading documents: {str(e)}")
            
        self.logger.info(f"Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks for better retrieval."""
        try:
            chunks = self.text_splitter.split_documents(documents)
            self.logger.info(f"Split documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            self.logger.error(f"Error splitting documents: {str(e)}")
            return []
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create and persist vector store from documents."""
        try:
            # Split documents into chunks
            chunks = self.split_documents(documents)
            
            if not chunks:
                raise ValueError("No document chunks available for vector store creation")
            
            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=settings.vector_store_path
            )
            
            # Chroma auto-persists, no need to call persist() manually
            self.logger.info("Vector store created and persisted successfully")
            
            return self.vector_store
            
        except Exception as e:
            self.logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def load_vector_store(self) -> Chroma:
        """Load existing vector store or create new one."""
        try:
            if os.path.exists(settings.vector_store_path):
                self.logger.info("Loading existing vector store")
                self.vector_store = Chroma(
                    persist_directory=settings.vector_store_path,
                    embedding_function=self.embeddings
                )
            else:
                self.logger.info("Creating new vector store")
                documents = self.load_documents(settings.docs_directory)
                if not documents:
                    raise ValueError("No documents found to create vector store")
                self.vector_store = self.create_vector_store(documents)
                
            return self.vector_store
            
        except Exception as e:
            self.logger.error(f"Error loading/creating vector store: {str(e)}")
            raise
    
    def get_vector_store(self) -> Chroma:
        """Get the vector store instance."""
        if self.vector_store is None:
            self.vector_store = self.load_vector_store()
        return self.vector_store