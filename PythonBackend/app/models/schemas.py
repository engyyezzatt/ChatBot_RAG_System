from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000, description="User's question")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Chatbot's response")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sources: Optional[list[str]] = Field(default=None, description="Source documents used")
    
class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    vector_store_status: str = "unknown"