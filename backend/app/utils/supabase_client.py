# backend/app/utils/supabase_client.py
from supabase import create_client, Client
from backend.app.core.config import settings

def get_supabase_client() -> Client:
    """
    Returns a Supabase client using the anon public key.
    Suitable for user-side operations like login/signup.
    """
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_KEY  # anon key
    return create_client(url, key)

def get_admin_supabase_client() -> Client:
    """
    Returns a Supabase client using the service role key.
    Required for admin actions like resetting passwords.
    """
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_ROLE_KEY  # service role key
    return create_client(url, key)
