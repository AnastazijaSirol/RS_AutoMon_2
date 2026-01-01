import random
from datetime import datetime, timedelta
from mqtt_client import publish_reading
import state
import asyncio

CAMERA_ID = "CAMERA2"
LOCATION = "Kamera Umag"

def generate_speed():
    return random.randint(90, 150)


async def process_camera2():
    while True:
        for e in state.entrances:
            key = f"{e['vehicle_id']}_{e['timestamp']}_{e['camera_id']}"
            if key in state.processed_camera2:
                continue

            origin = e["camera_id"]
            must_pass = False
            travel_time = None

            if origin == "UMAG-ENTRANCE":
                must_pass = True
                travel_time = 15

            elif origin == "RIJEKA-ENTRANCE":
                if random.random() <= 0.4:
                    must_pass = True
                    travel_time = 55

            elif origin == "PULA-ENTRANCE":
                if e["vehicle_id"] not in state.camera2_passed:
                    must_pass = True
                    travel_time = 45

            if not must_pass:
                state.processed_camera2.add(key)
                continue

            entry_time = datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S")
            travel_time += random.randint(-5, 5)
            passage_time = entry_time + timedelta(minutes=max(1, travel_time))

            reading = {
                "camera_id": CAMERA_ID,
                "camera_location": LOCATION,
                "vehicle_id": e["vehicle_id"],
                "timestamp": passage_time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_camera": True,
                "speed": generate_speed(),
                "speed_limit": 110
            }

            publish_reading(reading)
            state.processed_camera2.add(key)

            delay = 10
            if random.random() < 0.1:
                delay += random.choice([-5, 5])
                delay = max(1, delay)

            await asyncio.sleep(delay)