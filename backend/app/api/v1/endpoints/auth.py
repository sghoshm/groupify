# backend/app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Header
from supabase import Client
import os
from backend.app.services.auth_service import AuthService
from backend.app.utils.supabase_client import get_supabase_client     # fixed import
from backend.app.schemas.auth import UserCreate, UserLogin, Token

router = APIRouter()

@router.post("/signup", summary="Register a new user")
def signup_user(user: UserCreate, client: Client = Depends(get_supabase_client)):
    """
    Registers a new user with email and password using Supabase Auth.
    Profile creation is handled automatically by a database trigger.
    """
    auth_service = AuthService(client)

    try:
        auth_response = auth_service.signup(user.email, user.password)

        if not auth_response.user:
            error_detail = "Signup failed"
            if hasattr(auth_response, "json") and callable(auth_response.json):
                try:
                    error_json = auth_response.json()
                    error_detail = error_json.get("msg", error_json.get("message", error_detail))
                except:
                    pass

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_detail
            )

        user_id = auth_response.user.id
        print(f"User signed up successfully with ID: {user_id}. Profile creation handled by trigger.")
        return {"message": "User signed up successfully (profile creation triggered)", "user_id": user_id}

    except Exception as e:
        print(f"An unexpected error occurred during signup process: {e}")
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
        response = auth_service.login(user.email, user.password)
        if response.user and response.session:
            print(f"User logged in successfully with ID: {response.user.id}")
            return Token(access_token=response.session.access_token, token_type="bearer")
        else:
            error_detail = "Login failed: Invalid credentials"
            if hasattr(response, "json") and callable(response.json):
                try:
                    error_json = response.json()
                    error_detail = error_json.get("msg", error_json.get("message", error_detail))
                except:
                    pass

            print(f"Login failed for email {user.email}: {error_detail}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_detail
            )
    except Exception as e:
        print(f"An unexpected error occurred during login process: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during login process: {e}"
        )


@router.get("/me", summary="Get the current authenticated user")
def get_me(
    client: Client = Depends(get_supabase_client),
    authorization: str = Header(..., description="Bearer access token")
):
    """
    Returns the currently authenticated user's info by verifying
    the Supabase JWT passed in the Authorization header.
    """
    auth_service = AuthService(client)
    user = auth_service.get_current_user(authorization)
    return {"user": user}
