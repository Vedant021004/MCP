
import asyncio
from fastmcp import Client


async def main():
    url = "https://tender-pink-sturgeon.fastmcp.app/mcp"

    try:
        async with Client(url) as client:
            print("Connected to FastMCP Cloud!")

            tools = await client.list_tools()

            print("\nAvailable tools:")
            for tool in tools:
                print("-", tool.name)

    except Exception as e:
        print("Connection failed!")
        print("Error type:", type(e).__name__)
        print("Error details:", repr(e))


if __name__ == "__main__":
    asyncio.run(main())
