from langchain_core.prompts import PromptTemplate
from llm import llm
import asyncio

prompt = PromptTemplate.from_template("answer briefly: {q}")
chain = prompt | llm
async def answer_event():
    async for event in chain.astream_events(
            {"q": "What is the color of the sun?"},
            version="v1"
    ):
        print(event["event"], event["name"])
        if event["event"] == "on_llm_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                print(chunk.content)
asyncio.run(answer_event())