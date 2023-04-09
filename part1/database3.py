import sqlite3

def create_connection3():
    conn = sqlite3.connect('messages3.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sender TEXT NOT NULL,
                  recipient TEXT NOT NULL,
                  message TEXT NOT NULL,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  session_id INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS accounts
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL)''')

    conn.commit()
    return conn