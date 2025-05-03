# backend/app/schemas/users.py
from pydantic import BaseModel

class UserProfile(BaseModel):
    """Schema for user profile data."""
    id: str # Supabase user ID (UUID)
    username: str | None = None # Optional username
    avatar_url: str | None = None # Optional avatar URL

    class Config:
        # Allows converting SQLAlchemy/Supabase models to Pydantic models
        from_attributes = True

# Example schema for updating a profile (use Pydantic's exclude_unset=True)
# class UserProfileUpdate(BaseModel):
#     username: str | None = None
#     avatar_url: str | None = None
