import asyncio
from mqtt_client import connect
import pula_exit, rijeka_exit, umag_exit

async def main():
    connect()

    await asyncio.gather(
        pula_exit.run(),
        rijeka_exit.run(),
        umag_exit.run()
    )

if __name__ == "__main__":
    asyncio.run(main())