import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "slovio_memory.db")

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, timestamp TEXT, type TEXT, content TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY, timestamp TEXT, role TEXT, content TEXT)")
    return conn

def remember(record_type, content):
    conn = _get_conn()
    ts = datetime.datetime.now().isoformat()
    conn.execute("INSERT INTO memory (timestamp, type, content) VALUES (?, ?, ?)", (ts, record_type, content))
    conn.commit()
    conn.close()

def recall(query):
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, type, content FROM memory WHERE content LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

def save_conversation_turn(role, content):
    conn = _get_conn()
    ts = datetime.datetime.now().isoformat()
    conn.execute("INSERT INTO conversations (timestamp, role, content) VALUES (?, ?, ?)", (ts, role, content))
    conn.commit()
    conn.close()

def get_recent_conversation(n=20):
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM conversations ORDER BY timestamp DESC LIMIT ?", (n,))
    results = cursor.fetchall()
    conn.close()
    return list(reversed(results))
