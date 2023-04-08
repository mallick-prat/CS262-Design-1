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

# Global variables for connections and server status
server = None 
connected_to_main = True 

def serverConnect(ip, port):
    global server 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        server.connect((ip, port))
        print(f"Connected to server {ip}: {port}")
        return server
    except socket.error as e: 
        print(f"Error connecting to the server")
        return None 

# global way to receive messages 
def receive_message():
    global server
    try:
        message = server.recv(1024).decode()
        return message
    except socket.error as e:
        print(f"Error receiving message: {e}")
        return None

# global way to send messages - 
def sendMessage(message):
    global server 
    try:
        server.sendall(message.encode())
    except socket.error as e:
        print(f"Error sending message: {e}")
        return

# Heart beat monitoring
def heartbeat(main_ip, main_port, backup_ip, backup_port):
    global connected_to_main, server
    while True:
        time.sleep(10)
        sendMessage("heartbeat")
        response = receive_message()
        if response != "heartbeat_ack":
            if connected_to_main:
                print("Main server is down, switching to backup server...")
                server.close()
                if serverConnect(backup_ip, backup_port):
                    connected_to_main = False
            else:
                print("Backup server is down, switching to main server...")
                server.close()
                if serverConnect(main_ip, main_port):
                    connected_to_main = True

def Main():
    
    # Connect IP & Port
    #ip = "127.0.0.1"
    #port = 50051

    server1IP ="127.0.0.1"
    server1Port= 50051

    server2IP ="127.0.0.1"
    server2Port= 50052

    if not serverConnect(server1IP, server1Port):
        print("Main server not connecting. Switching to backup server")
        connected_to_main = False 
        if not serverConnect(server2IP, server2Port):
            print("All servers are not connecting")
            return 
    
    connection_monitor = threading.Thread(target=heartbeat, args=(server1IP, server1Port, server2IP, server2Port))
    connection_monitor.daemon = True
    connection_monitor.start()   

    # TCP socket connection
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

        # Initialize read sockets to process inputs from the server.
        read_sockets, _, _ = select.select(
            sockets_list, [], [])

        for socks in read_sockets:

            # Display messages received from the server.
            if socks == server:
                msg = socks.recv(4096)
                print(msg.decode('UTF-8'))

            # Send requests to the server from the client.
            else:
                msg = sys.stdin.readline().strip()
                server.send(msg.encode('UTF-8'))
                data = server.recv(4096)
                print(str(data.decode('UTF-8')))

if __name__ == '__main__':
    Main()