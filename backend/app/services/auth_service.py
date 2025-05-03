from supabase import Client
from postgrest.base_request_builder import APIResponse  # Import for type hinting Supabase responses

class AuthService:
    """Service class for handling authentication logic with Supabase."""
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def signup(self, email: str, password: str) -> APIResponse:
        """
        Calls Supabase Auth to sign up a new user.
        Returns the Supabase APIResponse object.
        """
        response = self.supabase_client.auth.sign_up({"email": email, "password": password})
        return response

    def login(self, email: str, password: str) -> APIResponse:
        """
        Calls Supabase Auth to log in an existing user.
        Returns the Supabase APIResponse object containing user and session.
        """
        # ✅ FIX: wrap email and password in a dictionary
        response = self.supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response

    # Add other auth-related methods as needed (e.g., logout, reset password, verify email)
    # def logout(self, access_token: str) -> APIResponse:
    #     return self.supabase_client.auth.sign_out(access_token)

    # def reset_password_for_email(self, email: str) -> APIResponse:
    #     return self.supabase_client.auth.reset_password_for_email(email)
