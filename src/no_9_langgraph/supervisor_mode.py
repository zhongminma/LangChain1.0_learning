from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.tools import tool
from typing import Annotated, Literal, Sequence, Dict, Any

from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

from llm import llm


# 1. state (SupervisorState)
class RouteDecision(BaseModel):
    next: Literal["tech_support", "sales", "billing"] = Field(
        description="Which specialist should handle the user's request"
    )
    reason: str = Field(description="Short reason for routing decision")

class SupervisorState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next: str  # next Agent
    reason: str

# 2. tools
@tool
def check_system_status(component: str) -> str:
    """check system component status"""
    status = {"database": "Good", "server": "High Load", "api": "Normal"}
    return status.get(component, "Unknown")

@tool
def get_product_info(product_name: str) -> str:
    """track product info"""
    products = {
        "Basic": "$19/m，basic functionality",
        "Professional": "$79/m，professional functionality",
    }
    return products.get(product_name, "product not found")

@tool
def query_invoice(order_id: str) -> str:
    """track receipt invoice"""
    invoices = {"ORD001": "receipt sent", "ORD002": "processing"}
    return invoices.get(order_id, "order not found")

# 3. nodes (specialist agents)
def tech_agent_node(state):
    """ tech_support Agent """
    last_message = state["messages"][-1].content
    if "system" in last_message or "server" in last_message:
        result = check_system_status.invoke({"component": "server"})
        response = f"[technical support] system status: {result}"
    else:
        response = "[technical support] Please describe the tech question you are facing."
    return {"messages": [AIMessage(content=response)]}

def sales_agent_node(state):
    """Sales Agent"""
    last_message = state["messages"][-1].content
    for product in ["Basic", "Professional"]:
        if product in last_message:
            info = get_product_info.invoke({"product_name": product})
            return {"messages": [AIMessage(content=f"[sales person]]{info}")]}
    return {"messages": [AIMessage(content="[sales person] We have a basic and professional, which one do you want?")]}

def billing_agent_node(state):
    """ Billing Agent"""
    return {"messages": [AIMessage(content="[order tracker] Please provide the order number, I will check it.")]}

# 4. Supervisor
def supervisor_node(state):
    """Supervisor：please decide next step"""
    last_message = state["messages"][-1].content
    tech_keywords = ["error", "bug", "crash", "system", "server"]
    sales_keywords = ["price", "buy", "product", "menu"]
    billing_keywords = ["receipt", "pay", "refund", "bill"]

    if any(kw in last_message for kw in tech_keywords):
        next_agent = "tech_support"
    elif any(kw in last_message for kw in sales_keywords):
        next_agent = "sales"
    elif any(kw in last_message for kw in billing_keywords):
        next_agent = "billing"
    else:
        next_agent = "sales"  # 默认销售
    return {"next": next_agent}

# 5. routing: route_after_supervisor
def route_after_supervisor(state) -> Literal["tech_support", "sales", "billing"]:
    return state["next"]

def supervisor_node(state: SupervisorState):
    history = list(state["messages"])[-10:]
    system = SystemMessage(content=
        "You are a routing supervisor for a customer support system.\n"
        "Your job is to decide which specialist should handle the user's last message.\n"
        "Pick exactly ONE of: tech_support, sales, billing.\n"
        "Return a JSON object with keys: next, reason.\n"
        "Routing rules:\n"
        "- tech_support: errors, bugs, crashes, server/system issues, API down, performance.\n"
        "- sales: pricing, plans, features, product comparison, purchasing.\n"
        "- billing: invoices, receipts, payments, refunds, charges.\n"
        "If unclear, choose sales and ask a clarifying question in reason."
    )
    structured_llm = llm.with_structured_output(RouteDecision)
    try:
        decision: RouteDecision = structured_llm.invoke([system, *history])
        nxt = decision.next
        reason = decision.reason
    except Exception as e:
        nxt = "sales"
        reason = f"Fallback to sales due to routing parse error: {e}"
    return {"next": nxt, "reason": reason}

# 6. graph
workflow = StateGraph(SupervisorState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("tech_support", tech_agent_node)
workflow.add_node("sales", sales_agent_node)
workflow.add_node("billing", billing_agent_node)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "tech_support": "tech_support",
        "sales": "sales",
        "billing": "billing",
    }
)
workflow.add_edge("tech_support", END)
workflow.add_edge("sales", END)
workflow.add_edge("billing", END)

app = workflow.compile()

# 7. test
test_cases = [
    "I am facing 500 server error, the system is shut down.",
    "What is the price for professional",
    "I need to check the receipt",
]

for query in test_cases:
    print(f"User: {query}")
    result = app.invoke({"messages": [HumanMessage(content=query)], "next": "", "reason": ""})
    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            print(msg.content)
    print()