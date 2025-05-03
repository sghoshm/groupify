# backend/app/api/v1/api.py
from fastapi import APIRouter

api_router = APIRouter()

# Import and include routers for different functionalities
# These imports are relative to the 'api.v1' package and are correct
from .endpoints import auth, users, chat
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Note: The imports *within* auth.py, users.py, and chat.py use absolute paths
# from backend.app.
