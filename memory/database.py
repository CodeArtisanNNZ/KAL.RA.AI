import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "assistant.db"


def connect():
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_key TEXT UNIQUE NOT NULL,
                memory_value TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_memory(memory_key, memory_value):
    with connect() as connection:
        connection.execute("""
            INSERT INTO memories (memory_key, memory_value) VALUES (?, ?)
            ON CONFLICT(memory_key) DO UPDATE SET
                memory_value = excluded.memory_value,
                updated_at = CURRENT_TIMESTAMP
        """, (memory_key, memory_value))


def get_memory(memory_key):
    with connect() as connection:
        result = connection.execute(
            "SELECT memory_value FROM memories WHERE memory_key = ?", (memory_key,)
        ).fetchone()
    return result[0] if result else None


def get_all_memories():
    with connect() as connection:
        return connection.execute(
            "SELECT memory_key, memory_value FROM memories ORDER BY updated_at DESC"
        ).fetchall()


def delete_memory(memory_key):
    with connect() as connection:
        cursor = connection.execute("DELETE FROM memories WHERE memory_key = ?", (memory_key,))
    return cursor.rowcount > 0
