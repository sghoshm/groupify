# backend/app/utils/supabase_client.py
from supabase import create_client, Client
from backend.app.core.config import settings # Import settings from core config using absolute path

def get_supabase_client() -> Client:
    """
    Provides a Supabase client instance using configured settings.
    This function can be used as a FastAPI dependency.
    """
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_KEY # This should be the anon key
    # Consider adding error handling for invalid URL/Key
    return create_client(url, key)

# Consider adding functions for common Supabase interactions if not handled by services
# def get_user_by_id(client: Client, user_id: str):
#     return client.from_("profiles").select("*").eq("id", user_id).execute()
