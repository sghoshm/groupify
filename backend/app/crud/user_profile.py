from appwrite.services.databases import Databases
from app.core.config import settings
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from app.models.user_profile import UserProfile
from app.utils.appwrite_client import client

APPWRITE_DATABASE_ID = settings.APPWRITE_DATABASE_ID
USER_PROFILE_COLLECTION_ID = settings.USERS_COLLECTION_ID

async def create(user_profile: UserProfileCreate) -> UserProfileResponse:
    profile_dict = user_profile.model_dump()
    databases = Databases(client)
    result = await databases.create_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        USER_PROFILE_COLLECTION_ID,
        profile_dict,
    )
    return UserProfileResponse(**result.data, id=result.id)

async def get_by_user_id(user_id: str) -> UserProfileResponse | None:
    databases = Databases(client)
    documents = await databases.list_documents(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        USER_PROFILE_COLLECTION_ID,
        queries=[f'equal("user_id", "{user_id}")'],
    )
    if documents.total > 0:
        return UserProfileResponse(**documents.documents[0].data, id=documents.documents[0].id)
    return None

async def update(user_id: str, user_profile_in: UserProfileUpdate) -> UserProfileResponse | None:
    existing_profile = await get_by_user_id(user_id)
    if not existing_profile:
        return None

    update_data = user_profile_in.model_dump(exclude_unset=True)
    databases = Databases(client)
    result = await databases.update_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        USER_PROFILE_COLLECTION_ID,
        existing_profile.id,
        update_data,
    )
    return UserProfileResponse(**result.data, id=result.id)