# mcp_langgraph_client.py
import asyncio
import os
import sys
from typing import Annotated, Literal, TypedDict, List
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def should_continue(state: State) -> Literal["tools", "__end__"]:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        print("🔧 TOOL CALL DETECTED:", last.tool_calls)
        return "tools"
    return "__end__"


async def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "mcp_math_server.py")

    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": sys.executable,   # ✅ venv python
                "args": [server_path],       # ✅ absolute path
                "cwd": base_dir,             # ✅ stable cwd
            }
        }
    )

    tools = await client.get_tools()
    llm_with_tools = llm.bind_tools(tools)

    def agent_node(state: State):
        system = HumanMessage(
            content="You MUST use available tools to do math. Do NOT calculate mentally."
        )
        resp = llm_with_tools.invoke([system, *state["messages"]])
        return {"messages": [resp]}

    tool_node = ToolNode(tools)

    g = StateGraph(State)
    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)

    g.add_edge(START, "agent")
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", "__end__": END})
    g.add_edge("tools", "agent")

    app = g.compile()

    result = await app.ainvoke(
        {"messages": [HumanMessage(content="Compute (3 + 5) * 12. Use tools.")]}
    )
    print("✅ FINAL:", result["messages"][-1].content)

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

# run python mcp_langgraph_client.py