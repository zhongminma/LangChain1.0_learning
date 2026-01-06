from langchain_core.tools import tool, StructuredTool, ToolException
from pydantic import BaseModel, Field

class CaculatorInput(BaseModel):
    a: int = Field(description="1st number")
    b: int = Field(description="2nd number")

def multiply(a: int, b: int) -> int:
    if b == 0:
        raise ToolException('b can not be 0')
    return a * b

def _handle_tool_error (error: ToolException)  -> str:
    return f'Tool failed. Please try again with different inputs'

multiply_tool = StructuredTool.from_function(
    func=multiply,
    name="multiply",
    description="Multiply two numbers.",
    args_schema=CaculatorInput,
    return_direct=True,
    handle_tool_error=_handle_tool_error,
)
print(multiply_tool.invoke({'a': 4, 'b' : 5}))
print(multiply_tool.invoke({'a': 4, 'b' : 0}))