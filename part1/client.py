import socket
import os
clear = lambda: os.system('clear')


# CLIENTPROGRAM: Defines network connection and message-sending logic for the client side
    ## If user types 'bye', they can end the conversation.
    ## If user types '/delete account', they can erase their messaging account.
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 8000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    message_string = message.lower().strip()  # formats message properly

    # If the user wants to delete their account, they can trigger this by typing "/delete account"
    if message_string == '/delete account':
        Delete()

    while message_string != 'bye' and message_string != '/delete account':  # excludes our two edge cases
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


# DELETE: Allows an existing, logged-in user to delete their account
    ## Requires user to confirm before proceeding
    ## If user does not type 'Y' or 'N', they will keep being prompted for input
def Delete():
    clear()
    print("DELETE ACCOUNT")
    print("--------")
    print()

    # Verifies the account deletion with user before proceeding
    while True:
        confirm = input("Are you sure you want to delete? Type (Y) for yes and (N) for no: ").lower()
        
        if confirm == 'y':
            rmUserInfo()
            break
        
        elif confirm != 'n':
            print("Please enter a valid input.")


# RMUSERINFO: Helper function; performs the actual logic behind deleting a user's account username and password.
def rmUserInfo(username):

    # First reads userInfo.txt as input (this is the original set of accounts)
    with open('userInfo.txt', 'r') as input:

        # Writes a copy of the original set of accounts to a temp txt file...
        with open('temp.txt', 'w') as output:
            
            # For every account BUT the account that needs to be deleted
            for user in input:
                if username not in user.strip(""):
                    output.write(user)
    
    # Replaces the old userInfo.txt with our updated list that was saved in temp.txt
    os.replace('temp.txt', 'userInfo.txt')

if __name__ == '__main__':
    client_program()