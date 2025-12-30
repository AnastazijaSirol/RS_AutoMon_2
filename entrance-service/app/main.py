import asyncio
from mqtt_client import connect
import pula, rijeka, umag

async def main():
    connect()

    tasks = [
        asyncio.create_task(pula.run()),
        asyncio.create_task(rijeka.run()),
        asyncio.create_task(umag.run())
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())