import unittest
import socket
from unittest.mock import MagicMock, patch
from message_base_server import get_new_leader, connect_to_server


class TestMessageBaseServer(unittest.TestCase):

    def test_get_new_leader(self):
        servers = [("127.0.0.1", 50051), ("127.0.0.1", 50052), ("127.0.0.1", 50053)]

        with patch('message_base_server.random.randint', return_value=1) as randint_mock:
            leader_index = get_new_leader(servers)
            randint_mock.assert_called_with(0, len(servers) - 1)
            self.assertEqual(leader_index, 1)

    @patch('socket.socket')
    def test_connect_to_server_success(self, socket_mock):
        ip, port = "127.0.0.1", 50051
        socket_instance = MagicMock()
        socket_mock.return_value = socket_instance

        server = connect_to_server(ip, port)

        socket_instance.setsockopt.assert_called_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_instance.connect.assert_called_with((ip, port))
        self.assertEqual(server, socket_instance)

    @patch('socket.socket')
    def test_connect_to_server_failure(self, socket_mock):
        ip, port = "127.0.0.1", 50051
        socket_instance = MagicMock()
        socket_mock.return_value = socket_instance
        socket_instance.connect.side_effect = ConnectionRefusedError

        with self.assertRaises(ConnectionRefusedError):
            connect_to_server(ip, port)

        socket_instance.setsockopt.assert_called_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_instance.connect.assert_called_with((ip, port))


if __name__ == '__main__':
    unittest.main()