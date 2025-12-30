import sqlite3
from pathlib import Path
from .models import Reading

DB_PATH = Path("traffic.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id TEXT,
            camera_location TEXT,
            vehicle_id TEXT,
            timestamp TEXT,
            is_entrance INTEGER,
            is_exit INTEGER,
            is_camera INTEGER,
            is_restarea INTEGER,
            speed INTEGER,
            speed_limit INTEGER,
            timestamp_entrance TEXT,
            timestamp_exit TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_reading(r: Reading):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO readings VALUES (
            NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        r.camera_id,
        r.camera_location,
        r.vehicle_id,
        r.timestamp,
        int(r.is_entrance) if r.is_entrance is not None else None,
        int(r.is_exit) if r.is_exit is not None else None,
        int(r.is_camera) if r.is_camera is not None else None,
        int(r.is_restarea) if r.is_restarea is not None else None,
        r.speed if r.speed is not None else None,
        r.speed_limit if r.speed_limit is not None else None,
        r.timestamp_entrance if r.timestamp_entrance is not None else None,
        r.timestamp_exit if r.timestamp_exit is not None else None
    ))

    conn.commit()
    conn.close()
