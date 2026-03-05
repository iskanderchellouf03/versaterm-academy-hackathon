import sqlite3
from src.config import DB_PATH

_db_initialized = False


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    global _db_initialized
    if _db_initialized:
        return
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS access_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            expires_at DATETIME NOT NULL,
            used BOOLEAN DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            expires_at DATETIME NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    _db_initialized = True
