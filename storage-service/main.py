from storage.database import init_db
from storage.mqtt_listener import start_listener

if __name__ == "__main__":
    print("Starting storage-service...")
    init_db()
    start_listener()