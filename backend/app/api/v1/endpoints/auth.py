from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Body
from supabase import Client, create_client
from backend.app.services.auth_service import AuthService
from backend.app.utils.supabase_client import get_supabase_client
from backend.app.schemas.auth import (
    UserCreate, UserLogin, Token, RefreshTokenRequest, PasswordChange, OAuthCodePayload,
    ResetPasswordRequest, ConfirmResetRequest, 
    #PhoneNumberRequest, VerifyOTPRequest
)
import os
import traceback

router = APIRouter()

@router.post("/signup")
def signup_user(user: UserCreate, client: Client = Depends(get_supabase_client)):
    auth_service = AuthService(client)
    try:
        result = auth_service.signup(user.email, user.password)
        if not result.user:
            raise HTTPException(status_code=400, detail="Signup failed")
        return {"message": "Signup successful", "user_id": result.user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login_user(user: UserLogin, client: Client = Depends(get_supabase_client)):
    auth_service = AuthService(client)
    try:
        response = auth_service.login(user.email, user.password)
        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
def get_me(client: Client = Depends(get_supabase_client), authorization: str = Header(...)):
    return {"user": AuthService(client).get_current_user(authorization)}

@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest, client: Client = Depends(get_supabase_client)):
    auth_service = AuthService(client)
    try:
        session = auth_service.refresh_session(payload.refresh_token).session
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {e}")

@router.post("/logout", summary="Logout current user")
def logout_user(
    client: Client = Depends(get_supabase_client),
    authorization: str = Header(..., description="Bearer access token")):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid header format")

    token = authorization.split(" ")[1]
    auth_service = AuthService(client)
    
    # Even though Supabase won't invalidate the token server-side,
    # you should clear it on the client (frontend) after this call
    auth_service.get_current_user(authorization)  # Ensure token is valid
    auth_service.logout(token)

    return {"message": "Logged out. Please discard the token on the client side."}


@router.post("/change-password")
def change_password(data: PasswordChange, client: Client = Depends(get_supabase_client), authorization: str = Header(...)):
    svc = AuthService(client)
    user = svc.get_current_user(authorization)
    session = svc.login(user.email, data.current_password).session
    if session:
        result = client.auth.update_user(data={"password": data.new_password})
        return {"message": "Password updated"} if result else HTTPException(status_code=400)
    raise HTTPException(status_code=400, detail="Invalid credentials")

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, client: Client = Depends(get_supabase_client)):
    return AuthService(client).reset_password_for_email(request.email)

@router.post("/reset-password/confirm")
def confirm_reset_password(request: ConfirmResetRequest, client: Client = Depends(get_supabase_client), authorization: str = Header(...)):
    user = AuthService(client).get_current_user(authorization)
    admin = AuthService(create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY")))
    return admin.admin_reset_password(user.id, request.new_password)


@router.get("/{provider}", summary="Get OAuth URL for provider")
def oauth_redirect(provider: str, request: Request):
    """
    Returns the OAuth login URL for the given provider.
    Example: /api/v1/auth/github → { "auth_url": "https://..." }
    """
    try:
        # Optional: you can pass frontend callback in query params
        redirect_to = request.query_params.get("redirect_to")
        return AuthService.get_oauth_url(provider, redirect_to)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while generating OAuth URL: {str(e)}"
        )

'''@router.post("/oauth/exchange")
def oauth_exchange_code(
    payload: OAuthCodePayload,
    client: Client = Depends(get_supabase_client)
):
    try:
        # Wrap code in a dict with key 'code'
        response = client.auth.exchange_code_for_session({"code": payload.code})
        
        if not response.session:
            raise HTTPException(status_code=401, detail="OAuth exchange failed")

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Exchange error: {e}")


@router.post("/login/phone/send", summary="Send OTP to phone number")
def send_otp(data: PhoneNumberRequest):
    if not data.phone_number.startswith("+"):
        raise HTTPException(status_code=400, detail="Phone number must be in E.164 format, e.g., +1234567890")
    
    return AuthService.login_with_phone_number(data.phone_number)

@router.post("/login/phone/verify", summary="Verify OTP and login")
def verify_otp(data: VerifyOTPRequest):
    if not data.token or not data.phone_number:
        raise HTTPException(status_code=400, detail="Phone number and OTP token are required")
    
    return AuthService.verify_phone_otp(data.phone_number, data.token)'''