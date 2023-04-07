import socket
import threading
import os
from database import create_connection

clear = lambda: os.system('clear')

#localhost / add functionality to define host/port connection --> ergo web server between different machines. 
host = '127.0.0.1'
port = 55556

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Usernames
clients = []
usernames = []

# Read the current session ID from the file
with open('session_id.txt', 'r') as f:
    session_id = int(f.read().strip())

# receive message from client, then broadcast to other clients; run this function in each thread per client. 
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('DELETE'):
                accountDeleted = msg.decode('ascii')[5:]
                print(accountDeleted)
            else:
                broadcast(message)

        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode('ascii'))
            usernames.remove(username)
            break


def broadcast(message):
    for client in clients:
        client.send(message)

def sql_message(client, msg):
    msg = client.recv(1024)
    index = clients.index(client)
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO messages (sender, message, session_id)
                VALUES (?, ?, ?)''', (usernames[index], msg.decode('ascii'), session_id))
    conn.commit()
    conn.close()

# DELETE: Allows an existing, logged-in user to delete their account
    ## Requires user to confirm before proceeding
    ## If user does not type 'Y' or 'N', they will keep being prompted for input
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



def rmUserInfo(username):
    with open('userInfo.txt', 'r') as input:
        with open('temp.txt', 'w') as output:
            for user in input:
                if username not in user.strip(""):
                    output.write(user)
    
    os.replace('temp.txt', 'userInfo.txt')

def receive():
    while True:
        # accept server side connection
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
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

        msg = client.recv(1024)
        sql_message(client, msg)

# Increment the session ID and write it back to the file
session_id += 1
with open('session_id.txt', 'w') as f:
    f.write(str(session_id))

print("Server is listening for new connections...")
print("Session ID is " + str(session_id))
receive()