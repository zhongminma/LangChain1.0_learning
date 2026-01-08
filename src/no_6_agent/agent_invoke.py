from langchain.agents import create_agent
from langchain.messages import HumanMessage

from llm import llm
from no_6_agent.tools.multiply_three import multiply_three

agent = create_agent(
    model=llm,
    tools=[multiply_three],
    system_prompt="You are a helpful assistant. Use tools when needed."
)

result = agent.invoke(
    {
        "messages": [HumanMessage(content="What is 17 * 23? Use the tool.")]
    },
)

print(result)

