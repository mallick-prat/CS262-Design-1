# CS262-Design-1

Current dependencies:
 - getpass
 - stdiomask
 - hashlib
 - protobuf I think?
 - betterproto[compiler]
 - grpcio-tools
 - @grpc/proto-loader
 - unittest

 - brew
 - pip
 - newest version of Python

 WELCOME TO OUR CS262 PROJECT, MESSAGEBASE!

 MessageBase is an interactive socket-style networking project that allows for simple chat functionality between a client and server.

 Upon launching MessageBase, the client will be presented with several options. They can either register for an account, log into an
 existing one, delete their account once logged in, or explore existing users. To ensure privacy, passwords are hash-encrypted.

 Once a user has logged in client-side, they may engage in a one-for-one texting conversation with the server. Upon receiving the " -> "
 prompt, the appropriate user (trades off between client and server) may type their text message to the other user. The message will display
 on the other user's screen, and the other user will be prompted to reply.

 LOGIN.PY
 Contains the pathways for registering, logging in, deleting an account, etc. Also contains the client-side networking code.

 SERVER.PY
 Contains the code used for establishing a connection to the client.

 USERINFO.TXT
 Stores user information-- username and hashed password.

 /COMPUTERSTUFF
 Files we needed downloads-wise to make sure our code would work.