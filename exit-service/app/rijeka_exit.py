import asyncio
import random
from datetime import datetime, timedelta
from mqtt_client import publish_reading
import state

EXIT_ID = "RIJEKA-EXIT"
LOCATION = "Izlaz Rijeka"
TRAVEL_TIME_FROM_PULA = 90
TRAVEL_TIME_FROM_UMAG = 70
TRAVEL_VARIATION = 10
TOPIC_OUT = "traffic/exit"

async def run():
    while True:
        for e in state.entrances:
            vehicle_id = e["vehicle_id"]
            origin = e["camera_id"]
            timestamp = e["timestamp"]
            key = f"{vehicle_id}_{origin}_{timestamp}"

            if key in state.processed_rijeka or origin == "RIJEKA-ENTRANCE":
                state.processed_rijeka.add(key)
                continue

            entry_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            must_exit = False
            travel_time = None

            if origin == "PULA-ENTRANCE" and vehicle_id in state.camera1_passed and vehicle_id not in state.camera2_passed:
                must_exit = True
                travel_time = TRAVEL_TIME_FROM_PULA
            elif origin == "UMAG-ENTRANCE" and vehicle_id in state.camera1_passed and vehicle_id in state.camera2_passed:
                must_exit = True
                travel_time = TRAVEL_TIME_FROM_UMAG

            if not must_exit:
                state.processed_rijeka.add(key)
                continue

            travel_time += random.randint(-TRAVEL_VARIATION, TRAVEL_VARIATION)
            travel_time = max(1, travel_time)
            exit_time = entry_time + timedelta(minutes=travel_time)

            reading = {
                "camera_id": EXIT_ID,
                "camera_location": LOCATION,
                "vehicle_id": vehicle_id,
                "timestamp": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_exit": True
            }

            publish_reading(TOPIC_OUT, reading)
            print(f"[RIJEKA-EXIT] Vehicle {vehicle_id} exits at {reading['timestamp']}")
            state.processed_rijeka.add(key)

        await asyncio.sleep(5)
