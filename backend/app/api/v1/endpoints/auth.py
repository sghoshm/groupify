# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
import os
# Import services, utils, and schemas using ABSOLUTE paths from backend.app
from backend.app.services.auth_service import AuthService
# Remove UserService import as profile creation is handled by DB trigger
# from backend.app.services.user_service import UserService
from backend.app.utils.supabase_client import get_supabase_client
from backend.app.schemas.auth import UserCreate, UserLogin, Token
# Remove UserProfile import as profile creation is handled by DB trigger
# from backend.app.schemas.users import UserProfile

router = APIRouter()

# Note: Supabase URL and Key are ideally loaded via config/env vars
# Basic implementation using get_supabase_client dependency

@router.post("/signup", summary="Register a new user")
def signup_user(user: UserCreate, client: Client = Depends(get_supabase_client)):
    """
    Registers a new user with email and password using Supabase Auth.
    Profile creation is handled automatically by a database trigger.
    """
    auth_service = AuthService(client)
    # UserService is no longer needed here for profile creation
    # user_service = UserService(client)

    try:
        # Step 1: Sign up the user with Supabase Auth
        # The database trigger 'on_auth_user_created' will automatically
        # create the profile entry after this succeeds.
        # Corrected call to sign_up: Pass email and password within a dictionary
        auth_response = auth_service.signup(user.email, user.password)

        # Check if signup was successful and user object is returned
        if not auth_response.user:
             # Handle specific Supabase Auth errors
             error_detail = "Signup failed"
             if hasattr(auth_response, 'json') and callable(auth_response.json):
                 try:
                     error_json = auth_response.json()
                     error_detail = error_json.get("msg", error_json.get("message", "Signup failed"))
                 except:
                     pass # Ignore JSON parsing errors

             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail=error_detail
             )

        user_id = auth_response.user.id
        print(f"User signed up successfully with ID: {user_id}. Profile creation handled by trigger.") # Log success

        # Return success message and user ID. Profile creation is implicit via trigger.
        return {"message": "User signed up successfully (profile creation triggered)", "user_id": user_id}

    except Exception as e:
        # Catch any other exceptions during the overall process
        print(f"An unexpected error occurred during signup process: {e}") # Log error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during signup process: {e}"
        )


@router.post("/login", response_model=Token, summary="Login an existing user")
def login_user(user: UserLogin, client: Client = Depends(get_supabase_client)):
    """
    Logs in an existing user with email and password and returns a token.
    """
    auth_service = AuthService(client)
    try:
        # Corrected call to sign_in_with_password: pass email and password as POSITIONAL arguments
        response = auth_service.login(user.email, user.password)
        # Supabase login response structure might vary; adjust as needed
        if response.user and response.session:
            print(f"User logged in successfully with ID: {response.user.id}") # Log success
            return Token(access_token=response.session.access_token, token_type="bearer")
        else:
            # Handle specific Supabase errors (e.g., invalid credentials)
            error_detail = "Login failed: Invalid credentials"
            if hasattr(response, 'json') and callable(response.json):
                 try:
                     error_json = response.json()
                     error_detail = error_json.get("msg", error_json.get("message", "Login failed: Invalid credentials"))
                 except:
                     pass # Ignore JSON parsing errors

            # Ensure consistent indentation for these lines within the else block
            print(f"Login failed for email {user.email}: {error_detail}") # Log failure
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_detail
            )
    except Exception as e:
        # Generic error handling
        print(f"An unexpected error occurred during login process: {e}") # Log error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during login process: {e}"
        )

# Add other auth-related endpoints as needed (e.g., logout, password reset)
# @router.post("/logout", summary="Logout the current user")
# def logout_user(client: Client = Depends(get_supabase_client), current_user_id: str = Depends(get_current_user_id)):
#     """
#     Logs out the current user. Requires authentication.
#     (Assumes you have a dependency like get_current_user_id that extracts user ID from token)
#     """
#     auth_service = AuthService(client)
#     try:
#         # Supabase sign_out requires the access token, which is usually
#         # handled client-side. A server-side logout might invalidate the token
#         # if Supabase provides an API for that, or simply be a client-side action.
#         # This endpoint might just return a success status if logout is client-driven.
#         # If Supabase provides a server-side token invalidation API, use it here.
#         # For typical use, client-side sign_out is sufficient.
#         print(f"User {current_user_id} attempting server-side logout.")
#         # Example if a server-side invalidation exists:
#         # auth_service.logout(access_token_from_header)
#         return {"message": "Logout successful (client-side action typically)"}
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
