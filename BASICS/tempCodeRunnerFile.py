

import asyncio

async def get_data():
    print("Getting data...")
    await asyncio.sleep(2)
    return "Data received"


async def main():
    result = await get_data()
    print(result)


asyncio.run(main())