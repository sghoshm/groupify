from fastapi import APIRouter, Depends, HTTPException, Header
from app.schemas.user_profile import UserProfileResponse, UserProfileUpdate
from app.crud import user_profile as crud_user_profile
from app.utils.appwrite_client import account

router = APIRouter()

async def get_current_user(x_session: str = Header(...)):
    try:
        account._client.set_session(x_session)
        user = account.get()
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    user_id = current_user["$id"]
    profile = await crud_user_profile.get_by_user_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.put("/me", response_model=UserProfileResponse)
async def update_my_profile(
    profile_in: UserProfileUpdate,
    current_user=Depends(get_current_user),
):
    user_id = current_user["$id"]
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
