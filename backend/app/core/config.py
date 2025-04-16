import os

class Settings:
    APPWRITE_ENDPOINT: str = os.getenv("APPWRITE_ENDPOINT")
    APPWRITE_PROJECT_ID: str = os.getenv("APPWRITE_PROJECT_ID")
    APPWRITE_API_KEY: str = os.getenv("APPWRITE_API_KEY")
    APPWRITE_DATABASE_ID: str = os.getenv("APPWRITE_DATABASE_ID")
    USERS_COLLECTION_ID: str = os.getenv("USERS_COLLECTION_ID")
    CHATS_COLLECTION_ID: str = os.getenv("CHATS_COLLECTION_ID")

settings = Settings()