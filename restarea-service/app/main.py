import asyncio
from mqtt_client import connect
import state
from restarea1 import run_restarea1
from restarea2 import run_restarea2
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    if str(data.get("is_entrance", False)).lower() == "true":
        state.entrances.append(data)
    elif str(data.get("is_exit", False)).lower() == "true":
        state.exits.append(data)

async def main():
    connect(on_message)
    await asyncio.gather(
        run_restarea1(),
        run_restarea2()
    )

if __name__ == "__main__":
    asyncio.run(main())