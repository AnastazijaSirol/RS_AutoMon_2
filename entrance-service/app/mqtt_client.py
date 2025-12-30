import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
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