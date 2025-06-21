import logging
import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.rag_service import RAGService
from app.config.settings import settings

import warnings

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Global RAG service instance (Singleton pattern)
rag_service: Optional[RAGService] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global rag_service
    logger.info("Starting up Python RAG Backend...")
    
    try:
        rag_service = RAGService()
        logger.info("RAG service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {str(e)}")
        rag_service = None
        # Don't raise exception to allow API to start for health checks
    
    yield
    
    # Shutdown
    logger.info("Shutting down Python RAG Backend...")

# Create FastAPI app with lifespan events
app = FastAPI(
    title="RAG Chatbot Backend",
    description="Python backend for RAG-based chatbot using LangChain",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_rag_service() -> RAGService:
    """Dependency to get RAG service instance."""
    if rag_service is None:
        raise HTTPException(
            status_code=503, 
            detail="RAG service is not available. The service failed to initialize. Please check server logs for details."
        )
    return rag_service

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    service: RAGService = Depends(get_rag_service)
):
    """
    Main chat endpoint that processes user questions and returns AI responses.
    """
    try:
        logger.info(f"Received chat request: {request.question}")
        
        # Get answer from RAG service
        answer, sources = service.get_answer(request.question)
        
        response = ChatResponse(
            response=answer,
            sources=sources if sources else None
        )
        
        logger.info(f"Successfully processed chat request")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your question: {str(e)}"
        )

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """Health check endpoint."""
    try:
        health_info = HealthResponse()
        
        if rag_service:
            service_health = rag_service.health_check()
            health_info.vector_store_status = service_health.get("vector_store_status", "unknown")
        else:
            health_info.vector_store_status = "unavailable"
            health_info.status = "degraded"
        
        logger.info("Health check completed")
        return health_info
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "message": "RAG Chatbot Backend API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )