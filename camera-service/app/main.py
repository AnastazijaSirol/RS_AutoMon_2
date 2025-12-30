import asyncio
from mqtt_client import connect
import camera1, camera2

async def main():
    connect()

    tasks = [
        asyncio.create_task(camera1.process_camera1()),
        asyncio.create_task(camera2.process_camera2())
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())