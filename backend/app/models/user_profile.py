from typing import Optional

class UserProfile:
    def __init__(
        self,
        username: str,
        email: str,
        user_id: Optional[str] = None,  # Appwrite user ID - Made Optional
        full_name: Optional[str] = None,
        bio: Optional[str] = None,
        profile_picture_url: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        id: Optional[str] = None,  # Appwrite document ID
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.bio = bio
        self.profile_picture_url = profile_picture_url
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_picture_url": self.profile_picture_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_appwrite_document(cls, document):
        return cls(
            id=document.id,
            user_id=document.data.get("user_id"),
            username=document.data.get("username"),
            email=document.data.get("email"),
            full_name=document.data.get("full_name"),
            bio=document.data.get("bio"),
            profile_picture_url=document.data.get("profile_picture_url"),
            created_at=document.data.get("created_at"),
            updated_at=document.data.get("updated_at"),
        )