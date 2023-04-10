# CS262-Design-MessageBase

Welcome to our CS262 project, MessageBase! MessageBase is an interactive socket-style networking project that allows for simple chat functionality between a client and multiple servers.

Upon launching MessageBase, the client will be presented with several options. They can either register for an account, log into an existing one, delete their account once logged in, search for users, display the user list, or send private messages. To ensure privacy, passwords are hash-encrypted.

Once a user has logged in client-side, they may engage in a one-for-one texting conversation with the server. The message will display on the other user's screen, and the other user will be prompted to reply.

## Setup

1. To install the packages listed in the requirements.txt file, open a terminal or command prompt and navigate to the project directory. 
Run the following command:
- pip install -r requirements.txt
2. Run `server{x}.py` for each server instance in separate terminals:
- python server1.py, python server2.py, etc. 
3. Run the client by executing:
- python client.py

## Files

- `client.py`: Contains the pathways for registering, logging in, deleting an account, etc. Also contains the client-side networking code.
- `server{x}.py`: Contains the code used for establishing a connection to the client and handling client requests.

## Functionality

- 1|<USERNAME>|<PASSWORD> - Register 
- 2|<USERNAME>|<PASSWORD> - Login
- 3|<USERNAME> - Delete.
- 4 - Display User List
- 5|<USERNAME> - Search for User(s)
- d|<TO>|<MESSAGE> - Send Private Message
= h - HELP | Display all options

## Additional Notes

- The client interacts with multiple servers to ensure fault tolerance.
- When one server is down, the client will initiate a leader election to select a new server to connect to.
- The client handles server disconnections and performs leader election to maintain connectivity.
- The provided code can be expanded to include additional features and improvements.
