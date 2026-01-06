from llm import llm
import asyncio
async def check_event():
    events = []
    async for event in llm.astream_events(input="Aloha"):
        events.append(event)
    print(events)
asyncio.run(check_event())