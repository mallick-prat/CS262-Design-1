

## SOOO TOOOTALLLY GARGBAGE RIGHT NOW






from atexit import register
from email.headerregistry import HeaderRegistry
import unittest
import time

import login.py

register_tests = 0
login_tests = 0
delete_tests = 0

class Register(unittest.TestCase):

    def wrong_main_option(self):
        # what happens if 1, 2, 3 not selected in main?
        start = time.time()
        argv = [login.py, 4]
        print(argv)

        while start > 10:
            register_tests += 1
            return True
    
    
    def existing_user(self):
        # prevents existing user from registering with same username
        start = time.time()
        argv = [login.py, 1, pratyushmallick]
        print(argv)

    def new_user(self):
        # successfully creates a new user
        print()

    def try_delete(self):
        # what happens if user tries to delete their account before registering?
        print()

    def blank_name(self):
        # what happens if user enters a blank name?
        print()

    def blank_pw(self):
        # what happens if user enters a blank pw?
        print()

    def no_pw_match(self):
        # use the pw hash helper function to make sure pw is hashing correctly
        print()

    def pw_hash(self):
        print()

    def add_to_txt(self):
        # check if the txt file has gained a line
        print()
    
    def name_in_txt(self):
        # register, then find username in txt file exactly once
        print()

if __name__ == '__main__':
    unittest.main()
    # Register.wrong_main_option()
    print("Register tests passed: " + register_tests)
    print("Login tests passed: " + login_tests)
    print("Delete tests passed: " + delete_tests)
    total_tests = register_tests + login_tests + delete_tests
    print("Total: " + total_tests + "out of ___ tests passed.")
    if total_tests < 100:
        print("🙏🏽Rasgullah")
    elif total_tests < 100:
        print("😌😤get on that grindset mindset")
    else:
        print("💯💶bas-ed")
