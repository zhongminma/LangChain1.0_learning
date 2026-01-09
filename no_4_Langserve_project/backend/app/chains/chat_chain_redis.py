from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

llm = ChatOpenAI(
    model="gpt-4o-mini",
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

# 内存存储
_STORE: dict[str, InMemoryChatMessageHistory] = {}

def get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _STORE:
        _STORE[session_id] = InMemoryChatMessageHistory()
    return _STORE[session_id]

chat_chain_redis = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)
