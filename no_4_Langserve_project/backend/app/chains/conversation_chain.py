from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.store.history_store import get_history

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

base_chain = prompt | llm

def build_chain(user_id: str, conversation_id: str):
    """
    return a runnable with memory history
    - every invoke will read from history firstly.
    """
    return RunnableWithMessageHistory(
        base_chain,
        lambda session_id: get_history(user_id, conversation_id),  # session_id 不用，key 用 user/conv
        input_messages_key="input",
        history_messages_key="chat_history",
    )
