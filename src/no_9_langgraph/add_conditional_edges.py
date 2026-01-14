from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

class CustomerState(TypedDict):
    question: str
    category: str
    answer: str

# classify --> Router: add_conditional_edges -> nodes
def classify_question(state: CustomerState):
    question = state['question'].lower()
    if "refund" in question or "return" in question:
        category = "refund"
    elif "shipping" in question or "order" in question:
        category = "shipping"
    elif "product" in question or "manual" in question:
        category = "product"
    else:
        category = "general"
    return {"category": category}

def handle_refund(state):
    return {"answer": "refund agent: please provide order_id, refund in 3 days"}

def handle_shipping(state):
    return {"answer": "shipping agent: your order is shipped."}

def handle_product(state):
    return {"answer": "product agent: please check no. 6 page"}

def handle_general(state):
    return {"answer": "general support：Hi Customer, do you have other questions"}

def route_question(state: CustomerState) -> str:
    return state["category"]

workflow = StateGraph(CustomerState)
workflow.add_node("classify", classify_question)
workflow.add_node("refund", handle_refund)
workflow.add_node("shipping", handle_shipping)
workflow.add_node("product", handle_product)
workflow.add_node("general", handle_general)
workflow.add_edge(START, "classify")
workflow.add_conditional_edges(
    "classify",
    route_question,
    {
        "refund": "refund",
        "shipping": "shipping",
        "product": "product",
        "general": "general"
    }
)

workflow.add_edge("refund", END)
workflow.add_edge("shipping", END)
workflow.add_edge("product", END)
workflow.add_edge("general", END)

app = workflow.compile()

# 测试
test_questions = [
    "I wanna return",
    "What is my order status",
    "How to use this product",
]

for q in test_questions:
    result = app.invoke({"question": q, "category": "", "answer": ""})
    print(f"question: {q}")
    print(f"answer: {result['answer']}\n")