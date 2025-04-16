from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    sender_id: str
    content: str
    timestamp: datetime

class ChatBase(BaseModel):
    group_id: str

class ChatCreate(ChatBase):
    messages: List[Message] = []

class ChatUpdate(ChatBase):
    messages: Optional[List[Message]] = None

class ChatResponse(ChatBase):
    id: str
    messages: List[Message]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
