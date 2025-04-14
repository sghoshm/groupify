from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router

app = FastAPI(title="Groupify Backend")

# Configure CORS
origins = [
    "http://localhost:3000",  # Default Flutter web port
    "http://localhost",
    "https://your-cloudflare-tunnel-url.com",  # Replace with your Cloudflare Tunnel URL for frontend
    "*",  # Be cautious with this in production
]

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