import random
import string
from datetime import datetime

def generate_random_registration():
    region = random.choice(["PU", "RI", "ZG", "ST", "ZD", "OS"])
    digits = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"{region}{digits}{letters}"

def generate_reading(camera_id, location):
    return {
        "camera_id": camera_id,
        "camera_location": location,
        "vehicle_id": generate_random_registration(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_entrance": True
    }