# CS262-Design-1

<h1>WELCOME TO OUR CS262 PROJECT, MESSAGEBASE!</h1>

 MessageBase is an interactive socket-style networking project that allows for simple chat functionality between a client and server.

 Upon launching MessageBase, the client will be presented with several options. They can either register for an account, log into an
 existing one, delete their account once logged in, or explore existing users. To ensure privacy, passwords are hash-encrypted.

 Once a user has logged in client-side, they may engage in a one-for-one texting conversation with the server. Upon receiving the " -> "
 prompt, the appropriate user (trades off between client and server) may type their text message to the other user. The message will display
 on the other user's screen, and the other user will be prompted to reply.

 <h2>LOGIN.PY</h2>
 Contains the pathways for registering, logging in, deleting an account, etc. Also contains the client-side networking code.

 <h2>SERVER.PY</h2>
 Contains the code used for establishing a connection to the client.

 <h2>USERINFO.TXT</h2>
 Stores user information-- username and hashed password.

 <h2>/COMPUTERSTUFF</h2>
 Files we needed downloads-wise to make sure our code would work.

 <h1>HOW TO GET STARTED:</h1>

    1. Make sure you are inside of the CS262-Design-1/part1 directory on each computer, with a terminal open on each computer.
    2. Establish a localhost connection between the two computers.
    3. Type "python3 server.py" into the 'server' computer, and "python3 client.py" into the 'client' computer (in that order).
    4. Text as you please! Use "/logout" or press Control-C on either computer to end the connection.
    5. Make sure you are inside of the CS262-Design-1/part1 directory on each computer, with a terminal open on each computer.
    6. To use gRPC, type "python3 greet_server.py" into the 'server' computer, and "python3 greet_client.py" into the 'client' computer (in that order).
    7. Have fun with the gRPC demos! Press Control-C on either computer to end the connection.

 Current dependencies:
 - getpass
 - stdiomask
 - hashlib
 - protobuf
 - betterproto[compiler]
 - grpcio-tools
 - @grpc/proto-loader
 - unittest
 - brew
 - pip
 - newest version of Python
 - Necessary packages for React
 - Axios
 - socket.io-client
 - Flask