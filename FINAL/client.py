import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


async def main():

    # Connect to MCP server
    client = MultiServerMCPClient(
        {
            "demo": {
                "command": "python",
                "args": ["mcp_server.py"],
                "transport": "stdio",
            }
        }
    )

    # Get tools exposed by MCP server
    tools = await client.get_tools()

    print("Available tools:")
    for tool in tools:
        print("-", tool.name)

    # LLM
    model = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    # LangGraph agent
    agent = create_react_agent(
        model=model,
        tools=tools,
    )

    # Ask agent
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 25 multiplied by 4?"
                }
            ]
        }
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())