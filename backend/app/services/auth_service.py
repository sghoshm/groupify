from supabase import Client
from postgrest.base_request_builder import APIResponse  # Import for type hinting Supabase responses
from fastapi import HTTPException ,status  # We also need to import HTTPException
from backend.app.utils.supabase_client import get_admin_supabase_client
import os

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

    # AuthService: Corrected get_current_user method
    def get_current_user(self, token: str):
        """
        Verifies JWT using Supabase and fetches the user.
        """
        try:
            if not token.startswith("Bearer "):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token must start with 'Bearer '")

            jwt_token = token.split(" ", 1)[1]
            resp = self.supabase_client.auth.get_user(jwt_token)
            
            # Check if the user object exists in the response
            if not resp.user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            return resp.user
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token: {e}")


    def refresh_session(self, refresh_token: str) -> APIResponse:
        """
        Refresh the user's session by using the provided refresh token.
        Returns the Supabase APIResponse object containing the refreshed session.
        """
        response = self.supabase_client.auth.refresh_session(refresh_token)
        return response


    # Add other auth-related methods as needed (e.g., logout, reset password, verify email)
    def logout(self) -> APIResponse:
        """
        Server-side sign out: invalidates the current session.
        Supabase Python SDK’s sign_out takes no arguments.
        """
        try:
            resp = self.supabase_client.auth.sign_out()
            print(f"Supabase Logout Response: {resp}")  # Log the response for debugging
            return resp
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Logout failed: {e}")

    def reset_password_for_email(self, email: str) -> APIResponse:
        return self.supabase_client.auth.reset_password_for_email(email)

    # Add at the bottom of AuthService
    # AuthService: Corrected admin_reset_password method
    def admin_reset_password(self, user_id: str, new_password: str) -> APIResponse:
        """
        Admin method to reset a user's password using their user_id.
        Requires Supabase service role key.
        """
        try:
            response = self.supabase_client.auth.admin.update_user_by_id(
                user_id,
                {"password": new_password}
            )
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to reset password: {str(e)}"
            )
    @staticmethod
    def login_with_google_redirect_url() -> dict:
        client = get_admin_supabase_client()
        try:
            # This generates the Google login redirect URL
            response = client.auth.sign_in_with_oauth({
                "provider": "google"
            })

            print(f"Redirect URL for Google login: {response.url}")

            return {
                "auth_url": response.url
            }

        except Exception as e:
            print(f"Error generating Google OAuth URL: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to generate Google login URL")


    @staticmethod
    def login_with_github_redirect_url() -> dict:
        client = get_admin_supabase_client()
        try:
            response = client.auth.sign_in_with_oauth({
                "provider": "github",
                "options": {
                    "redirect_to": "https://your-frontend.com/oauth/callback"
                }
            })
            return {"auth_url": response.url}
        except Exception as e:
            print(f"GitHub login failed: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to generate GitHub login URL")


    @staticmethod
    def login_with_phone_number(phone_number: str):
        client = get_admin_supabase_client()
        try:
            response = client.auth.sign_in_with_otp(phone=phone_number)
            return {"message": "OTP sent successfully"}
        except Exception as e:
            print(f"Phone OTP send failed: {str(e)}")
            raise HTTPException(status_code=400, detail="Failed to send OTP")

    @staticmethod
    def verify_phone_otp(phone_number: str, token: str):
        client = get_admin_supabase_client()
        try:
            response = client.auth.verify_otp(
                phone=phone_number,
                token=token,
                type='sms'
            )
            return {
                "session": response.session,
                "user": response.user
            }
        except Exception as e:
            print(f"OTP verification failed: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid OTP")
