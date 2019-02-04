import asyncio
import random


async def delay_print(val):
    print(await asyncio.sleep(random.random(), result = val))


async def main():
    print("Before")
    sub1 = asyncio.create_task(delay_print("One"))
    sub2 = asyncio.create_task(delay_print("Two"))
    await sub1
    await sub2
    print("After")


if __name__ == "__main__":
    asyncio.run(main())
