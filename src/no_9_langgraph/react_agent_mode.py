import ast
import math
import operator
import statistics

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing import Annotated, Literal
from typing_extensions import TypedDict

from llm import llm
@tool("python_executor")
def python_executor(expression: str) -> str:
    """
    Evaluate a simple Python expression safely.
    Allowed: numbers, + - * / **, parentheses, and a few math functions.
    Example input: "sqrt(2) + 3*5"
    """
    try:
        node = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        return f"Invalid expression syntax: {e}"

    # 2) whitelist
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
        ast.USub, ast.UAdd,
        ast.Constant,
        ast.Call,
        ast.Name,
        ast.Load,
    )

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            return f"Unsafe expression: contains disallowed node {type(n).__name__}"

        if isinstance(n, ast.Attribute):
            return "Unsafe expression: attribute access is not allowed"

        if isinstance(n, ast.Subscript):
            return "Unsafe expression: subscripts are not allowed"

    safe_env = {
        "sqrt": math.sqrt,
        "pow": pow,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "mean": statistics.mean,
        "pi": math.pi,
        "e": math.e,
    }
    try:
        result = eval(compile(node, "<expr>", "eval"), {"__builtins__": {}}, safe_env)
    except Exception as e:
        return f"Error while evaluating: {e}"

    return str(result)

# --- Tool 2: Text Analyzer ---
@tool("text_analyzer")
def text_analyzer(text: str, top_k: int = 8) -> Dict[str, Any]:
    """
    Analyze text: basic stats + top frequent words.
    Returns a JSON-like dict.
    """
    import re
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    char_count = len(text)
    word_count = len(words)
    unique_words = len(set(words))

    from collections import Counter
    freq = Counter(words).most_common(max(1, top_k))

    return {
        "char_count": char_count,
        "word_count": word_count,
        "unique_words": unique_words,
        "top_words": [{"word": w, "count": c} for w, c in freq],
    }

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    iterations: Annotated[int, operator.add]


tools = [python_executor, text_analyzer]
tool_node = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)


def call_model(state: AgentState):
    messages = state["messages"]
    response_msg = llm_with_tools.invoke(messages)
    return {"messages": [response_msg], "iterations": 1}


def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    # 对大多数 provider，AIMessage 有 tool_calls 属性
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return "__end__"

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "__end__": END})
workflow.add_edge("tools", "agent")

app = workflow.compile()

init_state: AgentState = {"messages": [], "iterations": 0}

query = """Please do two things:
1) Use python to calculate sqrt(2) + 3*5
2) Analyze this text: "LangGraph is great. LangGraph makes tools easy."
Return a concise final answer.
"""

result = app.invoke({"messages": [HumanMessage(content=query)], "iterations": 0})
print("iterations:", result["iterations"])
print("final:", result["messages"][-1].content)