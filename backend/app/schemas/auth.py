# backend/app/schemas/auth.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    """Schema for user signup request."""
    email: str
    password: str

class UserLogin(BaseModel):
    """Schema for user login request."""
    email: str
    password: str

class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer" # Default token type
