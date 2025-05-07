from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    """Schema for JWT token response (both access + refresh)."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    """Schema for refresh-token request body."""
    refresh_token: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ConfirmResetRequest(BaseModel):
    new_password: str

class GoogleAuthRequest(BaseModel):
    access_token: str

class PhoneNumberRequest(BaseModel):
    phone_number: str

class VerifyOTPRequest(BaseModel):
    phone_number: str
    token: str

class GitHubAuthURLResponse(BaseModel):
    auth_url: str

