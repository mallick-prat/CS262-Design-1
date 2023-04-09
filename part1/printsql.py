import sqlite3 as lite

conn = lite.connect('messages.db')
cur = conn.cursor()

def print_messages():
    cur.execute("SELECT * FROM messages")
    print(cur.fetchall())

print_messages()