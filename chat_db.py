
import sqlite3
from typing import List
from models import Message

DB_PATH = "chat_history.db"

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session TEXT,
                role TEXT,
                content TEXT
            )
        """)
        conn.commit()

def save_message(session: str, role: str, content: str):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO chats (session, role, content) VALUES (?, ?, ?)",
                  (session, role, content))
        conn.commit()

def get_messages(session: str) -> List[Message]:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT role, content FROM chats WHERE session = ?", (session,))
        rows = c.fetchall()
        return [Message(role=row[0], content=row[1]) for row in rows]

def get_all_sessions() -> List[str]:
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT DISTINCT session FROM chats ORDER BY id DESC")
        return [row[0] for row in c.fetchall()]
