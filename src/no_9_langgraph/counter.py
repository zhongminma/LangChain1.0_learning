from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# state
class CounterState(TypedDict):
    count: int
    history: list[int]

# Node
def increment_counter(state: CounterState):
    new_counter = state['count'] + 1
    message = f"increment -> count: {new_counter}"
    return {
        "count": new_counter,
        "history": state['history'] + [message]
    }

def double_node(state: CounterState):
    new_counter = state['count'] * 2
    message = f"double -> count: {new_counter}"
    return {
        "count": new_counter,
        "history": state['history'] + [message]
    }

def report_node(state: CounterState):
    return {"history": state['history'] + [f"Final Result: {state['count']}"]}

# stop condition router
def should_continue(state: CounterState) -> str:
    return "report" if state['count'] >= 200 else "increment"

# graph + add nodes and edges
workflow = StateGraph(CounterState)
workflow.add_node("double", double_node)
workflow.add_node("increment", increment_counter)
workflow.add_node("report", report_node)
workflow.add_edge(START, "double")
workflow.add_conditional_edges("double", should_continue)
workflow.add_edge("increment", "double")
workflow.add_edge("report", END)
# compile
app = workflow.compile()
result = app.invoke({ "count": 3,"history": ['execute']})

print('execute begin')
for step in result['history']:
    print(step)
print(f"\nfinal result: {result['count']}")
