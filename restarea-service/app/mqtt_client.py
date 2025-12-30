import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

_client = None

def connect(on_message_callback):
    global _client
    if _client is None:
        _client = mqtt.Client()
        _client.on_message = on_message_callback
        _client.connect(BROKER, PORT)
        _client.subscribe("traffic/entrance")
        _client.subscribe("traffic/exit")
        _client.loop_start()
    return _client

def publish_restarea(data: dict):
    if _client is None:
        raise RuntimeError("MQTT client not connected")
    _client.publish("traffic/restarea", json.dumps(data))