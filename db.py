import sqlite3

DB_NAME = "x7.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            verdict TEXT NOT NULL,
            score INTEGER NOT NULL,
            reasons TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_scan(url, verdict, score, reasons):
    conn = get_connection()
    conn.execute(
        "INSERT INTO scans (url, verdict, score, reasons) VALUES (?, ?, ?, ?)",
        (url, verdict, score, " | ".join(reasons)),
    )
    conn.commit()
    conn.close()


def get_recent_scans(limit=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM scans ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows