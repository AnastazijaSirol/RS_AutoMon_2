import json
import paho.mqtt.client as mqtt

from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
TOPIC = "traffic/entrance"

_client = None

def connect():
    global _client

    if _client is None:
        _client = mqtt.Client()
        _client.connect(BROKER, PORT)
        _client.loop_start()

    return _client


def publish_reading(data: dict):
    client = connect()
    client.publish(TOPIC, json.dumps(data))