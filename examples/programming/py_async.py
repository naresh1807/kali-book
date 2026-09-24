import asyncio

async def observe(value, gate):
    async with gate:
        await asyncio.sleep(0.01)
        return value * 2

async def main():
    gate = asyncio.Semaphore(2)
    print(await asyncio.gather(*(observe(x, gate) for x in range(4))))

asyncio.run(main())
