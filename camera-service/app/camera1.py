import random
from datetime import datetime, timedelta
from mqtt_client import publish_reading
import state
import asyncio

CAMERA_ID = "CAMERA1"
LOCATION = "Kamera Rijeka"

TRAVEL_TIME = {
    "RIJEKA-ENTRANCE": (35, 1.0),
    "PULA-ENTRANCE": (55, 0.4),
    "UMAG-ENTRANCE": (35, 0.25),
}

def generate_speed():
    return random.randint(90, 160)


async def process_camera1():
    while True:
        for e in state.entrances:
            key = f"{e['vehicle_id']}_{e['timestamp']}_{e['camera_id']}"
            if key in state.processed_camera1:
                continue

            origin = e["camera_id"]
            if origin not in TRAVEL_TIME:
                continue

            base_time, chance = TRAVEL_TIME[origin]
            if random.random() > chance:
                state.processed_camera1.add(key)
                continue

            entry_time = datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S")
            travel = base_time + random.randint(-5, 5)
            passage_time = entry_time + timedelta(minutes=max(1, travel))

            reading = {
                "camera_id": CAMERA_ID,
                "camera_location": LOCATION,
                "vehicle_id": e["vehicle_id"],
                "timestamp": passage_time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_camera": True,
                "speed": generate_speed(),
                "speed_limit": 120
            }

            publish_reading(reading)
            state.camera1_passed.add(e["vehicle_id"])
            state.processed_camera1.add(key)

            delay = 10
            if random.random() < 0.1:
                delay += random.choice([-5, 5])
                delay = max(1, delay)

            await asyncio.sleep(delay)