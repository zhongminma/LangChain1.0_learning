import shelve
from typing import Dict
from langchain_classic.memory import ConversationBufferMemory

memory_store: Dict[str, ConversationBufferMemory] = {}
def get_memory(user_id: str, conversation_id: str) :
    key = f'{user_id}:{conversation_id}'
    if key not in memory_store:
        memory_store[key] = ConversationBufferMemory(
            memory_key= 'chat_history',
            return_messages= True,
        )
    return memory_store[key]