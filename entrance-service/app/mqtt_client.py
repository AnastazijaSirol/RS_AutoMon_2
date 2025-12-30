import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "traffic/entrance"

def connect():
    client = mqtt.Client()
    client.connect("localhost", 1883)
    return client

def publish_reading(data: dict):
    client = connect()
    client.publish(TOPIC, json.dumps(data))