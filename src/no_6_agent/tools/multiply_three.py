# tools/multiply_three.py
from langchain_core.tools import tool

@tool
def multiply_three(a: int, b: int, c: int) -> int:
    """Multiply three integers."""
    return a * b * c
