import sqlite3
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

PATH = os.getenv("PATH")

DB_PATH = Path(PATH)

def get_connection():
    return sqlite3.connect(DB_PATH)