from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from llm import llm
from no_6_agent.tools.get_weather import get_weather
from no_6_agent.tools.multiply import multiply


def create_assistant():
    checkpointer = MemorySaver()
    agent = create_agent(
        model=llm,
        tools=[get_weather, multiply],
        checkpointer=checkpointer
    )
    return agent

def main():
    agent = create_assistant()
    config = {"configurable": {"thread_id": "main"}}
    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            print("bye bye")
            break
        if not user_input:
            continue
        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config
            )
            response = result["messages"][-1].content
            print(f"小智: {response}\n")

        except Exception as e:
            print(f"出错了: {str(e)}\n")

if __name__ == "__main__":
    main()
