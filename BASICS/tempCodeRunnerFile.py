import asyncio
from fastmcp import Client

async def main():
    async with Client("server.py") as client:

        async with Client("server.py") as client:
            tools = await client.list_tools()

            for tool in tools:
                print("Tool name:", tool.name)
                print("Description:", tool.description)
                print("Input schema:", tool.inputSchema)
                print("---")

asyncio.run(main())