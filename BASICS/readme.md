Python with vs async with — Beginner-Friendly Guide
A simple, practical guide to understanding why with and async with exist, what happens without them, and how async with is used in an MCP client.
Main idea: with and async with help manage a resource's lifecycle. They arrange setup and cleanup around a block of code. The difference is whether that resource management is synchronous or asynchronous.

Table of Contents
1. The real-life idea
2. What is a resource?
3. Without with: manage cleanup yourself
4. With with: cleanup is handled for you
5. What problem does async with solve?
6. A runnable async with example
7. Compare with and async with
8. Understand the MCP client example
9. Common misunderstandings
10. Practice questions
11. Quick recap
1. The real-life idea
Imagine you enter a room, use something, and then leave. You should make sure the room is left in a proper state when you finish.

Programs also use resources that should be cleaned up after use. Examples include:
- Files
- Network connections
- Database connections
- MCP client sessions
A program needs to set up these resources, use them, and then clean them up.

That is the basic problem with and async with help solve.
2. What is a resource?
A resource is something a program uses that may need to be opened, connected, or released.

For example, a file should be closed after writing. A client session should be closed after communicating with a server.

Consider this MCP client:
async with Client("server.py") as client:
    result = await client.call_tool(
        "add",
        {"a": 10, "b": 20}
    )
    print(result.data)
There are two separate ideas here:
- async with manages the client's lifecycle (enter/setup and exit/cleanup).
- await client.call_tool(...) waits for the asynchronous tool call to return.
They are not the same thing.
3. Without with: manage cleanup yourself
Here is a simplified file example that opens a file and closes it manually:
file = open("demo.txt", "w")

try:
    file.write("Hello, Vedant!")
finally:
    file.close()

print("File work finished")
What happens?
1. open(...) opens the file.
2. write(...) writes the text.
3. The finally block closes the file even if an error happens inside the try block.
4. The program continues.
This works, but you have to remember to write the cleanup code correctly every time.

If you forget to close the file, the resource may remain open longer than necessary.
4. With with: cleanup is handled for you
The same task can be written more simply:
with open("demo.txt", "w") as file:
    file.write("Hello, Vedant!")

print("File work finished")
The with statement arranges for the file to be closed when execution leaves the indented block, including when an exception occurs.
Compare them
Without with	With with
You explicitly manage cleanup, often using try/finally.	The context manager handles cleanup.
More code to maintain.	Usually shorter and easier to read.
Easy to forget cleanup if code is poorly structured.	Cleanup is tied to the block's lifecycle.


Important: with does not automatically make the file operation faster. Its main job is safe resource management.
5. What problem does async with solve?
Some resources have asynchronous setup or cleanup. For example, establishing or closing a network session may involve waiting for I/O.

A normal with is designed for synchronous context managers. An asynchronous context manager supports asynchronous entry and exit, so Python uses:
async with some_async_resource() as resource:
    # use the resource
    ...
async with is used inside an async def function.
The simple lifecycle
Enter async context / setup
            |
            v
       Use resource
            |
            v
Exit async context / cleanup
In Python, an asynchronous context manager provides special methods named __aenter__() and __aexit__(). You normally do not call these methods yourself; async with handles them.
6. A runnable async with example
This example imitates a connection. It does not connect to a real server; it only demonstrates the order of setup, work, and cleanup.
import asyncio


class DemoConnection:
    async def __aenter__(self):
        print("Connection opened")
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        print("Connection cleaned up")

    async def do_work(self):
        print("Doing work...")
        await asyncio.sleep(1)
        print("Work completed")


async def main():
    async with DemoConnection() as connection:
        await connection.do_work()

    print("Outside the connection block")


asyncio.run(main())
Expected output:
Connection opened
Doing work...
Work completed
Connection cleaned up
Outside the connection block
Read the output in order
1. __aenter__() runs when entering the async with block.
2. The returned object is assigned to connection.
3. await connection.do_work() runs the example operation.
4. When the block exits, __aexit__() runs for cleanup.
5. The final print runs after the context has exited.
The await asyncio.sleep(1) line simulates asynchronous waiting. While this coroutine is suspended, the event loop can run other scheduled tasks.
7. Compare with and async with
Feature	with	async with
Intended for	Synchronous context managers	Asynchronous context managers
Example	with open(...) as file:	async with Client(...) as client:
Setup/cleanup	Synchronous context-manager protocol	Asynchronous context-manager protocol
Where used	Ordinary functions or async functions, depending on the resource	Inside an async def function
Does it automatically make code faster?	No	No
Main benefit	Resource lifecycle and cleanup	Resource lifecycle and cleanup when entry/exit are asynchronous


What about await?
await and async with do different jobs:
async with Client("server.py") as client:
    result = await client.call_tool("add", {"a": 10, "b": 20})
- async with: manages the client's lifecycle.
- await: waits for the asynchronous call_tool operation to finish and gives you its result.
Neither keyword guarantees that every operation runs in parallel. Async is especially useful for I/O-bound work when tasks can make progress while other operations wait.
8. Understand the MCP client example
Suppose your MCP server contains tools called add and multiply.

A client can call the add tool like this:
import asyncio
from fastmcp import Client


async def main():
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print("-", tool.name)

        result = await client.call_tool(
            "add",
            {"a": 10, "b": 20}
        )
        print("Addition result:", result.data)


if __name__ == "__main__":
    asyncio.run(main())
Line-by-line explanation
async def main():

Defines the coroutine that contains the client's asynchronous workflow.

async with Client("server.py") as client:

Enters the FastMCP client's asynchronous context. The client manages the connection/session lifecycle for the block. With this local-script configuration, FastMCP launches/connects to the server process using its configured transport.

tools = await client.list_tools()

Requests the list of tools and waits for the result.

await client.call_tool("add", {"a": 10, "b": 20})

Requests the add tool with arguments a=10 and b=20, then waits for the tool-call result.

asyncio.run(main())

Starts the event loop to execute the top-level coroutine.

When execution leaves the async with block, the context manager handles client cleanup.
9. Common misunderstandings
Does async with make the program faster?
Not by itself. Its main purpose is to manage asynchronous resources correctly. Async I/O can improve responsiveness when the program has other tasks to run while waiting.
Is await the same as async with?
No.
- await: wait for one awaitable operation to complete.
- async with: manage an asynchronous resource's entry and exit.
Can I use async with anywhere?
No. It is normally used inside an async def function, and the object after async with must support the asynchronous context-manager protocol.
Do I need to write __aenter__() and __aexit__() in every project?
No. Libraries such as FastMCP implement the required behavior for their client objects. You use async with Client(...) without implementing those methods yourself.
10. Practice questions
Try answering before checking the answers.
1. What is the main purpose of with?
2. Why might a client connection need cleanup?
3. What does async with manage in the FastMCP client?
4. What is the difference between await client.call_tool(...) and async with Client(...)?
5. Does adding async automatically make a program faster?
<details>
<summary>Show answers</summary>

1. To manage a resource's lifecycle and ensure cleanup.
2. To release resources and close the session/connection appropriately.
3. The client's asynchronous context and lifecycle.
4. async with manages the client lifecycle; await waits for the tool call's result.
5. No. Async helps when asynchronous operations can make progress during I/O waits.
</details>

11. Quick recap
Remember these three points:
- with: use a resource and let its context manager handle cleanup.
- async with: the same lifecycle idea for an asynchronous context manager.
- await: wait for an asynchronous operation's result.
For MCP, this is the key pattern:
async with Client("server.py") as client:
    result = await client.call_tool("add", {"a": 10, "b": 20})
    print(result.data)
First, async with manages the client session. Then await waits for the tool call. When the block ends, the context manager cleans up the client.