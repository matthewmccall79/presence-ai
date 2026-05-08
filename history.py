import sqlite3
from datetime import datetime

DB_NAME = "presence_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            filename TEXT,
            top_emotion TEXT,
            excited REAL,
            alert REAL,
            anxious REAL,
            duration REAL,
            rms REAL,
            zcr REAL,
            spectral_centroid REAL,
            energy_variance REAL
        )
    """)

    conn.commit()
    conn.close()

def save_analysis(filename, result):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO analyses (
            created_at,
            filename,
            top_emotion,
            excited,
            alert,
            anxious,
            duration,
            rms,
            zcr,
            spectral_centroid,
            energy_variance
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        filename,
        result["top_emotion"],
        result["probabilities"]["Excited"],
        result["probabilities"]["Alert"],
        result["probabilities"]["Anxious"],
        result["features"]["duration"],
        result["features"]["rms"],
        result["features"]["zcr"],
        result["features"]["spectral_centroid"],
        result["features"]["energy_variance"]
    ))

    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT created_at, filename, top_emotion
        FROM analyses
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def clear_history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM analyses")

    conn.commit()
    conn.close()