from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.store.memory_store import get_memory

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{input}')]
)
def build_chain(user_id: str, conversation_id: str):
    memory = get_memory(user_id, conversation_id)
    return prompt | llm | memory
