from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfileBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    password: str  # 🔒 Required for registration
    user_id: Optional[str] = None  # Let backend set it

class UserLoginSchema(BaseModel):  # ✅ This was missing!
    email: EmailStr
    password: str

class UserProfileUpdate(UserProfileBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserProfileResponse(UserProfileBase):
    id: str
    user_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
