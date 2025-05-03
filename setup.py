#!/usr/bin/env python3
import os
import argparse
import subprocess
import sys

# --- Directories to create ---
EXTRA_DIRS = [
    ".github/workflows",
    "ai/models/llama-2",
    "backend/app/api/v1/endpoints",
    "backend/app/core",
    "backend/app/utils",
    "backend/app/services",
    "backend/app/schemas",
    "backend/app/tests",
    "docs/api",
]

# --- Files and their boilerplate content ---
EXTRA_FILES = {
    ".github/workflows/ci.yml": f"""\
name: CI

on:
  push:
    paths:
      - 'backend/**'
      - 'ai/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SSH and Deploy
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{'{'} secrets.VM_HOST {'}'}}
          username: ${{'{'} secrets.VM_USER {'}'}}
          key: ${{'{'} secrets.VM_SSH_KEY {'}'}}
          script: |
            cd ~/groupify
            docker-compose -f backend/docker-compose.yml -f ai/docker-compose.yml up -d --build --force-recreate
""",
    "ai/docker-compose.yml": f"""\
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
volumes:
  ollama-data:
""",
    "backend/Dockerfile": f"""\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "backend/requirements.txt": f"""\
fastapi==0.104.1
uvicorn==0.24.0.post1
supabase-py==2.3.1
requests==2.31.0
pydantic==2.5.2
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
""",
    "backend/docker-compose.yml": f"""\
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${'{'}SUPABASE_URL{'}'}
      - SUPABASE_KEY=${'{'}SUPABASE_KEY{'}'}
      - OLLAMA_ENDPOINT=http://ollama:11434
    depends_on:
      - ollama
""",
    "backend/app/main.py": f"""\
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
from .api.v1.api import api_router

load_dotenv()

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {{"status": "ok"}}

@app.get("/")
def read_root():
    return {{"message": "Welcome to Groupify Backend"}}
""",
    "backend/app/api/v1/api.py": f"""\
from fastapi import APIRouter

api_router = APIRouter()

from .endpoints import auth, users, chat
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
""",
    "backend/app/api/v1/endpoints/auth.py": f"""\
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client, create_client
import os
from ...services.auth_service import AuthService
from ...utils.supabase_client import get_supabase_client
from ...schemas.auth import UserCreate, UserLogin, Token

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, client: Client = Depends(get_supabase_client)):
    auth_service = AuthService(client)
    try:
        response = auth_service.signup(user.email, user.password)
        if response.user:
            return {{"message": "User signed up successfully", "user_id": response.user.id}}
        else:
             raise HTTPException(status_code=400, detail=response.json().get("msg", "Signup failed"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login_user(user: UserLogin, client: Client = Depends(get_supabase_client)):
    auth_service = AuthService(client)
    try:
        response = auth_service.login(user.email, user.password)
        if response.user:
            return Token(access_token=response.session.access_token, token_type="bearer")
        else:
            raise HTTPException(status_code=401, detail=response.json().get("msg", "Login failed"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
""",
    "backend/app/api/v1/endpoints/users.py": f"""\
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from ...services.user_service import UserService
from ...utils.supabase_client import get_supabase_client
from ...schemas.users import UserProfile

router = APIRouter()

@router.get("/{'{'}user_id{'}'}", response_model=UserProfile)
def get_user(user_id: str, client: Client = Depends(get_supabase_client)):
    user_service = UserService(client)
    try:
        response = user_service.get_user_profile(user_id)
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
""",
    "backend/app/api/v1/endpoints/chat.py": f"""\
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
import requests
import os
from ...services.chat_service import ChatService
from ...utils.supabase_client import get_supabase_client
from ...schemas.chat import MessageCreate, Message, AIChatRequest

router = APIRouter()

@router.post("/message", response_model=Message)
def send_message(message: MessageCreate, sender_id: str, client: Client = Depends(get_supabase_client)):
    chat_service = ChatService(client)
    try:
        response = chat_service.send_message(sender_id, message.room_id, message.content)
        if response.data:
             return response.data[0]
        else:
             raise HTTPException(status_code=400, detail="Failed to send message")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/room/{'{'}room_id{'}'}/messages", response_model=list[Message])
def get_messages(room_id: str, client: Client = Depends(get_supabase_client)):
    chat_service = ChatService(client)
    try:
        response = chat_service.get_messages(room_id)
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai")
def send_ai_message(request: AIChatRequest):
    chat_service = ChatService(None) # Supabase client not needed for AI interaction here
    try:
        ollama_response = chat_service.get_ai_response(request.prompt)
        if ollama_response:
            return ollama_response
        else:
            raise HTTPException(status_code=500, detail="Failed to get AI response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
""",
    "backend/app/core/config.py": f"""\
import os

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "YOUR_SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "YOUR_SUPABASE_KEY")
    OLLAMA_ENDPOINT: str = os.getenv("OLLAMA_ENDPOINT", "http://ollama:11434")

settings = Settings()
""",
    "backend/app/utils/supabase_client.py": f"""\
from supabase import create_client, Client
from ..core.config import settings

def get_supabase_client() -> Client:
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_KEY
    return create_client(url, key)
""",
    "backend/app/utils/ollama_client.py": f"""\
import requests
from ..core.config import settings

def generate_text_with_ollama(prompt: str, model: str = "llama2"):
    url = f"{{settings.OLLAMA_ENDPOINT}}/api/generate"
    payload = {{"model": model, "prompt": prompt}}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {{e}}")
        return None
""",
    "backend/app/services/auth_service.py": f"""\
from supabase import Client

class AuthService:
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def signup(self, email, password):
        return self.supabase_client.auth.sign_up(email=email, password=password)

    def login(self, email, password):
        return self.supabase_client.auth.sign_in_with_password(email=email, password=password)
""",
    "backend/app/services/user_service.py": f"""\
from supabase import Client

class UserService:
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def get_user_profile(self, user_id):
        return self.supabase_client.from_("profiles").select("*").eq("id", user_id).execute()
""",
    "backend/app/services/chat_service.py": f"""\
from supabase import Client
from ..utils.ollama_client import generate_text_with_ollama

class ChatService:
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def send_message(self, sender_id, room_id, content):
        return self.supabase_client.from_("messages").insert({{"sender_id": sender_id, "room_id": room_id, "content": content}}).execute()

    def get_messages(self, room_id):
        return self.supabase_client.from_("messages").select("*").eq("room_id", room_id).order("created_at").execute()

    def get_ai_response(self, prompt):
        return generate_text_with_ollama(prompt)
""",
    "backend/app/schemas/auth.py": f"""\
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
""",
     "backend/app/schemas/users.py": f"""\
from pydantic import BaseModel

class UserProfile(BaseModel):
    id: str
    username: str | None = None
    avatar_url: str | None = None
""",
    "backend/app/schemas/chat.py": f"""\
from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    room_id: str
    content: str

class Message(BaseModel):
    id: int
    sender_id: str
    room_id: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class AIChatRequest(BaseModel):
    prompt: str
""",
    "backend/app/tests/test_main.py": f"""\
import pytest
from httpx import AsyncClient
from ..main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {{"status": "ok"}}

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {{"message": "Welcome to Groupify Backend"}}
""",
    "README.md": f"""\
# Groupify

Turnkey, zero-cost chat app blueprint.

See docs/setup.md for setup instructions.
""",
    ".env.example": f"""\
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_KEY
OLLAMA_ENDPOINT=http://ollama:11434
""",
    ".gitignore": f"""\
venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage

# IDE specific
.idea/
.vscode/
*.iml
*.ipr
*.iws

# Environment variables file
.env

# OS specific
.DS_Store
Thumbs.db

# AI models (can be large)
ai/models/

# Ollama data volume
ollama-data/

# Flutter build artifacts
.flutter-plugins
.flutter-plugins-dependencies
.packages
.dart_tool/
build/
.pub-cache/
""",
    "docs/setup.md": f"""\
# Setup Instructions

See README.md for project overview.

This document outlines basic setup steps.

1. Run `python setup.py`.
2. Configure `.env` with Supabase and Ollama details.
3. Set up Supabase DB (profiles, messages, chat_rooms tables).
4. Set up Oracle Cloud VMs and networking.
5. Configure GitHub Actions secrets for deployment.
6. Develop backend and frontend.
7. Push code to trigger CI/CD.
""",
    "docs/architecture.md": f"""\
# Architecture Overview

- Frontend: Flutter (Web, Mobile, Desktop)
- Backend: FastAPI (Python) on Oracle Cloud VM
- AI: Ollama on Oracle Cloud VM
- Database/Auth/Storage: Supabase
- CI/CD: GitHub Actions
- Hosting: Cloudflare Pages (Frontend Web)

Data Flow: Frontend -> Backend -> Supabase/Ollama
""",
    "docs/api/openapi.json": f"""\
{{}}
""",
    "frontend/lib/main.dart": f"""\
import 'package:flutter/material.dart';
import 'package:groupify/groupify_app.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();

  // Hardcoded placeholders - replace with actual Supabase credentials
  await Supabase.initialize(
    url: 'YOUR_SUPABASE_URL',
    anonKey: 'YOUR_SUPABASE_KEY',
  );

  runApp(const GroupifyApp());
}}
""",
    "frontend/lib/groupify_app.dart": f"""\
import 'package:flutter/material.dart';

class GroupifyApp extends StatelessWidget {{
  const GroupifyApp({{Key? key}}) : super(key: key);

  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: 'Groupify',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const HomePage(), // Define your initial screen here
    );
  }}
}}

class HomePage extends StatelessWidget {{
  const HomePage({{Key? key}}) : super(key: key);

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('Groupify'),
      ),
      body: const Center(
        child: Text('Welcome to Groupify!'),
      ),
    );
  }}
}}
""",
    "frontend/test/widget_test.dart": f"""\
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:groupify/groupify_app.dart'; // Import your app file

void main() {{
  testWidgets('App starts with basic text', (WidgetTester tester) async {{
    await tester.pumpWidget(const GroupifyApp());

    expect(find.text('Welcome to Groupify!'), findsOneWidget);
    expect(find.byType(AppBar), findsOneWidget);
  }});
}}
""",
    "frontend/pubspec.yaml": f"""\
name: groupify
description: A new Flutter project.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  supabase_flutter: ^1.0.0 # Add Supabase Flutter package

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
""",
    "frontend/analysis_options.yaml": f"""\
include: package:flutter_lints/flutter.yaml
analyzer:
  exclude:
    - '**/*.g.dart'
    - '**/*.freezed.dart'
linter:
  rules:
    # Enable recommended lints
    - avoid_print
    - prefer_single_quotes
""",
}

def run(cmd, cwd=None):
    """Run a subprocess command, raising on failure."""
    print(f"> {' '.join(cmd)}")
    try:
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {{e}}")
        print(f"Stdout: {{e.stdout}}")
        print(f"Stderr: {{e.stderr}}")
        sys.exit(1)

def ensure_flutter_project():
    """Ensure a Flutter project exists in frontend/."""
    if not os.path.isdir("frontend"):
        print("Frontend directory not found. Creating a new Flutter project...")
        run(["flutter", "create", "frontend"])
    else:
        print("Frontend directory found.")

def ensure_flutter_web_support():
    """Run `flutter create .` inside frontend/ to add missing web files if needed."""
    print("Ensuring Flutter web support...")
    run(["flutter", "create", "."], cwd="frontend")

def make_extra_dirs():
    """Create all additional directories."""
    print("Creating extra directories...")
    for d in EXTRA_DIRS:
        os.makedirs(d, exist_ok=True)

def write_extra_files():
    """Write boilerplate files defined in EXTRA_FILES."""
    print("Writing extra boilerplate files...")
    for path, content in EXTRA_FILES.items():
        dirpath = os.path.dirname(path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        try:
            with open(path, "w") as f:
                f.write(content)
            print(f"  - Written {path}")
        except IOError as e:
            print(f"Error writing file {path}: {{e}}")
            sys.exit(1)

def flutter_pub_get():
    """Run flutter pub get in the frontend directory."""
    print("Running flutter pub get...")
    run(["flutter", "pub", "get"], cwd="frontend")

def build_frontend():
    """Run flutter build web to produce build/web."""
    print("Building frontend web application...")
    run(["flutter", "build", "web"], cwd="frontend")

def main():
    parser = argparse.ArgumentParser(
        description="Scaffold Groupify project structure and write boilerplate files."
    )
    parser.add_argument(
        "--skip-frontend-build", action="store_true",
        help="Skip the Flutter web build process."
    )
    args = parser.parse_args()

    ensure_flutter_project()
    ensure_flutter_web_support()
    make_extra_dirs()
    write_extra_files()

    flutter_pub_get() # Run pub get after writing pubspec.yaml

    print("\nScaffolding complete.")

    if not args.skip_frontend_build:
        build_frontend()
        print("Frontend build process finished.")

    print("\nSetup script finished.")
    print("Remember to fill in your actual credentials in the generated `.env` file.")

if __name__ == "__main__":
    main()

