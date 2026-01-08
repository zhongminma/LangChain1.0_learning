from langchain_core.prompts import PromptTemplate
from llm import llm
import asyncio

prompt = PromptTemplate.from_template("answer briefly: {q}")
chain = prompt | llm
chunks: list[str] = []
async def answer_questions():
    async for chunk in chain.astream(
            {"q": "What is the color of the sun?"}):
        if chunk.content:
            chunks.append(chunk.content)
    result = "".join(chunks)
    print(result)
async def answer_event():
    async for event in chain.astream_events(
            {"q": "What is the color of the sun?"}):
        print(event["event"], event["name"])
        if event["event"] == "on_llm_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                print(chunk.content)

asyncio.run(answer_questions())
asyncio.run(answer_event())