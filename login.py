from stdiomask import getpass
import hashlib
import os
clear = lambda: os.system('cls')


def main():

    # Rendering initial visuals; presenting users with login options
    clear()

    print("MessageBase - Anika Lakhani & Pratyush Mallick - CS 262\n")
    print("---------")
    print()

    print("1 - Register")
    print("2 - Login")
    print("3 - Delete")
    print()

    # Logic to direct users to the correct functionality based on the option they choose
    while True:
        userChoice = input("Choose An Option: ")
        if userChoice in ['1', '2', '3']:
            break

    if userChoice == '1': # new user wants to register
        Register()

    elif userChoice == '2': # existing user wants to login
        Login()

    elif userChoice == '3': # existing user wants to delete their account
        Delete()



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
        displayUserAlreadyExistMessage()

    else: # this is a new user with a valid username

        while True: # password prompt
            userPassword = getpass("Enter (Unprivate) Password: ")
            if userPassword != '':
                print("Please enter a username.")
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



# LOGIN: Allows an existing user to log into an account that has already been made and entered into our database.
    ## User must enter valid username and password
    ## After 10 failed login attempts, account will be automatically deleted for security purposes
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
            break

    # User has successfully logged in; print success message    
    print()
    print("Logged In! (:)>")

def Delete():
    clear()
    print("DELETE ACCOUNT")
    print("--------")
    print()
    while True:
        userName = input("Enter Username: ").title()
        if userName != '':
            break
    userName = sanitizeName(userName)
    if userAlreadyExist(userName):
        confirm = input("Are you sure you want to delete? Type (Y) for yes and (N) for no: ").lower()
        if confirm == 'y':
            rmUserInfo()
        elif confirm != 'n':
            print("Please enter a valid input.")


def addUserInfo(userInfo: list):
    with open('userInfo.txt', 'a') as file:
        for info in userInfo:
            file.write(info)
            file.write(' ')
        file.write('\n')

def rmUserInfo(username, userInfo: list):
    with open('userInfo.txt', 'r') as input:
        with open('temp.txt', 'w') as output:
            for user in input:
                if username not in user.strip(""):
                    output.write(user)
    
    os.replace('temp.txt', 'userInfo.txt')

def userAlreadyExist(userName, userPassword=None):
    if userPassword == None:
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName:
                    return True
        return False
    else:
        userPassword = hash_password(userPassword)
        usersInfo = {}
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName and line[1] == userPassword:
                    usersInfo.update({line[0]: line[1]})
        if usersInfo == {}:
            return False
        return usersInfo[userName] == userPassword

def displayUserAlreadyExistMessage():
    while True:
        print()
        error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login:\nPress (D) To Delete: ").lower()
        if error == 't':
            Register()
            break
        elif error == 'l':
            Login()
            break
        elif error == 'n':
            Delete()
            break

def sanitizeName(userName):
    userName = userName.split()
    userName = '-'.join(userName)
    return userName

def spamLogins():

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

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password_hash(password, hash):
    return hash_password(password) == hash
    
main()