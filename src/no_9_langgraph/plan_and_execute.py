import ast
import math
from typing import List, TypedDict, Annotated, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from llm import llm


@tool("python_calc")
def python_calc(expression: str) -> str:
    """Safely evaluate a simple math expression, e.g. 'sqrt(2)+3*5'."""
    node = ast.parse(expression, mode="eval")
    safe_env = {"sqrt": math.sqrt, "pi": math.pi}
    return str(eval(compile(node, "<expr>", "eval"), {"__builtins__": {}}, safe_env))

# 1. planner
class Plan(BaseModel):
    steps: List[str] = Field(description="A short, ordered list of steps to solve the user request.")

# 2. state
class PXState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    steps: List[str]
    i: int
    scratch: List[str]


# 3. Planner node
def planner_node(state: PXState):
    user_msg = state["messages"][-1]
    planner_prompt = SystemMessage(content=
        "You are a planner. Break the user's request into 2-6 short steps. "
        "Steps must be actionable and concrete."
    )
    plan: Plan = llm.with_structured_output(Plan).invoke([planner_prompt, user_msg])
    return {"steps": plan.steps, "i": 0, "scratch": []}


# 4. Executor Node (execute a step and trigger tool_calls)
tools = [python_calc]
tool_node = ToolNode(tools)
llm_with_tools = llm.bind_tools(tools)

def executor_node(state: PXState):
    step = state["steps"][state["i"]]
    exec_prompt = SystemMessage(content=
        "You are an executor. Execute ONLY the current step.\n"
        "If you need computation, call python_calc with ONLY a pure expression.\n"
        "Example: sqrt(2) + 3*5\n"
        "After a tool result is available, summarize it briefly."
    )
    step_msg = HumanMessage(content=f"Current step: {step}")
    resp = llm_with_tools.invoke([exec_prompt, *state["messages"], step_msg])
    return {"messages": [resp]}


# 5. route_after_executor
def route_after_executor(state: PXState) -> Literal["tools", "advance"]:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", None):
        return "tools"
    return "advance"


def advance_node(state: PXState):
    step = state["steps"][state["i"]]
    last_text = state["messages"][-1].content or ""

    new_scratch = [*state["scratch"], f"Step {state['i']+1} ({step}): {last_text}"]
    return {"scratch": new_scratch, "i": state["i"] + 1}

def route_after_advance(state: PXState) -> Literal["execute", "__end__"]:
    if state["i"] >= len(state["steps"]):
        return "__end__"
    return "execute"

# 6. Final Node
def final_node(state: PXState):
    summary_prompt = SystemMessage(content="Combine the step results into a concise final answer.")
    summary_input = HumanMessage(content="\n".join(state["scratch"]))
    final = llm.invoke([summary_prompt, summary_input])
    return {"messages": [final]}


#7. Graph
g = StateGraph(PXState)
g.add_node("plan", planner_node)
g.add_node("execute", executor_node)
g.add_node("tools", tool_node)
g.add_node("advance", advance_node)
g.add_node("final", final_node)
g.add_edge(START, "plan")
g.add_edge("plan", "execute")

g.add_conditional_edges("execute", route_after_executor, {
    "tools": "tools",
    "advance": "advance",
})

g.add_edge("tools", "advance")
g.add_conditional_edges("advance", route_after_advance, {
    "execute": "execute",
    "__end__": "final",
})
g.add_edge("final", END)
app = g.compile()


# test
query = """Do two things:
1) Compute sqrt(2) + 3*5 using python.
2) Explain in one sentence what Plan-and-Execute means.
"""
result = app.invoke({
    "messages": [HumanMessage(content=query)],
    "steps": [],
    "i": 0,
    "scratch": [],
    "step_used_tool": False,
})

print(result["messages"][-1].content)

