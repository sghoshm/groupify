from appwrite.services.databases import Databases
from app.core.config import settings
from app.schemas.chat import ChatCreate, ChatUpdate, ChatResponse
from app.models.chat import Chat
from app.utils.appwrite_client import client

APPWRITE_DATABASE_ID = settings.APPWRITE_DATABASE_ID
CHAT_COLLECTION_ID = settings.CHATS_COLLECTION_ID

async def create(chat: ChatCreate) -> ChatResponse:
    chat_dict = chat.model_dump()
    databases = Databases(client)
    result = await databases.create_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        CHAT_COLLECTION_ID,
        chat_dict,
    )
    return ChatResponse(**result.data, id=result.id)

async def get_by_group_id(group_id: str) -> ChatResponse | None:
    databases = Databases(client)
    documents = await databases.list_documents(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        CHAT_COLLECTION_ID,
        queries=[f'equal("group_id", "{group_id}")'],
    )
    if documents.total > 0:
        return ChatResponse(**documents.documents[0].data, id=documents.documents[0].id)
    return None

async def update(group_id: str, chat: ChatUpdate) -> ChatResponse | None:
    existing_chat = await get_by_group_id(group_id)
    if not existing_chat:
        return None

    update_data = chat.model_dump(exclude_unset=True)
    databases = Databases(client)
    result = await databases.update_document(
        settings.APPWRITE_PROJECT_ID,
        APPWRITE_DATABASE_ID,
        CHAT_COLLECTION_ID,
        existing_chat.id,
        update_data,
    )
    return ChatResponse(**result.data, id=result.id)