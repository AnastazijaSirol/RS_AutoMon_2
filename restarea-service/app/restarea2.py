import asyncio
import random
from datetime import datetime, timedelta
from mqtt_client import publish_reading
import state

RESTAREA_ID = "RESTAREA2"
LOCATION = "Odmorište Rijeka"

TRAVEL_TO_RESTAREA_FROM_ENTRANCE = (3, 7)
TRAVEL_TO_RESTAREA_BEFORE_EXIT = (3, 7)
STOP_DURATION = (2, 5)
ENTRANCE_PASS_CHANCE = 0.6
EXIT_PASS_CHANCE = 0.5

async def run_restarea2():
    while True:
        for v in state.entrances:
            key = f"{v['vehicle_id']}_entry_{v['timestamp']}"
            if key in state.processed_restarea2:
                continue

            if random.random() > ENTRANCE_PASS_CHANCE:
                state.processed_restarea2.add(key)
                continue

            try:
                t_entry = datetime.strptime(v["timestamp"], "%Y-%m-%d %H:%M:%S")
            except:
                state.processed_restarea2.add(key)
                continue

            rest_entry = t_entry + timedelta(minutes=random.randint(*TRAVEL_TO_RESTAREA_FROM_ENTRANCE))
            stop_time = random.randint(*STOP_DURATION)
            rest_exit = rest_entry + timedelta(minutes=stop_time)

            data = {
                "camera_id": RESTAREA_ID,
                "camera_location": LOCATION,
                "vehicle_id": v["vehicle_id"],
                "is_restarea": True,
                "timestamp_entrance": rest_entry.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp_exit": rest_exit.strftime("%Y-%m-%d %H:%M:%S"),
            }
            publish_reading(data)
            print(f"[RESTAREA2] {v['vehicle_id']} stops {data['timestamp_entrance']}")
            state.processed_restarea1.add(key)
            await asyncio.sleep(random.uniform(1.0, 2.0))

        for v in state.exits:
            key = f"{v['vehicle_id']}_exit_{v['timestamp']}"
            if key in state.processed_restarea2:
                continue

            if random.random() > EXIT_PASS_CHANCE:
                state.processed_restarea2.add(key)
                continue

            try:
                t_exit = datetime.strptime(v["timestamp"], "%Y-%m-%d %H:%M:%S")
            except:
                state.processed_restarea2.add(key)
                continue

            rest_exit_time = t_exit - timedelta(minutes=random.randint(*TRAVEL_TO_RESTAREA_BEFORE_EXIT))
            stop_time = random.randint(*STOP_DURATION)
            rest_entry_time = rest_exit_time - timedelta(minutes=stop_time)

            data = {
                "camera_id": RESTAREA_ID,
                "camera_location": LOCATION,
                "vehicle_id": v["vehicle_id"],
                "is_restarea": True,
                "timestamp_entrance": rest_entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp_exit": rest_exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            publish_reading(data)
            print(f"[RESTAREA2] {v['vehicle_id']} stops {data['timestamp_entrance']}")
            state.processed_restarea2.add(key)
            await asyncio.sleep(random.uniform(1.0, 2.0))

        await asyncio.sleep(5)