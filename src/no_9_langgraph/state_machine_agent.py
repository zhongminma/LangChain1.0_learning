from typing import TypedDict, Literal, Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from llm import llm


# 1. state
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    intent: Literal["chat", "math", "done"]
    result: str

# 2. Tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# 3. Node - 1, 2, 3
def classify_node(state: AgentState):
    user_text = state["messages"][-1].content.lower()
    if "add" in user_text or "+" in user_text:
        intent = "math"
    else:
        intent = "chat"
    return {"intent": intent}
def math_node(state: AgentState):
    result = add.invoke({"a": 2, "b": 3})
    return {
        "result": str(result),
        "messages": [AIMessage(content=f"The result is {result}")],
        "intent": "done"
    }
def chat_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {
        "messages": [response],
        "intent": "done"
    }

# 4. route
def route_by_intent(state: AgentState) -> Literal["math", "chat", "__end__"]:
    if state["intent"] == "math":
        return "math"
    if state["intent"] == "chat":
        return "chat"
    return "__end__"

# 5. graph
graph = StateGraph(AgentState)
graph.add_node("classify", classify_node)
graph.add_node("math", math_node)
graph.add_node("chat", chat_node)
graph.add_edge(START, "classify")
graph.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "math": "math",
        "chat": "chat",
        "__end__": END,
    }
)
graph.add_edge("math", END)
graph.add_edge("chat", END)
app = graph.compile()

# 6. test
state = {
    "messages": [HumanMessage(content="Please add 2 and 3")],
    "intent": "",
    "result": "",
}
result = app.invoke(state)
print(result["messages"][-1].content)
