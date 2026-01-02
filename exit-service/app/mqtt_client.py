import json
import paho.mqtt.client as mqtt
import state

from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))

TOPIC_IN_CAMERA = "traffic/camera"
TOPIC_IN_ENTRANCE = "traffic/entrance"
TOPIC_OUT = "traffic/exit"

_client = None


def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC_IN_CAMERA)
    client.subscribe(TOPIC_IN_ENTRANCE)


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

        print(f"[EXIT] Received {vehicle_id} from {cam_id}")

    except Exception as e:
        print("Exit-service error:", e)


def connect():
    global _client
    if _client is None:
        _client = mqtt.Client()
        _client.on_connect = on_connect
        _client.on_message = on_message
        _client.connect(BROKER, PORT)
        _client.loop_start()
    return _client


def publish_reading(data: dict):
    client = connect()
    client.publish(TOPIC_OUT, json.dumps(data), retain=False)