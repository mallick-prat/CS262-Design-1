import socket
import threading
#localhost / add functionality to define host/port connection --> ergo web server between different machines. 
host = '127.0.0.1'
port = 55556

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
usernames = []

# receive message from client, then broadcast to other clients; run this function in each thread per client. 
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
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


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Username is {}".format(username))
        broadcast("{} joined!".format(username).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening for new connections...")
receive()