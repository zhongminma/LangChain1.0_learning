from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph

from llm import llm


class ChatState(MessagesState):
    user_name: str
    conversation_count: int

def chatbot_node(state: ChatState):
    """chat nodes"""
    system_prompt = f"""You are a helpful assistant.
    username: {state.get('user_name', 'user')}
    Current is the No. {state.get('conversation_count', 0)} round conver"""
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response_msg = llm.invoke(messages)

    return {
        "messages": [response_msg],
        "conversation_count": state.get("conversation_count", 0) + 1
    }

# graph
workflow = StateGraph(ChatState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)
app = workflow.compile()
# multiple rounds conversation
state = {"messages": [], "user_name": "小明", "conversation_count": 0}
conversations = [
    "Hello, this is Kevin Ma",
    "What is my name",
    "please recommend me a book related Python LLM"
]

for user_input in conversations:
    print(f"user: {user_input}")
    state["messages"].append(HumanMessage(content=user_input))
    result = app.invoke(state)
    state = {**state, **result}
    print(f"assistant: {result['messages'][-1].content}\n")