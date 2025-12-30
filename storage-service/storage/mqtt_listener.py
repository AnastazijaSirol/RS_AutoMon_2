import json
import paho.mqtt.client as mqtt

from .models import Reading
from .database import insert_reading

BROKER = "localhost"
PORT = 1883

TOPICS = [
    ("traffic/entrance", 0),
]

def on_connect(client, userdata, flags, rc):
    print("Storage connected to MQTT")
    for topic, qos in TOPICS:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        reading = Reading(**payload)
        insert_reading(reading)
        print(f"Stored {reading.vehicle_id} ({reading.camera_id})")
    except Exception as e:
        print("Error:", e)

def start_listener():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_forever()