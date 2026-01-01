import random
import asyncio
from entrance_base import generate_reading
from mqtt_client import publish_reading

CAMERA_ID = "PULA-ENTRANCE"
LOCATION = "Ulaz Pula"

async def run():
    while True:
        reading = generate_reading(CAMERA_ID, LOCATION)
        publish_reading(reading)

        print(f"[PULA] Vozilo {reading['vehicle_id']} enters {reading['timestamp']}")

        delay = 30
        if random.random() < 0.1:
            delay += random.choice([-5, 5])
            delay = max(1, delay)

        await asyncio.sleep(delay)