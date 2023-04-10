import unittest
from server import hash_password, directMessage, register, login, delete, userList, search
from unittest.mock import Mock

class TestServerMethods(unittest.TestCase):

    def test_hash_password(self):
        self.assertEqual(hash_password("password123"), 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f')

    def test_directMessage(self):
        connection = Mock()
        recipient_name = "user"
        msg = "Hello, user!"
        response = directMessage(connection, recipient_name, msg)
        self.assertEqual(response, "\033[32m\nMessage will be delivered to user after the account is online.\033[0m")

    def test_register(self):
        connection = Mock()
        msg_list = ["1", "newuser", "password"]
        response = register(msg_list, connection)
        self.assertIn("\033[32m\nNew account created! User ID: newuser. Please log in.\033[0m", response)

    def test_login(self):
        connection = Mock()
        msg_list = ["2", "existinguser", "password"]
        response = login(msg_list, connection)
        self.assertIn("\033[32m\nLogin successful - welcome back existinguser!\033[0m", response)

    def test_delete(self):
        connection = Mock()
        msg_list = ["3", "existinguser"]
        response = delete(msg_list, connection)
        self.assertIn("\033[32m\nAccount existinguser has been deleted.\033[0m", response)

    def test_userList(self):
        response = userList()
        self.assertIn("No existing users!", response)

    def test_search(self):
        msg_list = ["5", "A"]
        response = search(msg_list)
        self.assertIn("\033[31m\nNo usernames starting with A\033[0m", response)

if __name__ == '__main__':
    unittest.main()