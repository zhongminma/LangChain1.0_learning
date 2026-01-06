from langchain.tools import tool
from pydantic import Field, BaseModel


class CaculatorInput(BaseModel):
    a: int = Field(description="1st number")
    b: int = Field(description="2nd number")

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@tool(args_schema=CaculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

print(add.name, add.description, add.args)
print(multiply.name, multiply.description, multiply.args)