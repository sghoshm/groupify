# backend/app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
# Import service, utils, and schemas using ABSOLUTE paths from backend.app
from backend.app.services.user_service import UserService
from backend.app.utils.supabase_client import get_supabase_client
from backend.app.schemas.users import UserProfile

router = APIRouter()

# Note: You will likely need an authentication dependency here
# to get the ID of the currently authenticated user making the request.
# Example (you'd need to implement get_current_user_id):
# from backend.app.utils.dependencies import get_current_user_id
# @router.get("/me", response_model=UserProfile, summary="Get current user's profile")
# def get_current_user_profile(current_user_id: str = Depends(get_current_user_id), client: Client = Depends(get_supabase_client)):
#     user_service = UserService(client)
#     try:
#         response = user_service.get_user_profile(current_user_id)
#         if response.data:
#             return response.data[0]
#         else:
#             # This case should ideally not happen if user is authenticated but good to handle
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found for authenticated user.")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{'{'}user_id{'}'}", response_model=UserProfile, summary="Get user profile by ID")
def get_user(user_id: str, client: Client = Depends(get_supabase_client)):
    """
    Retrieves a user's profile information from Supabase by their UUID.
    The RLS policy on the 'profiles' table will determine if the requesting
    user is authorized to view this profile.
    """
    user_service = UserService(client)
    try:
        # Call the service method to fetch the profile
        response = user_service.get_user_profile(user_id)

        # Check the response data
        # Supabase client returns data in response.data as a list
        if response.data:
            # Return the first item in the data list (assuming user_id is unique)
            return response.data[0]
        else:
            # If data is empty, the user was not found or RLS prevented access
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found or access denied."
            )
    except Exception as e:
        # Catch any exceptions during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching user: {e}"
        )

# Add other user-related endpoints as needed (e.g., update profile)
# @router.put("/me", response_model=UserProfileUpdate, summary="Update current user's profile")
# def update_current_user_profile(profile_update: UserProfileUpdate, current_user_id: str = Depends(get_current_user_id), client: Client = Depends(get_supabase_client)):
#     user_service = UserService(client)
#     try:
#         # Call the service method to update the profile
#         response = user_service.update_user_profile(current_user_id, profile_update.model_dump(exclude_unset=True)) # Use model_dump for Pydantic v2+
#         if response.data:
#             return response.data[0]
#         else:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update profile.")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
