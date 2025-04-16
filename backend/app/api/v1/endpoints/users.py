from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_profile import UserProfileResponse, UserProfileUpdate
from app.crud import user_profile as crud_user_profile

router = APIRouter()

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile():
    # In a real application, you would get the current user's ID from the authentication context
    # For now, we'll assume a placeholder user ID
    user_id = "some-user-id"  # Replace with actual logic to get current user ID
    profile = await crud_user_profile.get_by_user_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.put("/me", response_model=UserProfileResponse)
async def update_current_user_profile(profile_in: UserProfileUpdate):
    # In a real application, you would get the current user's ID from the authentication context
    # For now, we'll assume a placeholder user ID
    user_id = "some-user-id"  # Replace with actual logic to get current user ID
    profile = await crud_user_profile.update(user_id, profile_in)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    profile = await crud_user_profile.get_by_user_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile
