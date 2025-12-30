import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

_client = None

TOPIC_IN = "traffic/entrance"
TOPIC_IN2 = "traffic/exit"
TOPIC_OUT = "traffic/restarea"

def connect(on_message_callback):
    global _client
    if _client is None:
        _client = mqtt.Client()
        _client.on_message = on_message_callback
        _client.connect(BROKER, PORT)
        _client.subscribe(TOPIC_IN)
        _client.subscribe(TOPIC_IN2)
        _client.loop_start()
    return _client

def publish_reading(data: dict):
    if _client is None:
        raise RuntimeError("MQTT client not connected")
    _client.publish(TOPIC_OUT, json.dumps(data))