import uuid
from fastapi import APIRouter, Depends, HTTPException
from appwrite.exception import AppwriteException
from app.utils.appwrite_client import account, database
from app.core.config import settings
from app.schemas.user_profile import UserProfileCreate, UserProfileResponse
from app.models.user_profile import UserProfile

router = APIRouter()
APPWRITE_DATABASE_ID = "67fcce30000cb2d2fec9"  # Your Appwrite database ID
USER_PROFILE_COLLECTION_ID = "67fcd214000dd0f539f6"  # Your user profile collection ID

@router.post("/register", response_model=UserProfileResponse)
def register_user(user: UserProfileCreate):
    try:
        user_result = account.create(
            user_id=uuid.uuid4().hex,
            email=user.email,
            password="super-secure-pwd",
            name=user.username
        )

        profile = UserProfile(**user.model_dump(exclude={"user_id"}))
        profile.user_id = user_result["$id"]

        profile_document = database.create_document(
            APPWRITE_DATABASE_ID,
            USER_PROFILE_COLLECTION_ID,
            "unique()",
            profile.to_dict()
        )

        return UserProfileResponse.model_validate({
            **profile.to_dict(),
            "id": profile_document["$id"]
        })

    except AppwriteException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.post("/login", response_model=UserProfileResponse)
async def login_user(user: UserProfileCreate):  # Using UserProfileCreate for simplicity, you might want a dedicated Login schema
    try:
        session = await account.create_session(user.email, "super-secure-pwd")
        user_data = await account.get()
        profile_document = await database.list_documents(
            settings.APPWRITE_PROJECT_ID,
            APPWRITE_DATABASE_ID,
            USER_PROFILE_COLLECTION_ID,
            queries=[f'equal("user_id", "{user_data.id}")'],
        )
        if profile_document.total == 0:
            raise HTTPException(status_code=404, detail="User profile not found")
        profile = UserProfile.from_appwrite_document(profile_document.documents[0])
        return UserProfileResponse.from_attributes(profile)
    except AppwriteException as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Add more authenticatioon endpoints like logout, get current user, etc.