import sqlite3

print("attempting to clear server 1: \n")

conn = sqlite3.connect('messages1.db')
c = conn.cursor()

# Delete all rows from the messages table if the table exists
while True:
    try:
        c.execute('DELETE FROM messages')
    except:
        print("No table called 'messages' exists")
        break

conn.commit()
conn.close()

print("moving on to server 2: \n")

conn = sqlite3.connect('messages2.db')
c = conn.cursor()

# Delete all rows from the messages table if the table exists
while True:
    try:
        c.execute('DELETE FROM messages')
    except:
        print("No table called 'messages' exists")
        break

conn.commit()
conn.close()

print("moving on to server 3: \n")

conn = sqlite3.connect('messages3.db')
c = conn.cursor()

# Delete all rows from the messages table if the table exists
while True:
    try:
        c.execute('DELETE FROM messages')
    except:
        print("No table called 'messages' exists")
        break

conn.commit()
conn.close()

print("Finished running.")