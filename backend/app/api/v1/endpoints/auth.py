import uuid
from fastapi import APIRouter, HTTPException
from appwrite.exception import AppwriteException
from appwrite.query import Query
from app.utils.appwrite_client import account, database
from app.core.config import settings
from app.schemas.user_profile import UserProfileCreate, UserLoginSchema, UserProfileResponse
from app.models.user_profile import UserProfile

router = APIRouter()

@router.post("/register", response_model=UserProfileResponse)
def register_user(user: UserProfileCreate):
    try:
        user_res = account.create(
            user_id=uuid.uuid4().hex,
            email=user.email,
            password=user.password,
            name=user.username,
        )

        profile = UserProfile(**user.model_dump(exclude={"password"}))
        profile.user_id = user_res["$id"]

        doc = database.create_document(
            settings.APPWRITE_DATABASE_ID,
            settings.USERS_COLLECTION_ID,
            "unique()",
            profile.to_dict(),
        )

        payload = profile.to_dict()
        payload.update({"id": doc["$id"]})
        return UserProfileResponse.model_validate(payload)

    except AppwriteException as e:
        raise HTTPException(status_code=400, detail=e.message or "Registration failed")

@router.post("/login", response_model=UserProfileResponse)
def login_user(user: UserLoginSchema):
    try:
        # Create a session using email and password
        session = account.create_email_password_session(email=user.email, password=user.password)
        
        # Retrieve the authenticated user's account information
        me = account.get()

        # Query the database for the user's profile
        docs = database.list_documents(
            settings.APPWRITE_DATABASE_ID,
            settings.USERS_COLLECTION_ID,
            queries=[Query.equal("user_id", me["$id"])],
        )

        if docs.get("total", 0) == 0:
            raise HTTPException(status_code=404, detail="User profile not found")

        profile = UserProfile.from_appwrite_document(docs["documents"][0])
        payload = profile.to_dict()
        payload.update({"id": docs["documents"][0]["$id"]})
        return UserProfileResponse.model_validate(payload)

    except AppwriteException as e:
        raise HTTPException(status_code=401, detail=e.message or "Invalid credentials")