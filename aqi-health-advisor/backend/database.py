import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "advisor.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            age_group TEXT,
            medical_history TEXT,
            occupation TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS advisory_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            lat REAL,
            lon REAL,
            aqi INTEGER,
            temp REAL,
            humidity REAL,
            wind_speed REAL,
            advisory_text TEXT,
            precautions TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            alert_type TEXT,
            message TEXT,
            severity TEXT
        )
    """)

    conn.commit()
    conn.close()