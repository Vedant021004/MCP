import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent


async def main():
    client = MultiServerMCPClient({
        "demo": {
            "transport": "http",
            "url": "https://tender-pink-sturgeon.fastmcp.app/mcp",
        }
    })

    tools = await client.get_tools()

    print("Available tools:")
    for tool in tools:
        print("-", tool.name)

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    agent = create_react_agent(
        model=model,
        tools=tools,
    )

    result = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": "Use the multiply tool to calculate 25 multiplied by 4.",
            }
        ]
    })

    print("\nAgent response:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
