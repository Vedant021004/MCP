
def normal_function():
    return "Hello from normal function"


async def async_function():
    return "Hello from async function"


print(normal_function())
print(async_function())



import asyncio

async def async_function():
    print("Function started")
    return "Hello from async function"


async def main():
    result = await async_function()
    print(result)


asyncio.run(main())




import time

def task(name):
    print(name, "started")
    time.sleep(3)
    print(name, "completed")


task("Task A")
task("Task B")



import asyncio

async def task(name):
    print(name, "started")
    await asyncio.sleep(3)
    print(name, "completed")


async def main():
    await asyncio.gather(
        task("Task A"),
        task("Task B")
    )


asyncio.run(main())




import asyncio

async def get_data():
    print("Getting data...")
    await asyncio.sleep(2)
    return "Data received"


async def main():
    result = await get_data()
    print(result)


asyncio.run(main())



import asyncio
from fastmcp import Client

async def main():
    async with Client("server.py") as client:
        tools = await client.list_tools()

        for tool in tools:
            print(tool.name)

asyncio.run(main())




import asyncio
from fastmcp import Client

async def main():

        async with Client("server.py") as client:
            tools = await client.list_tools()

            for tool in tools:
                print("Tool name:", tool.name)
                print("Description:", tool.description)
                print("Input schema:", tool.inputSchema)
                print("---")

asyncio.run(main())


