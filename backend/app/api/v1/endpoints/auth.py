# backend/app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from supabase import Client, create_client
import os
import traceback
from backend.app.services.auth_service import AuthService
from backend.app.utils.supabase_client import get_supabase_client, get_admin_supabase_client    # fixed import
from backend.app.schemas.auth import UserCreate, UserLogin, Token, RefreshTokenRequest, PasswordChange, ResetPasswordRequest, ConfirmResetRequest, GoogleAuthRequest, GitHubAuthURLResponse

router = APIRouter()


@router.post("/signup", summary="Register a new user")
def signup_user(user: UserCreate, client: Client = Depends(get_supabase_client)):
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_detail)
        user_id = auth_response.user.id
        print(f"User signed up successfully with ID: {user_id}.")
        return {"message": "User signed up successfully", "user_id": user_id}
    except Exception as e:
        print(f"Signup error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", summary="Login an existing user")
def login_user(user: UserLogin, client: Client = Depends(get_supabase_client)):
    auth_service = AuthService(client)
    try:
        response = auth_service.login(user.email, user.password)
        if not response or not getattr(response, "session", None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")
        print(f"User logged in: {response.user.id}")
        print(f"Access token: {response.session.access_token}")
        print(f"Refresh token: {response.session.refresh_token}")
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me", summary="Get the current authenticated user")
def get_me(
    client: Client = Depends(get_supabase_client),
    authorization: str = Header(..., description="Bearer access token")
):
    auth_service = AuthService(client)
    user = auth_service.get_current_user(authorization)
    return {"user": user}


@router.post("/refresh", summary="Refresh the access token using the refresh token")
def refresh_token(payload: dict, client: Client = Depends(get_supabase_client)):
    """
    Request JSON body: { "refresh_token": "…" }
    """
    rt = payload.get("refresh_token")
    if not rt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="refresh_token is required")
    auth_service = AuthService(client)
    try:
        response = auth_service.refresh_session(rt)
        if not response or not getattr(response, "session", None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        print(f"Refreshed Access token: {response.session.access_token}")
        print(f"Refreshed Refresh token: {response.session.refresh_token}")
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Refresh error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/logout", summary="Logout current user")
def logout_user(
    client: Client = Depends(get_supabase_client),
    authorization: str = Header(..., description="Bearer access token")):
    """
    Calls sign_out() (no args) on Supabase.
    Frontend should delete its token.
    """
    auth_service = AuthService(client)

    # Verify header format & token validity
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid header")
    
    # Ensure token was valid
    auth_service.get_current_user(authorization)

    # Now sign out
    resp = auth_service.logout()

    print(f"Logout Response: {resp}")  # Log the response for debugging

    # resp.error will be truthy if sign_out failed
    if getattr(resp, "error", None):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=resp.error)

    return {"message": "Logged out successfully"}


@router.post("/change-password", summary="Change user password")
def change_password(
    data: PasswordChange,
    client: Client = Depends(get_supabase_client),
    authorization: str = Header(...)):
    auth_service = AuthService(client)
    user = auth_service.get_current_user(authorization)

    # re-authenticate
    session = auth_service.login(user.email, data.current_password).session
    if session:
        result = client.auth.update_user(data={"password": data.new_password})
        if result:
            return {"message": "Password updated successfully"}
    raise HTTPException(status_code=400, detail="Password update failed")


@router.post("/reset-password", summary="Send password reset email")
def reset_password(
    request: ResetPasswordRequest,
    client: Client = Depends(get_supabase_client)
):
    auth_service = AuthService(client)
    try:
        result = auth_service.reset_password_for_email(request.email)
        return {"message": "Password reset email sent", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password/confirm")
def confirm_reset_password(
    request: ConfirmResetRequest,
    client: Client = Depends(get_supabase_client),
    authorization: str = Header(..., description="Bearer access_token")
):
    # Initialize user-facing auth service
    svc = AuthService(client)
    user = svc.get_current_user(authorization)  # This will now return the user object directly

    user_id = user.id  # Extract user ID
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")

    # Use Supabase service role key to update password
    svc_role_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
    svc_admin = AuthService(svc_role_client)
    
    # Admin method to reset the password using the user ID
    svc_admin.admin_reset_password(user_id, request.new_password)

    return {"message": "Password successfully updated"}

@router.post("/login/google")
def google_login_redirect():
    response = AuthService.login_with_google_redirect_url()
    return response

@router.post("/auth/login/github", response_model=GitHubAuthURLResponse)
def github_login():
    return AuthService.login_with_github_redirect_url()

@router.post("/login/phone/send")
def send_otp(phone: dict):
    return AuthService.login_with_phone_number(phone["phone_number"])

@router.post("/login/phone/verify")
def verify_otp(data: dict):
    return AuthService.verify_phone_otp(data["phone_number"], data["token"])
