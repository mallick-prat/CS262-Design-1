import sqlite3

conn = sqlite3.connect('messages.db')
c = conn.cursor()

# delete all rows from the messages table
c.execute('DELETE FROM messages')

conn.commit()
conn.close()