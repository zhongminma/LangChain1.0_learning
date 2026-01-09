import os
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def get_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    session_id = f"{user_id}:{conversation_id}"
    return RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        ttl=60 * 60 * 24 * 7,
    )
