from supabase import Client
from postgrest.base_request_builder import APIResponse  # Import for type hinting Supabase responses
from fastapi import HTTPException  # We also need to import HTTPException

class AuthService:
    """Service class for handling authentication logic with Supabase."""
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def signup(self, email: str, password: str) -> APIResponse:
        """
        Calls Supabase Auth to sign up a new user.
        Returns the Supabase APIResponse object.
        """
        # Corrected call to sign_up: Pass email and password within a dictionary
        response = self.supabase_client.auth.sign_up({"email": email, "password": password})
        return response

    def login(self, email: str, password: str) -> APIResponse:
        """
        Calls Supabase Auth to log in an existing user.
        Returns the Supabase APIResponse object containing user and session.
        """
        # Corrected call: pass email and password inside a dictionary
        response = self.supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response

    def get_current_user(self, token: str):
        """
        Verifies JWT using Supabase and fetches the user.
        """
        try:
            if not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Token must start with 'Bearer '")

            jwt_token = token.split(" ")[1]
            user = self.supabase_client.auth.get_user(jwt_token)
            return user
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")

    # Add other auth-related methods as needed (e.g., logout, reset password, verify email)
    # def logout(self, access_token: str) -> APIResponse:
    #     return self.supabase_client.auth.sign_out(access_token)

    # def reset_password_for_email(self, email: str) -> APIResponse:
    #     return self.supabase_client.auth.reset_password_for_email(email)
