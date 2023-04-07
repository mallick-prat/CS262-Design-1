import socket
import threading
import os
from database import create_connection

clear = lambda: os.system('clear')

# Define host and port for the server to listen on
host = '127.0.0.1'
port = 5000

# Create the server socket, bind it to the host and port, and listen for connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists to store clients and their usernames
clients = []
usernames = []
current_msg = []

# Read the current session ID from the file
with open('session_id.txt', 'r') as f:
    session_id = int(f.read().strip())

# Function to handle incoming messages from clients and broadcast them to other clients
def handle(client):
    while True:
        try:
            # Receive the message from the client
            new_message = False
            msg = message = client.recv(1024)
            
            # Decode the message and extract the text
            full_msg_text = msg.decode('ascii')
            msg_text = full_msg_text.split(": ")[1]
            
            # Add the message to the current message list and print its length
            current_msg.append(msg_text)

            # Flag that a new message has been received and insert it into the database
            new_message = True
            if new_message:
                sql_message(client, current_msg[-1])
                new_message = False
            
            # If the message starts with "DELETE", delete the corresponding user account
            if msg.decode('ascii').startswith('DELETE'):
                accountDeleted = msg.decode('ascii')[5:]
                print(accountDeleted)
            else:
                # Otherwise, broadcast the message to all clients
                broadcast(message)

        except:
            # Remove and close the client's connection if an error occurs
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'))
            usernames.remove(username)
            break

# Function to broadcast a message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to insert a message into the database
def sql_message(client, msg):
    index = clients.index(client)
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO messages (sender, message, session_id)
                VALUES (?, ?, ?)''', (usernames[index], msg, session_id))
    conn.commit()
    conn.close()

# Function to delete a user account
def Delete(input):
    clear()
    print("DELETE ACCOUNT")
    print("--------")
    print()
    while True:
        confirm = input("Are you sure you want to delete? Type (Y) for yes and (N) for no: ").lower()
        if confirm == 'y':
            rmUserInfo(input)
            break
        elif confirm != 'n':
            print("Please enter a valid input.")

# Function to remove a user's information from the user info file
def rmUserInfo(username):
    with open('userInfo.txt', 'r') as input:
        with open('temp.txt', 'w') as output:
            for user in input:
                if username not in user.strip(""):
                    output.write(user)
    
    os.replace('temp.txt', 'userInfo.txt')

# Function to receive incoming connections from clients
def receive():
    while True:
        # Accept incoming connection from a client
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Username
        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Print And Broadcast Username
        print("Username is {}".format(username))
        broadcast("{} joined!".format(username).encode('ascii'))
        #broadcast()
        client.send('Connected to server!'.encode('ascii'))

        #if len(current_msg) > 0:
            #sql_message(client, current_msg[-1])

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        #msg = client.recv(1024).decode('ascii')
        print("Bottom: the length of current_msg is " + str(len(current_msg)))
        # if len(current_msg) > 0:
            # sql_message(client, current_msg[-1])

# Increment the session ID and write it back to the file
session_id += 1
with open('session_id.txt', 'w') as f:
    f.write(str(session_id))

print("Server is listening for new connections...")
print("Session ID is " + str(session_id))
receive()