import socket
import os
clear = lambda: os.system('cls')


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 8000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    if message.lower().strip() == '/delete account':
        Delete()

    while message.lower().strip() != 'bye' & message.lower.strip() != '/delete account':
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
    while True:
        confirm = input("Are you sure you want to delete? Type (Y) for yes and (N) for no: ").lower()
        if confirm == 'y':
            rmUserInfo()
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


if __name__ == '__main__':
    client_program()