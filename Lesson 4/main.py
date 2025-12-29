from mcp.server.fastmcp import FastMCP

mcp = FastMCP('demo')

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """subtract two numbers. and return the result."""
    return a - b


if __name__ == '__main__':
    print("running...")
    mcp.run(transport='stdio')