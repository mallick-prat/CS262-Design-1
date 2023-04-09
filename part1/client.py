import socket
import threading 
import os 
from getpass import getpass
from getpass import getuser 
import hashlib
import time
import socket
import sys
import select
from termcolor import colored

def connect_to_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect((ip, port))
    return server

def Main():
    
    # Connect IP & Port for both servers
    servers = [("127.0.0.1", 50051), ("127.0.0.1", 50052)]

    # Attempt to connect to the first server
    current_server_index = 0
    try:
        server = connect_to_server(servers[current_server_index][0], servers[current_server_index][1])
    except ConnectionRefusedError:
        print("Server 1 is down. Switching to Server 2.")
        current_server_index = 1
        server = connect_to_server(servers[current_server_index][0], servers[current_server_index][1])

    # Intro message

    msg = "\nMessageBase -- CS 262\n"
    msg += "\n ---------"
    msg += "\n1|<USERNAME>|<PASSWORD> - Register"
    msg += "\n2|<USERNAME>|<PASSWORD> - Login"
    msg += "\n3|<USERNAME> - Delete"
    msg += "\n4 - Display User List"
    
    msg += "\n5|<USERNAME> - Search for User(s)"
    msg += "\nd|<TO>|<MESSAGE> - Send Private Message"
    msg += "\nh - HELP | Display all options"
    msg = colored(msg, 'blue')
    print(msg)

    # Rendering initial visuals; presenting users with login options
    loggedIn = False 

    # Main loop for clients to receive and send messages to the server.
    while True:

        # List of input streams.
        sockets_list = [sys.stdin, server]

        try:
            # Initialize read sockets to process inputs from the server.
            read_sockets, _, _ = select.select(sockets_list, [], [])

            for socks in read_sockets:

                # Display messages received from the server.
                if socks == server:
                    msg = socks.recv(4096)
                    if not msg:
                        raise ConnectionError("Server connection lost.")
                    print(msg.decode('UTF-8'))

                # Send requests to the server from the client.
                else:
                    msg = sys.stdin.readline().strip()
                    server.send(msg.encode('UTF-8'))
                    data = server.recv(4096)
                    print(str(data.decode('UTF-8')))

        except (ConnectionError, socket.error):
            print("Server connection closed. Switching to the other server.")
            server.close()
            current_server_index = (current_server_index + 1) % 2
            server = connect_to_server(servers[current_server_index][0], servers[current_server_index][1])

if __name__ == '__main__':
    Main()