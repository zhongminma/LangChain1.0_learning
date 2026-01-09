from Tools.scripts.dutree import store
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from llm import llm

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)
chain = prompt | llm
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chat_with_history = RunnableWithMessageHistory(
    chain, get_session_history,
    input_messages_key = 'input',
    history_messages_key='chat_history'
)

config = {
    'configurable' : { 'session_id': 'user_1_conver_1'}
}
res1 = chat_with_history.invoke(
    {"input": "My name is Kevin."},
    config=config
)
print(res1.content)
res2 = chat_with_history.invoke(
    {"input": "What is my name?"},
    config=config
)
print(res2.content)