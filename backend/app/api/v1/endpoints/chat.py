from fastapi import APIRouter, Depends, HTTPException
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
