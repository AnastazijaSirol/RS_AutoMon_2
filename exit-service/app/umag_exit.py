import asyncio
import random
from datetime import datetime, timedelta
from mqtt_client import publish_reading
import state

EXIT_ID = "UMAG-EXIT"
LOCATION = "Izlaz Umag"

TRAVEL_TIME_FROM_PULA = 60
TRAVEL_TIME_FROM_RIJEKA = 70
TRAVEL_VARIATION = 5

MIN_TRAVEL_TIME = {
    "PULA-ENTRANCE": 50,
    "RIJEKA-ENTRANCE": 60
}

async def run():
    while True:
        for e in state.entrances:
            vehicle_id = e["vehicle_id"]
            origin = e["camera_id"]
            timestamp = e["timestamp"]
            key = f"{vehicle_id}_{origin}_{timestamp}"

            if key in state.processed_umag or origin == "UMAG-ENTRANCE":
                state.processed_umag.add(key)
                continue

            try:
                entry_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                state.processed_umag.add(key)
                continue

            must_exit = False
            base_travel_time = None

            if origin == "RIJEKA-ENTRANCE" and vehicle_id in state.camera2_passed:
                must_exit = True
                base_travel_time = TRAVEL_TIME_FROM_RIJEKA

            elif origin == "PULA-ENTRANCE" and vehicle_id in state.camera2_passed:
                must_exit = True
                base_travel_time = TRAVEL_TIME_FROM_PULA

            if not must_exit:
                state.processed_umag.add(key)
                continue

            travel_time = base_travel_time + random.randint(
                -TRAVEL_VARIATION, TRAVEL_VARIATION
            )

            min_allowed = MIN_TRAVEL_TIME.get(origin, 10)
            travel_time = max(min_allowed, travel_time)

            exit_time = entry_time + timedelta(minutes=travel_time)

            reading = {
                "camera_id": EXIT_ID,
                "camera_location": LOCATION,
                "vehicle_id": vehicle_id,
                "timestamp": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_exit": True
            }

            publish_reading(reading)

            print(
                f"[UMAG-EXIT] Vehicle {vehicle_id} "
                f"({origin}) exits at {reading['timestamp']} "
                f"(travel {travel_time} min)"
            )

            state.processed_umag.add(key)

        await asyncio.sleep(5)
