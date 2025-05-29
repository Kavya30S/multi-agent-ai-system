import sqlite3
from datetime import datetime
import uuid

class MemoryManager:
    def __init__(self, db_path="memory/memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database with a table for context."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS context (
                    thread_id TEXT PRIMARY KEY,
                    source_type TEXT,
                    intent TEXT,
                    timestamp TEXT,
                    extracted_fields TEXT
                )
            """)
            conn.commit()

    def save_context(self, source_type, intent, extracted_fields):
        """Save context to SQLite with a unique thread ID."""
        thread_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO context (thread_id, source_type, intent, timestamp, extracted_fields) VALUES (?, ?, ?, ?, ?)",
                (thread_id, source_type, intent, timestamp, str(extracted_fields))
            )
            conn.commit()
        return thread_id

    def retrieve_context(self, thread_id):
        """Retrieve context by thread ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM context WHERE thread_id = ?", (thread_id,))
            result = cursor.fetchone()
            if result:
                return {
                    "thread_id": result[0],
                    "source_type": result[1],
                    "intent": result[2],
                    "timestamp": result[3],
                    "extracted_fields": result[4]
                }
        return None