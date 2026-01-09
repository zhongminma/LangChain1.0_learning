from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from llm import llm

DB_URL = "sqlite:///./chat_history.db"
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
chain = prompt | llm

def get_session_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=DB_URL,
    )

chat_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "user_1_conver_1"}}
res1 = chat_with_history.invoke({"input": "My name is Kevin."}, config=config)
print(res1.content)
res2 = chat_with_history.invoke({"input": "What is my name?"}, config=config)
print(res2.content)
