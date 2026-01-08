from langchain.agents import create_agent
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage

from llm import llm
from no_6_agent.tools.multiply_three import multiply_three


def main():
    agent = create_agent(
        model=llm,
        tools=[multiply_three],
        system_prompt=(
            "You are a math assistant."
            "When multiplication is required, you MUST use the provided tool."
        ),
    )
    messages = [
        HumanMessage(content=(
                "Calculate the following step by step:\n"
                "1) 2 * 3 * 4\n"
                "2) Take the result and multiply by 5\n"
                "Show intermediate results."
            )
        )
    ]
    for chunk in agent.stream({"messages": messages}):
        # tool_result
        if "tools" in chunk:
            for msg in chunk["tools"]["messages"]:
                if isinstance(msg, ToolMessage):
                    print(f"tool_result is: name={msg.name}, output={msg.content}")
        #  tool_call / final
        if "model" in chunk:
            for msg in chunk["model"]["messages"]:
                if isinstance(msg, AIMessage):
                    if msg.tool_calls:
                        for call in msg.tool_calls:
                            print(f"tool_call is: name={call['name']}, args={call['args']}")
                    if msg.content and not msg.tool_calls:
                        print("\nFINAL ANSWER:")
                        print(msg.content)
if __name__ == "__main__":
    main()