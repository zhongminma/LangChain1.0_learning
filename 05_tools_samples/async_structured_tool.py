import asyncio
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class CaculatorInput(BaseModel):
    a: int = Field(description="1st number")
    b: int = Field(description="2nd number")

async def multiply(a: int, b: int) -> int:
    return a * b

multiply_tool = StructuredTool.from_function(
    func=multiply,
    coroutine=multiply,
    name="multiply",
    description="Multiply two numbers.",
    args_schema=CaculatorInput,
    return_direct=True,
)
print(multiply_tool)

async def main():
    result = await multiply_tool.ainvoke({"a": 4, "b": 5})
    print(result)

asyncio.run(main())