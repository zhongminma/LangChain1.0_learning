import sys

from fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    print(f"[MCP] add({a}, {b})", file=sys.stderr)
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    print(f"[MCP] multiply({a}, {b})", file=sys.stderr)
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
