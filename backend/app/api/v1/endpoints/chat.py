# backend/app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
import requests
import os
# Import services, utils, and schemas using ABSOLUTE paths from backend.app
from backend.app.services.chat_service import ChatService
from backend.app.utils.supabase_client import get_supabase_client
from backend.app.schemas.chat import MessageCreate, Message, AIChatRequest # Corrected import path
# Import authentication dependency (you need to implement this)
# from backend.app.utils.dependencies import get_current_user_id # Example dependency

router = APIRouter()

# Ollama endpoint (can also be loaded via config)
# Using os.getenv directly here, but ideally loaded via a config object
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://ollama:11434")

# Example endpoint to create a room (requires authentication)
# @router.post("/rooms", summary="Create a new chat room")
# def create_room(room_name: str | None = None, is_group: bool = False, client: Client = Depends(get_supabase_client), creator_id: str = Depends(get_current_user_id)):
#     chat_service = ChatService(client)
#     try:
#         room_response = chat_service.create_chat_room(creator_id=creator_id, name=room_name, is_group=is_group)
#         if room_response.data:
#             new_room = room_response.data[0]
#             # Automatically add the creator as a member
#             member_response = chat_service.add_room_member(room_id=new_room['id'], user_id=creator_id)
#             if member_response.data:
#                  return {"message": "Room created and user added", "room": new_room}
#             else:
#                  # Handle error if creator couldn't be added as member
#                  print(f"Warning: Room created ({new_room['id']}) but creator ({creator_id}) could not be added as member.")
#                  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Room created, but failed to add creator as member.")
#         else:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create room.")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Example endpoint to get user's rooms (requires authentication)
# @router.get("/me/rooms", summary="Get rooms the current user is in")
# def get_my_rooms(client: Client = Depends(get_supabase_client), user_id: str = Depends(get_current_user_id)):
#      chat_service = ChatService(client)
#      try:
#          rooms_response = chat_service.get_user_rooms(user_id)
#          if rooms_response.data:
#              # The response format might be list of { room_id: ..., chat_rooms: { ... } }
#              # You might want to transform this data structure
#              return rooms_response.data
#          else:
#              return [] # Return empty list if no rooms found
#      except Exception as e:
#          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/message", response_model=Message, summary="Send a chat message")
# This endpoint needs authentication to get the sender_id
# def send_message(message: MessageCreate, client: Client = Depends(get_supabase_client), sender_id: str = Depends(get_current_user_id)): # Example with auth dependency
def send_message(message: MessageCreate, sender_id: str, client: Client = Depends(get_supabase_client)): # Using sender_id from request body for now
    """
    Sends a new chat message and saves it to Supabase.
    Requires sender_id (ideally from authenticated user) and message details.
    The RLS policy on 'messages' will verify sender authorization.
    """
    chat_service = ChatService(client)
    try:
        # Call the service method to insert the message
        response = chat_service.send_message(sender_id, message.room_id, message.content)

        # Check the response data
        if response.data:
             # Return the inserted message object (Supabase returns a list)
             return response.data[0]
        else:
             # This might indicate an RLS issue or database error
             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail="Failed to send message to database. Check RLS policies."
             )
    except Exception as e:
        # Catch any exceptions during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while sending message: {e}"
        )

@router.get("/room/{'{'}room_id{'}'}/messages", response_model=list[Message], summary="Get messages for a chat room")
# This endpoint needs authentication to ensure the user is in the room
# def get_messages(room_id: str, client: Client = Depends(get_supabase_client), user_id: str = Depends(get_current_user_id)): # Example with auth dependency
def get_messages(room_id: str, client: Client = Depends(get_supabase_client)): # Getting messages for a room (RLS handles access)
    """
    Retrieves all messages for a specific chat room, ordered by creation time.
    The RLS policy on the 'messages' table will determine if the requesting
    user is allowed to view these messages.
    """
    chat_service = ChatService(client)
    try:
        # Call the service method to fetch messages
        response = chat_service.get_messages(room_id)

        # Return the list of messages
        # Supabase client returns data in response.data as a list
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching messages: {e}"
        )

@router.post("/ai", summary="Send a prompt to the AI (Ollama)")
# This endpoint might also require authentication depending on your app's design
# def send_ai_message(request: AIChatRequest, current_user_id: str = Depends(get_current_user_id)): # Example with auth dependency
def send_ai_message(request: AIChatRequest): # Corrected typo: AIChatRequest
    """
    Sends a text prompt to the Ollama AI service and returns the response.
    Does not require Supabase client.
    """
    chat_service = ChatService(None) # Supabase client not needed for this service method call
    try:
        # Call the service method to get AI response
        ollama_response = chat_service.get_ai_response(request.prompt)

        if ollama_response and ollama_response.status_code == 200:
            # Return the JSON response from Ollama
            return ollama_response.json()
        else:
             # Handle cases where Ollama utility returned None or non-200 status
             status_code = ollama_response.status_code if ollama_response else status.HTTP_500_INTERNAL_SERVER_ERROR
             detail = "Failed to get response from AI service."
             if ollama_response and ollama_response.text:
                 detail += f" Ollama response: {ollama_response.text[:100]}..." # Include part of Ollama error if available

             raise HTTPException(
                 status_code=status_code,
                 detail=detail
             )
    except Exception as e:
        # Catch any exceptions during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during AI request: {e}"
        )

# Add other chat-related endpoints as needed (e.g., create room, get rooms)
