import asyncio
import time

async def fun1():
    print("started fun1")
    await asyncio.sleep(2)
    print("Ended fun1")

async def fun2():
    print("started fun2")
    await asyncio.sleep(4)
    print("Ended fun2")

async def main():
    await asyncio.gather(fun1(), fun2())  # Wrap gather in a coroutine

asyncio.run(main())  # Pass the coroutine to asyncio.run()