import sqlite3

def create_connection1():
    conn = sqlite3.connect('messages1.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sender TEXT NOT NULL,
                  recipient TEXT NOT NULL,
                  message TEXT NOT NULL,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  session_id INTEGER)''')
    conn.commit()
    return conn
