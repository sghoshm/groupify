import os
import subprocess

def create_empty_file(filepath):
    """Creates an empty file if it doesn't exist."""
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            pass

def create_directory(path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory '{path}' already exists.")

def write_file(filepath, content):
    """Writes content to a file, creating the directory if it doesn't exist."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created and populated file: {filepath}")

def create_project_structure():
    """Populates backend files in the existing 'groupify' structure."""

    backend_dir = "backend"
    docker_dir = "docker"
    ollama_docker_dir = os.path.join(docker_dir, "ollama")

    backend_app_dir = os.path.join(backend_dir, "app")
    backend_app_api_v1_dir = os.path.join(backend_app_dir, "api", "v1")
    backend_app_api_v1_endpoints_dir = os.path.join(backend_app_api_v1_dir, "endpoints")
    backend_app_core_dir = os.path.join(backend_app_dir, "core")
    backend_app_crud_dir = os.path.join(backend_app_dir, "crud")
    backend_app_models_dir = os.path.join(backend_app_dir, "models")
    backend_app_schemas_dir = os.path.join(backend_app_dir, "schemas")
    backend_app_utils_dir = os.path.join(backend_app_dir, "utils")
    backend_alembic_dir = os.path.join(backend_dir, "alembic")

    # Create backend directories (if they don't exist)
    create_directory(backend_dir)
    create_directory(backend_app_dir)
    create_directory(backend_app_api_v1_dir)
    create_directory(backend_app_api_v1_endpoints_dir)
    create_directory(backend_app_core_dir)
    create_directory(backend_app_crud_dir)
    create_directory(backend_app_models_dir)
    create_directory(backend_app_schemas_dir)
    create_directory(backend_app_utils_dir)
    create_directory(backend_alembic_dir)

    # Populate backend files
    write_file(os.path.join(backend_app_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_dir, "main.py"), """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router

app = FastAPI(title="Groupify Backend")

origins = ["*"]  # Adjust as needed for security

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Groupify Backend API v1"}
""")
    write_file(os.path.join(backend_app_api_v1_dir, "__init__.py"), "from .api import api_router")
    write_file(os.path.join(backend_app_api_v1_dir, "api.py"), """from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
""")
    write_file(os.path.join(backend_app_api_v1_endpoints_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_api_v1_endpoints_dir, "auth.py"), """from fastapi import APIRouter, HTTPException
from appwrite.exception import AppwriteException
from app.utils.appwrite_client import account, database
from app.core.config import settings
from app.schemas.user_profile import UserProfileCreate, UserProfileResponse
from app.models.user_profile import UserProfile

router = APIRouter()
APPWRITE_DATABASE_ID = "67fcce30000cb2d2fec9"  # Your Appwrite database ID
USER_PROFILE_COLLECTION_ID = "67fcd214000dd0f539f6"  # Your user profile collection ID

@router.post("/register", response_model=UserProfileResponse)
async def register_user(user: UserProfileCreate):
    try:
        user_result = await account.create(
            user.email,
            "password",  # Consider a more secure way to handle passwords in a real application
            user.username,
        )
        profile_data = user.model_dump()
        profile_data["user_id"] = user_result.id
        profile = UserProfile(**profile_data)
        profile_document = await database.create_document(
            settings.APPWRITE_PROJECT_ID,
            APPWRITE_DATABASE_ID,
            USER_PROFILE_COLLECTION_ID,
            profile.to_dict(),
        )
        return UserProfileResponse.from_attributes(profile.copy(update={"id": profile_document.id}))
    except AppwriteException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.post("/login", response_model=UserProfileResponse)
async def login_user(user: UserProfileCreate):  # Using UserProfileCreate for simplicity, you might want a dedicated Login schema
    try:
        session = await account.create_email_session(user.email, "password")
        user_data = await account.get()
        profile_document = await database.list_documents(
            settings.APPWRITE_PROJECT_ID,
            APPWRITE_DATABASE_ID,
            USER_PROFILE_COLLECTION_ID,
            queries=[f'equal("user_id", "{user_data.id}")'],
        )
        if profile_document.total == 0:
            raise HTTPException(status_code=404, detail="User profile not found")
        profile = UserProfile.from_appwrite_document(profile_document.documents[0])
        return UserProfileResponse.from_attributes(profile)
    except AppwriteException as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")
""")
    write_file(os.path.join(backend_app_api_v1_endpoints_dir, "chat.py"), """from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.chat import ChatCreate, ChatResponse, ChatUpdate
from app.crud import chat as crud_chat

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def create_chat(chat_in: ChatCreate):
    chat = await crud_chat.create(chat_in)
    return chat

@router.get("/{group_id}", response_model=ChatResponse)
async def get_chat_by_group_id(group_id: str):
    chat = await crud_chat.get_by_group_id(group_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.put("/{group_id}", response_model=ChatResponse)
async def update_chat(group_id: str, chat_in: ChatUpdate):
    chat = await crud_chat.update(group_id, chat_in)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
""")
    write_file(os.path.join(backend_app_api_v1_endpoints_dir, "users.py"), """from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_profile import UserProfileResponse, UserProfileUpdate
from app.crud import user_profile as crud_user_profile

router = APIRouter()

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile():
    # In a real application, you would get the current user's ID from the authentication context
    # For now, we'll assume a placeholder user ID
    user_id = "some-user-id"  # Replace with actual logic to get current user ID
    profile = await crud_user_profile.get_by_user_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.put("/me", response_model=UserProfileResponse)
async def update_current_user_profile(profile_in: UserProfileUpdate):
    # In a real application, you would get the current user's ID from the authentication context
    # For now, we'll assume a placeholder user ID
    user_id = "some-user-id"  # Replace with actual logic to get current user ID
    profile = await crud_user_profile.update(user_id, profile_in)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    profile = await crud_user_profile.get_by_user_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile
""")
    write_file(os.path.join(backend_app_core_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_core_dir, "config.py"), """import os

class Settings:
    APPWRITE_ENDPOINT: str = os.getenv("APPWRITE_ENDPOINT")
    APPWRITE_PROJECT_ID: str = os.getenv("APPWRITE_PROJECT_ID")
    APPWRITE_API_KEY: str = os.getenv("APPWRITE_API_KEY")
    APPWRITE_DATABASE_ID: str = os.getenv("APPWRITE_DATABASE_ID", "67fcce30000cb2d2fec9")
    USERS_COLLECTION_ID: str = os.getenv("USERS_COLLECTION_ID")
    CHATS_COLLECTION_ID: str = os.getenv("CHATS_COLLECTION_ID")

settings = Settings()
""")
    write_file(os.path.join(backend_app_crud_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_crud_dir, "chat.py"), """from appwrite.databases import Databases
from app.core.config import settings
from app.schemas.chat import ChatCreate, ChatUpdate, ChatResponse
from app.models.chat import Chat
from app.utils.appwrite_client import client

APPWRITE_DATABASE_ID = "67fcce30000cb2d2fec9"
CHAT_COLLECTION_ID = settings.CHATS_COLLECTION_ID

async def create(chat: ChatCreate) -> ChatResponse:
    chat_dict = chat.model_dump()
    result = await client.databases.create_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        CHAT_COLLECTION_ID,
        chat_dict,
    )
    return ChatResponse(**result.data, id=result.id)

async def get_by_group_id(group_id: str) -> ChatResponse | None:
    documents = await client.databases.list_documents(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        CHAT_COLLECTION_ID,
        queries=[f'equal("group_id", "{group_id}")'],
    )
    if documents.total > 0:
        return ChatResponse(**documents.documents[0].data, id=documents.documents[0].id)
    return None

async def update(group_id: str, chat: ChatUpdate) -> ChatResponse | None:
    existing_chat = await get_by_group_id(group_id)
    if not existing_chat:
        return None

    update_data = chat.model_dump(exclude_unset=True)
    result = await client.databases.update_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        CHAT_COLLECTION_ID,
        existing_chat.id,
        update_data,
    )
    return ChatResponse(**result.data, id=result.id)
""")
    write_file(os.path.join(backend_app_crud_dir, "user_profile.py"), """from appwrite.databases import Databases
from app.core.config import settings
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from app.models.user_profile import UserProfile
from app.utils.appwrite_client import client

APPWRITE_DATABASE_ID = "67fcce30000cb2d2fec9"
USER_PROFILE_COLLECTION_ID = settings.USERS_COLLECTION_ID

async def create(user_profile: UserProfileCreate) -> UserProfileResponse:
    profile_dict = user_profile.model_dump()
    result = await client.databases.create_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        USER_PROFILE_COLLECTION_ID,
        profile_dict,
    )
    return UserProfileResponse(**result.data, id=result.id)

async def get_by_user_id(user_id: str) -> UserProfileResponse | None:
    documents = await client.databases.list_documents(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        USER_PROFILE_COLLECTION_ID,
        queries=[f'equal("user_id", "{user_id}")'],
    )
    if documents.total > 0:
        return UserProfileResponse(**documents.documents[0].data, id=documents.documents[0].id)
    return None

async def update(user_id: str, user_profile_in: UserProfileUpdate) -> UserProfileResponse | None:
    existing_profile = await get_by_user_id(user_id)
    if not existing_profile:
        return None

    update_data = user_profile_in.model_dump(exclude_unset=True)
    result = await client.databases.update_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        USER_PROFILE_COLLECTION_ID,
        existing_profile.id,
        update_data,
    )
    return UserProfileResponse(**result.data, id=result.id)
""")
    write_file(os.path.join(backend_app_models_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_models_dir, "chat.py"), """from typing import Optional, List
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
""")
    write_file(os.path.join(backend_app_models_dir, "user_profile.py"), """from typing import Optional

class UserProfile:
    def __init__(
        self,
        user_id: str,  # Appwrite user ID
        username: str,
        email: str,
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
""")
    write_file(os.path.join(backend_app_schemas_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_schemas_dir, "chat.py"), """from pydantic import BaseModel
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
""")
    write_file(os.path.join(backend_app_schemas_dir, "user_profile.py"), """from pydantic import BaseModel, EmailStr
from typing import Optional

class UserProfileBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    user_id: str  # Appwrite user ID

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
""")
    write_file(os.path.join(backend_app_utils_dir, "__init__.py"), "")
    write_file(os.path.join(backend_app_utils_dir, "appwrite_client.py"), """import os
from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.services.functions import Functions
from app.core.config import settings

client = Client()

client.set_endpoint(settings.APPWRITE_ENDPOINT)
client.set_project(settings.APPWRITE_PROJECT_ID)
client.set_key(settings.APPWRITE_API_KEY)

account = Account(client)
database = Databases(client)
storage = Storage(client)
functions = Functions(client)
""")
    write_file(os.path.join(backend_dir, "alembic.ini"), """# Alembic Config File.
# ... (rest of the default content)
""")
    write_file(os.path.join(backend_dir, "requirements.txt"), """appwrite
fastapi
uvicorn
python-multipart
requests
pydantic[email]
alembic
""")
    write_file(os.path.join(backend_dir, "Dockerfile"), """FROM python:3.11-slim-buster

WORKDIR /app
ENV PYTHONPATH=/app/app:/app

COPY ../app /app/app
COPY ./alembic.ini /app/alembic.ini
COPY ./alembic /app/alembic

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

    # Create Docker directories and files
    create_directory(docker_dir)
    create_directory(ollama_docker_dir)
    write_file(os.path.join(docker_dir, "docker-compose.yml"), """services:
  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
      - APPWRITE_PROJECT_ID=67fccdb50010befde82f
      - APPWRITE_API_KEY=standard_b87bd1877c3cf4bec2f1c474bead58fc8555345fc306b4ebfa510c820d99577ed9c6154bc00dccc5875e8f3dfeebeebe00c4566a7eead0b59ce443aa85c96f17465364045868006c4319f8ab61416cb8fd8cc702c8ab10cd01529e25bc858ca6dc0019dce5ec0f6a5efb68d8d7b5c793b2f86983f5244422335ba1afe6a32b75
      - USERS_COLLECTION_ID=${USERS_COLLECTION_ID}
      - CHATS_COLLECTION_ID=${CHATS_COLLECTION_ID}
    env_file:
      - backend/.env
    depends_on:
      - ollama
    volumes:
      - backend_data:/app

  frontend:
    build: ../frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    # You might need to adjust volumes depending on how you build your Flutter web app
    # volumes:
    #   - ../frontend/build/web:/usr/share/nginx/html:ro

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
  backend_data:
""")
    write_file(os.path.join(ollama_docker_dir, "Dockerfile"), """# This Dockerfile is optional as we are using the official ollama image in docker-compose.yml
# You might use this if you need to customize the Ollama image further.
# For now, the docker-compose.yml configuration is sufficient.
""")

    # Create root level files
    create_empty_file(os.path.join(".", ".gitignore"))
    create_empty_file(os.path.join(".", "README.md"))

if __name__ == "__main__":
    create_project_structure()
    print("\nProject setup complete with all directories and initial files!")