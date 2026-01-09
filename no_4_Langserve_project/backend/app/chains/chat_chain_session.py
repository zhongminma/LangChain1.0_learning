from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

print(">>> building chat_chain")
import os
print(">>> OPENAI_API_KEY =", os.environ.get("OPENAI_API_KEY"))

llm = ChatOpenAI(
    model="gpt-4o",   # ⚠️ 先不要用 mini
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

base_chain = prompt | llm

STORE: dict[str, InMemoryChatMessageHistory] = {}

def get_history(session_id: str):
    print(f">>> get_history called, session_id={session_id}")
    return STORE.setdefault(session_id, InMemoryChatMessageHistory())

chat_chain_session = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)
