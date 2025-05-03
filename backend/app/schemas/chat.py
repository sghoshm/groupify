# backend/app/schemas/chat.py
from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    """Schema for creating a new chat message."""
    room_id: str
    content: str

class Message(BaseModel):
    """Schema for a chat message object."""
    id: int # Database primary key
    sender_id: str # ID of the user who sent the message
    room_id: str # ID of the chat room
    content: str # Message content
    created_at: datetime # Timestamp of message creation

    class Config:
        # Allows converting SQLAlchemy/Supabase models to Pydantic models
        from_attributes = True

class AIChatRequest(BaseModel):
    """Schema for a request to the AI endpoint."""
    prompt: str
