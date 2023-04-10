import sqlite3

conn = sqlite3.connect('messages3.db')
c = conn.cursor()

# Delete all rows from the messages table if the table exists
while True:
    try:
        c.execute('DELETE FROM messages')
    except:
        print("No table called 'messages' exists")
        break

while True:
    try:
        c.execute('DELETE FROM accounts')
    except:
        print("No table called 'accounts' exists")
        break

conn.commit()
conn.close()