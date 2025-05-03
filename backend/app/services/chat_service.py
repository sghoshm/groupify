# backend/app/services/chat_service.py
from supabase import Client
from ..utils.ollama_client import generate_text_with_ollama # Import AI utility

class ChatService:
    """Service class for handling chat and AI interaction logic."""
    def __init__(self, supabase_client: Client | None):
        # Supabase client might be None if the service is used only for AI
        self.supabase_client = supabase_client

    def send_message(self, sender_id, room_id, content):
        """Inserts a new message into the 'messages' table."""
        if not self.supabase_client:
            raise ValueError("Supabase client is not initialized for sending messages.")
        # Add validation or data formatting if needed
        return self.supabase_client.from_("messages").insert({"sender_id": sender_id, "room_id": room_id, "content": content}).execute()

    def get_messages(self, room_id):
        """Fetches messages for a specific room."""
        if not self.supabase_client:
            raise ValueError("Supabase client is not initialized for getting messages.")
        # Add sorting, filtering, or pagination if needed
        return self.supabase_client.from_("messages").select("*").eq("room_id", room_id).order("created_at").execute()

    def get_ai_response(self, prompt):
        """Sends a prompt to the Ollama AI utility."""
        # Add prompt engineering or response parsing if needed
        return generate_text_with_ollama(prompt)

    # Add other chat-related methods (e.g., create room, add user to room)
