import json
import paho.mqtt.client as mqtt
import state

from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))

TOPIC_IN_ENTRANCE = "traffic/entrance"
TOPIC_IN_EXIT = "traffic/exit"
TOPIC_OUT = "traffic/restarea"

_client = None


def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC_IN_ENTRANCE)
    client.subscribe(TOPIC_IN_EXIT)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        if str(data.get("is_entrance", False)).lower() == "true":
            state.entrances.append(data)
            print(f"[RESTAREA] Entrance {data['vehicle_id']}")

        elif str(data.get("is_exit", False)).lower() == "true":
            state.exits.append(data)
            print(f"[RESTAREA] Exit {data['vehicle_id']}")

    except Exception as e:
        print("Restarea-service error:", e)


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
    client.publish(TOPIC_OUT, json.dumps(data))