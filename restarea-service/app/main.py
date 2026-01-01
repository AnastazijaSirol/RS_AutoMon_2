import asyncio
from mqtt_client import connect
from restarea1 import run_restarea1
from restarea2 import run_restarea2

async def main():
    connect()

    await asyncio.gather(
        run_restarea1(),
        run_restarea2()
    )

if __name__ == "__main__":
    asyncio.run(main())