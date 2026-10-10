
import asyncio
from fastmcp import Client
from langchain.mcp import MCPAdapter
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

SERVER_URL = "http://127.0.0.1:8000/mcp"


async def main():
    mcp_client = Client(SERVER_URL)

    async with MCPAdapter(mcp_client) as adapter:
        tools = await adapter.list_tools()
        print("MCP tools:", [tool.name for tool in tools])

        llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0,
        )

        agent = create_react_agent(
            model=llm,
            tools=tools,
        )

        print("\nMCP Agent is ready! Type 'exit' to quit.")

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not user_input:
                continue

            try:

                response = await agent.ainvoke({
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                })

                for message in response["messages"]:
                    if getattr(message, "tool_calls", None):
                        for call in message.tool_calls:
                            print(
                                f"\n[MCP TOOL REQUEST] "
                                f"{call['name']}({call['args']})"
                            )
                    elif getattr(message, "type", "") == "tool":
                        print(
                            f"[TOOL RESULT] {message.name}: "
                            f"{message.content}"
                        )

                print("\nAgent:", response["messages"][-1].content)


            except Exception as e:
                print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
