import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from models import Message

# Update this with your Railway DB URL or keep as localhost for local testing
DATABASE_URL = "your_database_url_here"

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    session TEXT,
                    role TEXT,
                    content TEXT
                )
            """)
            conn.commit()

def register_user(email: str, password_hash: str) -> bool:
    try:
        with get_connection() as conn:
            with conn.cursor() as c:
                c.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password_hash))
                conn.commit()
                return True
    except:
        return False

def get_user(email: str):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT * FROM users WHERE email = %s", (email,))
            return c.fetchone()

def save_message(user_id: int, session: str, role: str, content: str):
    with get_connection() as conn:
        with conn.cursor() as c:
            c.execute(
                "INSERT INTO chats (user_id, session, role, content) VALUES (%s, %s, %s, %s)",
                (user_id, session, role, content)
            )
            conn.commit()

def get_messages(user_id: int, session: str) -> List[Message]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT role, content FROM chats WHERE user_id = %s AND session = %s", (user_id, session))
            rows = c.fetchall()
            return [Message(role=row["role"], content=row["content"]) for row in rows]

def get_all_sessions(user_id: int) -> List[str]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT DISTINCT session FROM chats WHERE user_id = %s ORDER BY id DESC", (user_id,))
            rows = c.fetchall()
            return [row["session"] for row in rows]
