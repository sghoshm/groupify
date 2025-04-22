from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router  # 💡 make sure this path is correct

app = FastAPI(title="Groupify Backend")

origins = ["*"]  # 🔐 Replace with allowed origins in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")  # 💥 this ensures /auth/register works

@app.get("/")
async def root():
    return {"message": "Groupify Backend API v1"}
