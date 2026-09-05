import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        bot_response TEXT,
        mood TEXT,
        category TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        status TEXT DEFAULT 'Open',
        category TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    hashed_pw = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    if user and check_password_hash(user[1], password):
        return user[0]
    return None

def log_chat(user_msg, bot_msg, user_id=None, mood="Neutral", category="General"):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chats (user_id, user_message, bot_response, mood, category) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_msg, bot_msg, mood, category)
    )
    conn.commit()
    conn.close()

def create_ticket(user_msg, user_id=None, category="General"):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tickets (user_id, user_message, category) VALUES (?, ?, ?)", (user_id, user_msg, category))
    ticket_id = cur.lastrowid
    conn.commit()
    conn.close()
    return ticket_id

def save_feedback(rating, user_id=None, comment=""):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (user_id, rating, comment) VALUES (?, ?, ?)", (user_id, rating, comment))
    conn.commit()
    conn.close()

def get_recent_history(user_id=None, limit=5):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    # Check if table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chats'")
    if not cur.fetchone():
        conn.close()
        return []

    if user_id:
        cur.execute("SELECT user_message, bot_response FROM chats WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
    else:
        cur.execute("SELECT user_message, bot_response FROM chats ORDER BY id DESC LIMIT ?", (limit,))
        
    rows = cur.fetchall()
    conn.close()
    
    history = []
    for user_msg, bot_msg in reversed(rows):
        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": bot_msg})
    return history

def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT id, user_message, timestamp 
        FROM chats 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (user_id, limit))
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1][:25] + ("..." if len(r[1]) > 25 else ""), "time": r[2]} for r in rows]

def delete_chat(chat_id, user_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM chats WHERE id = ? AND user_id = ?", (chat_id, user_id))
    conn.commit()
    conn.close()

def clear_all_history(user_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM chats WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()