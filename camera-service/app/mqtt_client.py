import json
import paho.mqtt.client as mqtt
import state

from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
TOPIC_IN = "traffic/entrance"
TOPIC = "traffic/camera"

_client = None

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC_IN)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        state.entrances.append(data)
        print(
            f"[CAMERA] Received entrance {data['vehicle_id']} "
            f"from {data['camera_id']}"
        )
    except Exception as e:
        print("Camera-service error:", e)

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
    client.publish(TOPIC, json.dumps(data))