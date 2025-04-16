from typing import Optional, List
from datetime import datetime

class Chat:
    def __init__(
        self,
        group_id: str,
        messages: List[dict],  # Each message can be a dictionary with sender, content, timestamp, etc.
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        id: Optional[str] = None,  # Appwrite document ID
    ):
        self.group_id = group_id
        self.messages = messages
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id

    def to_dict(self):
        return {
            "group_id": self.group_id,
            "messages": self.messages,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_appwrite_document(cls, document):
        return cls(
            id=document.id,
            group_id=document.data.get("group_id"),
            messages=document.data.get("messages", []),
            created_at=datetime.fromisoformat(document.data.get("created_at")) if document.data.get("created_at") else None,
            updated_at=datetime.fromisoformat(document.data.get("updated_at")) if document.data.get("updated_at") else None,
        )
