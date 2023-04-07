import socket
import threading 
import os
from getpass import getpass
from getpass import getuser 
import hashlib
from time import sleep
from database import create_connection

clear = lambda: os.system('clear')

##############################################################################################################

# MAIN: This is kind of like the CLI landing page for the application.
    ## From here, the user has two main functionalities: Register and Log In.
    ## If the user types '1', they will be prompted to register for a new account.
    ## If the user types '2', they will be prompted to log into an existing account.
    ## If the user types '3', they will actually also go to the login page.
    ## But, they will first see a message that shows how to delete an account.
    ## For security purposes, one can only delete an account once they are logged in.
    ## If the user types '4', they can display the entire user list.
    ## If the user types '5', they can search for a specific user.
    ## If the user types '6', they can retrieve all messages from the current session.
    ## If the user types '7', they can replay what the chat has looked like so far in the session.
def main():

    # Rendering initial visuals; presenting users with login options
    clear()
    loggedIn = False 

    print("MessageBase -- CS 262\n")
    print("---------")
    print()

    print("1 - Register")
    print("2 - Login")
    print("3 - Delete")
    print("4 - Display User List")
    print("5 - Search for User(s)")
    print("6 - Re-Generate Chat")
    print("7 - Replay Chat")
    print()

    # Logic to direct users to the correct functionality based on the option they choose
    while True:
        userChoice = input("Choose An Option: ")
        if userChoice in ['1', '2', '3', '4', '5', '6', '7']:
            break

    if userChoice == '1': # new user wants to register ------------------------------------------------------
        Register()

    elif userChoice == '2': # existing user wants to login --------------------------------------------------
        Login()

    elif userChoice == '3': # existing user wants to delete their account -----------------------------------
        print("First log in, then type '/delete account' to delete your account.")
    
    elif userChoice == '4': # user wants to print out all usernames
        lines_printed = 0

        # We are storing usernames and passwords in userInfo.txt, so we need to read and print from here
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line_str = line.split()
                print(line_str[0])
                lines_printed += 1
                if lines_printed == 0:
                    print("No usernames currently in database.")
        
        # Redirects user to main menu or ends program after printing the list
        while True:
            returnChoice = input("Return to main menu? (Y) or (N)").lower()
            if returnChoice == 'y':
                main()
                break
            elif returnChoice == 'n':
                break

    elif userChoice == '5': # user wants to search through users ------------------------------------------
        print("Alphabetical lookup:")
        
        while True:
            alpha_range = input("Enter the first letter of the username you're looking for: ").upper()
            
            # We just added a simple easter egg for fun :)
            if alpha_range == "EASTEREGG":
                print("Congratulations! YOU FOUND THE EASTER EGG!")
                print("ʕ•́ᴥ•̀ʔっ♡")
                break
            
            if alpha_range.isalpha():
                break

        lines_printed = 0

        # We are storing usernames and passwords in userInfo.txt, so we need to read and print from here
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line_str = line.split()
                if line_str[0][0] == alpha_range:
                    print(line_str[0])
                    lines_printed += 1
                
            if lines_printed == 0 and alpha_range != 'EASTEREGG':
                print("No usernames starting with " + alpha_range)

    elif userChoice == '6': # Print messages for a specific session_id --------------------------------------
        
        # We are storing the current session ID as a string in a txt file called session_id, so we need to retrieve it
        with open('session_id.txt', 'r') as f:
            session_id = f.read().strip()

        lines_printed = 0

        # We are establishing a connection to our database so that we can perform a SQL query
        conn = create_connection()
        c = conn.cursor()

        # Retrieves the SQL information from the table; prints the information in a formatted manner
        c.execute("SELECT sender, message, timestamp FROM messages WHERE session_id=?", (session_id,))
        results = c.fetchall()

        for row in results:
            print(row[0] + ": '" + row[1] + "'; sent at " + row[2])
            lines_printed += 1
        
        # If we pass through all of that logic with nothing to print, we know that no messages have yet been sent in the current session
        if lines_printed == 0:
            print("No messages have been sent within this session yet.")

        # Now that we have re-generated the chat, we either redirect to the main menu or exit the program
        while True:
            print("It is possible that new messages have been sent since you last checked.")
            print("Therefore, we recommend that you choose Option 6 once more if you want to be safe.")
            returnChoice = input("Return to main menu? (Y) or (N)").lower()
            
            if returnChoice == 'y':
                main()
                break
            elif returnChoice == 'n':
                break

    elif userChoice == '7': # 'Replay' messages for a specific session_id with waits ------------------------
        # We are storing the current session ID as a string in a txt file called session_id, so we need to retrieve it
        with open('session_id.txt', 'r') as f:
            session_id = f.read().strip()

        lines_printed = 0

        # We are establishing a connection to our database so that we can perform a SQL query
        conn = create_connection()
        c = conn.cursor()

        # Retrieves the SQL information from the table; prints the information in a formatted manner
        c.execute("SELECT sender, message FROM messages WHERE session_id=?", (session_id,))
        results = c.fetchall()

        for row in results:
            print(row[0] + ": '" + row[1] + "'")
            lines_printed += 1

            # We call sleep() so that it looks more like 'watching the chat back'
            sleep(1)

        # If we pass through all of that logic with nothing to print, we know that no messages have yet been sent in the current session
        if lines_printed == 0:
            print("No messages have been sent within this session yet.")

        # Now that we have re-generated the chat, we either redirect to the main menu or exit the program
        while True:
            print("It is possible that new messages have been sent since you last checked.")
            print("Therefore, we recommend that you choose Option 6 once more if you want to be safe.")
            
            if returnChoice == 'y':
                main()
                break
            elif returnChoice == 'n':
                break

##############################################################################################################

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
            userPassword = getpass("Enter (Unprivate) Password: ")
            if userPassword != '':
                # print("Please enter a username.")
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
        input("Press enter to continue:")
        main()
        ####### return to main menu

##############################################################################################################

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
    authuser = [] # empty dictionary to store auth users

    with open('userInfo.txt', 'r') as file: # fills the dictionary using the format 'username: password' with one entry per user
        for line in file:
            line = line.split()
            usersInfo.update({line[0]: line[1]})

    with open('authuser.txt') as f:
        lines = f.readlines()

    # Loop through the lines and add them to the list
    for line in lines:
        line = line.strip()
        authuser.append(line)

    while True:

        loginAttempts = 0

        userName = input("Enter Your User Name: ").title() # collects and sanitizes unverified username
        userName = sanitizeName(userName)
        
        for authuser in authuser: # checks to see if the user is already logged in
            if authuser == userName:
                print("You are already logged in.")
                input("You will now be redirected to the main menu. Press enter to continue:").lower()
                main()

        if userName not in usersInfo: # checks to see if username is in database
            loginAttempts += 1
            print("Not a registered username. Please try again, silly.")
            input('Press enter to continue.')
            main()

            if loginAttempts >= 10: # if user has tried too many times, they likely don't have an account
                spamLogins()

        else: # catches username edge cases
            break

    while True: # user has entered valid username; must now confirm account's password

        loginAttempts = 0

        userPassword = getpass("Enter Your Password: ")

        if not check_password_hash(userPassword, usersInfo[userName]):
            loginAttempts += 1
            print("Incorrect Password. Try again, silly.")
            print()

            if loginAttempts >= 10: # if user has tried too many times, they likely don't have an account
                spamLogins()

        else: # user has entered correct password
            addNewAuth(userName)
            break 

    # User has successfully logged in; print success message    
    session_username = userName
    print()
    print("Logged In! (:)>")
    print("If you would like to delete your account, please type '/delete account' at any time.")
    print("Your username is:", session_username)

    # Dictionary for the options of hosts and ports to connect to
    connection_dict = {
        '127.0.0.1': 55556,
        '127.0.0.1': 5000
    }

    # Establish a socket connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_iter = iter(connection_dict.items())
    
    while True:
        try:
            conn, port = next(conn_iter)
            client.connect((conn, port))
            break
        
        except StopIteration:
            print("Could not connect to any server.")
            break
        
        except Exception as e:
            print(f"Error connecting to {conn}:{port}: {str(e)}")


    # Allows the client to receive messages
    def receive():
        while True:
            try:
                # Receive Message From Server
                # If 'USER' Send Username
                message = client.recv(1024).decode('ascii')
                if message == 'USER':
                    client.send(session_username.encode('ascii'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                client.close()
                break 

    # Allows the client to send messages
    def write():
        while True:

            # The message format will be [username]: [message]
            message = '{}: {}'.format(session_username, input(''))

            # Listen for if they're asking to delete their account
            if message[len(session_username)+2:].startswith('/delete'):
                client.send(f'DELETE {session_username}'.encode('ascii'))
                Delete(session_username)
            
            # Listen for if they're asking to log out of their account
            if message[len(session_username)+2:].startswith('/logout'):
                rmAuthUser(session_username)
                main()

            # If they are just typing a normal message, then send it
            else: 
                client.send(message.encode('ascii'))

    # Run client and write threads 
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

##############################################################################################################

# ADDUSERINFO: Appends the user's information to the txt file with all logins and passwords
def addUserInfo(userInfo: list):
    with open('userInfo.txt', 'a') as file:
        for info in userInfo:
            file.write(info)
            file.write(' ')
        file.write('\n')

##############################################################################################################

# ADDNEWAUTH: Add's a logged-in user to authuser.txt to denote that they have an active session
def addNewAuth(newauth: list):
     with open('authuser.txt', 'a') as file:
        for info in newauth:
            file.write(info)
        file.write('\n')

##############################################################################################################

# USERALREADYEXIST: Given a username, checks if an account exists under a specific username and password
    ## If a username has not been used yet, the function will return false
def userAlreadyExist(userName, userPassword=None):
    
    if userPassword == None:
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()

                if line[0] == userName:
                    return True

        return False

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

        return usersInfo[userName] == userPassword

##############################################################################################################

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

##############################################################################################################

# SANITIZENAME: Reformats the username to our standard for more standardized recording in the .txt document.
    ## Example: The string 'mallick prat' would become 'mallick-prat'
def sanitizeName(userName):
    userName = userName.split() # 'mallick prat' --> ['mallick', 'prat']
    userName = '-'.join(userName) # ['mallick', 'prat'] --> 'mallick-prat'
    return userName

##############################################################################################################

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

##############################################################################################################

# HASH_PASSWORD: Uses SHA256 encryption to hash the password for enhanced security
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

##############################################################################################################

# CHECK_PASSWORD_HASH: Given a password and its hash, return a boolean for if the password is correct.
    ## With hash encryption, only the correct password will produce the unique hash.
    ## So, a false password will make the return statement false and vice versa.
def check_password_hash(password, hash):
    return hash_password(password) == hash

##############################################################################################################

# DELETE: Allows an existing, logged-in user to delete their account
    ## Requires user to confirm before proceeding
    ## If user does not type 'Y' or 'N', they will keep being prompted for input
def Delete(session_username):
    clear()

    # Rendering the CLI graphics
    print("DELETE ACCOUNT")
    print("--------")
    print()

    while True: # Confirm delete; delete if 'y'
        confirm = input("Are you sure you want to delete? Type (Y) for yes and (N) for no: ").lower()
        if confirm == 'y':
            rmUserInfo(session_username)
            rmAuthUser(session_username)
            main()
            break
        elif confirm != 'n':
            print("Please enter a valid input.")

##############################################################################################################

# RMUSERINFO: Deletes the user's info from userInfo.txt by writing the new user info to temp.txt and replacing the file
def rmUserInfo(username):
    with open('userInfo.txt', 'r') as input:
        with open('temp.txt', 'w') as output:
            for user in input:
                if username not in user.strip(""):
                    output.write(user)
    
    os.replace('temp.txt', 'userInfo.txt')

##############################################################################################################

# RMAUTHUSER: Same thing as rmUserInfo, except with the auth information to denote that this deleted/inactive account cannot have an active session
def rmAuthUser(session_username):
    with open('authuser.txt', 'r') as input:
        with open('temp1.txt', 'w') as output:
            for user in input:
                if session_username not in user.strip(""):
                    output.write(user)
    os.replace('temp1.txt', 'authuser.txt')

##############################################################################################################

if __name__ == "__main__":
    main()