from supabase import Client
from postgrest.base_request_builder import APIResponse
from fastapi import HTTPException, status
from backend.app.utils.supabase_client import get_admin_supabase_client
import os

class AuthService:
    def __init__(self, supabase_client: Client):
        self.supabase_client = supabase_client

    def signup(self, email: str, password: str) -> APIResponse:
        return self.supabase_client.auth.sign_up({"email": email, "password": password})

    def login(self, email: str, password: str) -> APIResponse:
        return self.supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

    def get_current_user(self, token: str):
        try:
            if not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Token must start with 'Bearer '")

            access_token = token.split(" ", 1)[1]

            # Check if token is blacklisted
            blacklist_check = self.supabase_client.table("token_blacklist").select("*").eq("token", access_token).execute()

            if blacklist_check.data and len(blacklist_check.data) > 0:
                raise HTTPException(status_code=401, detail="Token is blacklisted")

            resp = self.supabase_client.auth.get_user(access_token)

            if not resp.user:
                raise HTTPException(status_code=404, detail="User not found")

            return resp.user

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")


    def refresh_session(self, refresh_token: str) -> APIResponse:
        return self.supabase_client.auth.refresh_session(refresh_token)

    def logout(self, access_token: str) -> APIResponse:
        """
        Logs out the user and blacklists the token to prevent reuse.
        """
        try:
            if not access_token:
                raise ValueError("Access token is required for logout.")

            # Get current user info
            user_response = self.supabase_client.auth.get_user(access_token)
            if not user_response or not user_response.user:
                raise HTTPException(status_code=401, detail="Invalid token.")

            user_id = user_response.user.id

            # Store token in blacklist table
            insert_response = self.supabase_client.table("token_blacklist").insert({
                "token": access_token,
                "user_id": user_id
            }).execute()

            print(f"Token blacklisted for user {user_id}")

            # Optional: log out from Supabase session as well
            self.supabase_client.auth.sign_out()

            return insert_response

        except Exception as e:
            print(f"Logout failed: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Logout failed: {e}")


    def reset_password_for_email(self, email: str) -> dict:
        try:
            self.supabase_client.auth.reset_password_for_email(
                email,
                options={"redirect_to": os.getenv("RESET_PASSWORD_REDIRECT_URL", "http://localhost:3000/reset-password")}
            )

            # Even if no response is returned, assume success if no exception is raised
            return {
                "message": "Password reset link sent successfully.",
                "email": email
            }

        except Exception as e:
            print(f"Password reset error: {e}")
            raise HTTPException(status_code=400, detail=f"Reset failed: {e}")



    def admin_reset_password(self, user_id: str, new_password: str) -> APIResponse:
        try:
            return self.supabase_client.auth.admin.update_user_by_id(
                user_id,
                {"password": new_password}
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to reset password: {str(e)}")

    @staticmethod
    def get_oauth_url(provider: str, redirect_to: str = None) -> dict:
        """
        Generates a Supabase OAuth redirect URL for supported providers.
        """
        client = get_admin_supabase_client()

        # Supported providers
        valid_providers = {"google", "github", "facebook", "azure"}

        if provider not in valid_providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OAuth provider: '{provider}'. Supported providers: {', '.join(valid_providers)}"
            )

        try:
            # Fallback redirect if not provided
            redirect_to = redirect_to or os.getenv("OAUTH_REDIRECT_URL", "http://localhost:3000/oauth/callback")

            # Construct payload for Supabase
            payload = {
                "provider": provider,
                "options": {
                    "redirect_to": redirect_to
                }
            }

            # Request Supabase to generate URL
            response = client.auth.sign_in_with_oauth(payload)

            if not hasattr(response, "url") or not response.url:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to retrieve OAuth redirect URL from Supabase."
                )

            return {"auth_url": response.url}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"OAuth URL generation failed for '{provider}': {str(e)}"
            )
'''    @staticmethod
    def login_with_phone_number(phone_number: str):
        client = get_admin_supabase_client()
        try:
            # Wrap phone inside a dict as per Supabase SDK
            client.auth.sign_in_with_otp({"phone": phone_number})
            return {"message": "OTP sent"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to send OTP: {e}")


    @staticmethod
    def verify_phone_otp(phone_number: str, token: str):
        client = get_admin_supabase_client()
        try:
            response = client.auth.verify_otp(
                phone=phone_number,
                token=token,
                type='sms'
            )

            if not response.session:
                raise HTTPException(status_code=401, detail="OTP verification failed")

            # Update phone_verified in profiles
            user_id = response.user.id
            update_resp = client.table("profiles").update({
                "phone_number": phone_number,
                "phone_verified": True
            }).eq("id", user_id).execute()

            return {
                "session": response.session,
                "user": response.user,
                "profile_update": update_resp.data
            }
        except Exception as e:
            print(f"OTP verification failed: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid OTP")
'''