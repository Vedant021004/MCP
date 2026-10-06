from mcp.server import MCPServer


# ==========================================
# MCP SERVER
# ==========================================

mcp = MCPServer(
    "My MCP Server"
)


# ==========================================
# TOOLS
# ==========================================

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def greet(name: str) -> str:
    """Greet a user."""
    return f"Hello, {name}!"


# ==========================================
# RESOURCES
# ==========================================

@mcp.resource("server://info")
def server_info() -> str:
    """Return information about the MCP server."""

    return """
MCP Server Information

Name: My MCP Server
Version: 1.0.0
Host: 0.0.0.0
Port: 8000
Transport: Streamable HTTP

Tools:
- add
- multiply
- greet

Resources:
- server://info
- config://app
"""


@mcp.resource("config://app")
def app_config() -> str:
    """Return application configuration."""

    return """
{
    "environment": "development",
    "debug": true,
    "version": "1.0.0"
}
"""


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )


# yehh