import sqlite3
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = Path(os.getenv("DB_PATH"))

def get_connection():
    return sqlite3.connect(DB_PATH)