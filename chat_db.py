import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from models import Message
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def create_tables():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id SERIAL PRIMARY KEY,
                    session TEXT,
                    role TEXT,
                    content TEXT
                )
            """)
            conn.commit()

def save_message(session: str, role: str, content: str):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO chats (session, role, content) VALUES (%s, %s, %s)",
                (session, role, content)
            )
            conn.commit()

def get_messages(session: str) -> List[Message]:
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT role, content FROM chats WHERE session = %s", (session,))
            rows = c.fetchall()
            return [Message(role=row["role"], content=row["content"]) for row in rows]

def get_all_sessions() -> List[str]:
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("SELECT DISTINCT session FROM chats ORDER BY id DESC")
            rows = c.fetchall()
            return [row["session"] for row in rows]
