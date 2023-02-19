from getpass import getpass
import hashlib
from http import client
import os
import socket
clear = lambda: os.system('clear')


session_username = ""

# MAIN: This is kind of like the CLI landing page for the application.
    ## From here, the user has two main functionalities: Register and Log In.
    ## If the user types '1', they will be prompted to register for a new account.
    ## If the user types '2', they will be prompted to log into an existing account.
    ## If the user types '3', they will actually also go to the login page.
    ## But, they will first see a message that shows how to delete an account.
    ## For security purposes, one can only delete an account once they are logged in.
    ## If the user types '4', they will generate a list of all current account usernames.
    ## If the user types '5', they can search for a specific user by typing in the first letter of the user's username.
def main():

    # Rendering initial visuals; presenting users with login options
    clear()

    print("MessageBase -- CS 262\n")
    print("---------")
    print()

    print("1 - Register")
    print("2 - Login")
    print("3 - Delete")
    print("4 - Display User List")
    print("5 - Search for User(s)")
    print()

    # Logic to direct users to the correct functionality based on the option they choose
    while True:
        userChoice = input("Choose An Option: ")
        if userChoice in ['1', '2', '3', '4', '5']:
            break

    if userChoice == '1': # new user wants to register
        Register()

    elif userChoice == '2': # existing user wants to login
        Login()

    elif userChoice == '3': # existing user wants to delete their account
        print("First log in, then type '/delete account' to delete your account.")
        Login()
    
    elif userChoice == '4': # user wants to print out all usernames
        lines_printed = 0

        with open('userInfo.txt', 'r') as file: # reads user info
            for line in file:
                line_str = line.split()
                print(line_str[0]) # prints only the username shown on each line
                lines_printed += 1

                # If no usernames were printed, display this message (so the user knows that the search still happened)
                if lines_printed == 0:
                    print("No usernames currently in database.")
        
        # Help redirect user since they are probably done with this functionality after receiving the list
        while True:
            returnChoice = input("Return to main menu? (Y) or (N)").lower()
            
            if returnChoice == 'y':
                main()
                break
            
            elif returnChoice == 'n':
                break

    elif userChoice == '5': # user wants to search through users
        print("Alphabetical lookup:")
        
        while True:
            alpha_range = input("Enter the first letter of the username you're looking for: ").upper()
            
            # We just included a fun little easter egg in case the people grading us happen to find it in the code review :)
            if alpha_range == "EASTEREGG":
                print("Congratulations! YOU FOUND THE EASTER EGG!")
                print("ʕ•́ᴥ•̀ʔっ♡")
                break
            
            if alpha_range.isalpha(): # ensures that the user input is actually a letter
                break

        lines_printed = 0
        with open('userInfo.txt', 'r') as file: # reads user info
            for line in file:
                line_str = line.split()

                if line_str[0][0] == alpha_range: # if the first letter of the username is the desired letter...
                    print(line_str[0]) # then print the username
                    lines_printed += 1

            # If no usernames were printed, display this message (so the user knows that the search still happened)
            if lines_printed == 0 and alpha_range != 'EASTEREGG':
                print("No usernames starting with " + alpha_range)




# REGISTER: Allows a new user to create a username and password to be entered into our database.
    ## Username and password can be used upon subsequent visits to login
    ## User cannot provide a blank or existing username
    ## User must enter and re-enter the same password
    ## If username-password combination are already in use, user is prompted to login from an existing account
def Register():

    # Render initial graphics
    clear()
    print("REGISTER")
    print("--------")
    print()

    while True: # username prompt
        userName = input("Enter Username: ").title()
        if userName != '':
            break

    userName = sanitizeName(userName) # saves username as a string

    if userAlreadyExist(userName): # checks if existing user
        displayExistenceMessage()

    else: # this is a new user with a valid username

        while True: # password prompt
            userPassword = getpass("Enter Password: ")
            if userPassword != '':
                break

        while True: # password confirm

            confirmPassword = getpass("Confirm Password: ")
            if confirmPassword == userPassword:
                break

            else: # keeps looping until user enters correct password match
                print("Passwords Do Not Match")
                print()

        # Records new user info into database; prints success message
        addUserInfo([userName, hash_password(userPassword)])

        print()
        print("Registered! (:)>")
        print("If you would like to delete your account, please type '/delete account' at any time.")
        client_program() # directs logged-in user to the chat functionality



# LOGIN: Allows an existing user to log into an account that has already been made and entered into our database.
    ## User must enter valid username and password
    ## After 10 failed login attempts, user will be encouraged to register for a new account
def Login():

    # Render initial graphics
    clear()
    print("LOGIN")
    print("-----")
    print()

    usersInfo = {} # initializes an empty dictionary for which to store the verified login information

    with open('userInfo.txt', 'r') as file: # fills the dictionary using the format 'username: password' with one entry per user
        for line in file:
            line = line.split()
            usersInfo.update({line[0]: line[1]})

    while True:

        loginAttempts = 0

        userName = input("Enter Your Name: ").title() # collects and sanitizes unverified username
        userName = sanitizeName(userName)

        if userName not in usersInfo: # checks to see if username is in database
            loginAttempts += 1
            print("Not a registered username. Please try again, silly.")
            print()

            if loginAttempts >= 10: # if user has tried too many times, they likely don't have an account
                spamLogins() # help redirect the user

        else: # catches username edge cases
            break

    while True: # user has entered valid username; must now confirm account's password

        loginAttempts = 0

        userPassword = getpass("Enter Your Password: ")

        if not check_password_hash(userPassword, usersInfo[userName]): # checks if correct password
            loginAttempts += 1
            print("Incorrect Password. Try again, silly.")
            print()

            if loginAttempts >= 10: # if user has tried too many times, they likely don't have an account
                spamLogins()

        else: # user has entered correct password
            break

    # User has successfully logged in; print success message    
    session_username = userName
    print()
    print("Logged In! (:)>")
    print("If you would like to delete your account, please type '/delete account' at any time.")
    client_program() # directs logged-in user to the chat functionality



# ADDUSERINFO: Appends the user's information to the txt file with all logins and password hashes
    ## Sample format for a line in userInfo.txt: usernamehere PaSsWoRdHaShHeRe
    ## Formula for a line in userInfo.txt: [username] + [space] + [password hash] + [newline]
def addUserInfo(userInfo: list):
    with open('userInfo.txt', 'a') as file:
        for info in userInfo:
            file.write(info)
            file.write(' ') # adds a space between username and password hash
        file.write('\n')



# USERALREADYEXIST: Given a username, checks if an account exists under a specific username and password
    ## If a username has not been used yet, the function will return false

## QUESTION: I DON'T UNDERSTAND WHY WE NEED THE 'NONE' AT THE BEGINNING
def userAlreadyExist(userName, userPassword=None):
    
    if userPassword == None:

        # Returns true if the current username is in the list and false if not
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()

                if line[0] == userName:
                    return True

        return False

    # QUESTION: How do we even get to the else statement if we're initializing userPassword as none?
    else:
        userPassword = hash_password(userPassword) # hashes the password for enhanced security
        usersInfo = {} # initializes an empty dictionary for which to store the user info

        # Fills in our empty dictionary with the user's info
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName and line[1] == userPassword:
                    usersInfo.update({line[0]: line[1]})
        
        # usersInfo will remain blank if the user's information was not found in the .txt document
        if usersInfo == {}:
            return False # therefore, we know that the user does not yet exist

        # A user with a valid username can only be in the system if this boolean is TRUE    
        return usersInfo[userName] == userPassword



# DISPLAYEXISTENCEMESSAGE: For use if the user is trying to register but already has an account.
    ## Presents the user with more helpful options since they were falsely trying to register.
    ## If the user presses T, they will be able to register as a new user.
    ## If the user presses L, they will be able to log into their existing account.
def displayExistenceMessage():
    while True:
        # Setting up the graphics
        print()
        error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()

        if error == 't':
            Register()
            break

        elif error == 'l':
            Login()
            break

        else: # the user has provided undesired input (they are probably confused and should be redirected)
            print("Redirecting you to the main menu.")
            main()
            break



# SANITIZENAME: Reformats the username to our standard for more standardized recording in the .txt document.
    ## Example: The string 'mallick prat' would become 'mallick-prat'
def sanitizeName(userName):
    userName = userName.split() # 'mallick prat' --> ['mallick', 'prat']
    userName = '-'.join(userName) # ['mallick', 'prat'] --> 'mallick-prat'
    return userName



# SPAMLOGINS: Used when the user has tried logging in, either by entering an incorrect username or an incorrect password 10+ times.
    ## Since the user is repeatedly trying a path that is not helpful to them, they will be redirected.
    ## The user is prompted to create a new account since they likely don't have one.
    ## If the user selects 'N,' they will be redirected to the main menu.
def spamLogins():

    clear()
    print("You have attempted too many times. Would you like to create an account?")
    
    while True: # makes sure user has given correct input
        newAcct = input("Type (Y) for yes and (N) for no.").lower()
        if newAcct in ['y', 'n']:
            break

    if newAcct == 'y': # encourage user to register for an account
        Register()

    else: # take them back to the beginning
        print("Redirecting back to main options.")
        main()



# HASH_PASSWORD: Uses SHA256 encryption to hash the password for enhanced security
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()



# CHECK_PASSWORD_HASH: Given a password and its hash, return a boolean for if the password is correct.
    ## With hash encryption, only the correct password will produce the unique hash.
    ## So, a false password will make the return statement false and vice versa.
def check_password_hash(password, hash):
    return hash_password(password) == hash



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



# To start, display the 'main menu' in the CLI for the user.
main()