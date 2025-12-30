import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

_client = None

def connect(on_message_callback=None, topics=None):
    global _client
    if _client is None:
        _client = mqtt.Client()
        if on_message_callback:
            _client.on_message = on_message_callback
        _client.connect(BROKER, PORT)
        if topics:
            for topic in topics:
                _client.subscribe(topic)
        _client.loop_start()
    return _client

def publish_reading(topic, data):
    client = connect()
    client.publish(topic, json.dumps(data), retain=True)
