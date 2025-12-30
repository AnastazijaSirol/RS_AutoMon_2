import asyncio
import json
import state
import mqtt_client
import pula_exit, rijeka_exit, umag_exit

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        state.entrances.append(data)

        vehicle_id = data.get("vehicle_id")
        cam_id = data.get("camera_id")
        if cam_id == "CAMERA1":
            state.camera1_passed.add(vehicle_id)
        elif cam_id == "CAMERA2":
            state.camera2_passed.add(vehicle_id)
    except Exception as e:
        print("Exit-service error", e)

mqtt_client.connect(
    on_message_callback=on_message,
    topics=["traffic/camera", "traffic/entrance"]
)

async def main():
    await asyncio.gather(
        pula_exit.run(),
        rijeka_exit.run(),
        umag_exit.run()
    )

if __name__ == "__main__":
    asyncio.run(main())
