import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"  # You can change this to "llama3" if you have it installed
    
    # Document Processing
    docs_directory: str = "docs"
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # Vector Store
    vector_store_path: str = "./vector_store"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # API Configuration
    host: str = "localhost"
    port: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()