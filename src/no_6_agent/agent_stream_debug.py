from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from llm import llm
from no_6_agent.tools.multiply_three import multiply_three


def _print_message(msg):
    #  AIMessage -> tool_call
    if isinstance(msg, AIMessage):
        if getattr(msg, "tool_calls", None):
            print("TOOL_CALLS:", msg.tool_calls)
        if msg.content:
            print("AI:", msg.content)
    # ToolMessage -> tool_result
    elif isinstance(msg, ToolMessage):
        print(f"TOOL_RESULT name={msg.name} content={msg.content}")
    else:
        print("MSG:", msg)

def main():
    agent = create_agent(
        model=llm,
        tools=[multiply_three],
        system_prompt=(
            "You are a math assistant. "
            "When multiplication is required, you MUST use the provided tool."
        ),
    )
    messages = [
        HumanMessage(
            content=(
                "Calculate the following step by step:\n"
                "1) 2 * 3 * 4\n"
                "2) Take the result and multiply by 5\n"
                "Show intermediate results."
            )
        )
    ]

    for chunk in agent.stream({"messages": messages}):
        print("CHUNK TYPE:", type(chunk))
        print("CHUNK RAW :", chunk)
        if isinstance(chunk, dict):
            if "messages" in chunk and chunk["messages"]:
                last = chunk["messages"][-1]
                _print_message(last)
            elif "output" in chunk:
                print("OUTPUT:", chunk["output"])
        elif isinstance(chunk, (AIMessage, ToolMessage)):
            _print_message(chunk)

if __name__ == '__main__':
    main()