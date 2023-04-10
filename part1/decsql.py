import sqlite3

# Open a connection to the database file
conn = sqlite3.connect('messages1.db')
cursor = conn.cursor()

# Decrement the ID numbers of all rows in the table "mytable" by 1
cursor.execute("UPDATE accounts SET id = id - 1")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("ID numbers decremented successfully!")
