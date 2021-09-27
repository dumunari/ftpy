import unittest
from unittest.mock import patch, call
from src.servers.custom_server import CustomServer


class TestCustomServer(unittest.TestCase):

    @patch('src.servers.custom_server.FTPServer')
    @patch('src.servers.custom_server.Args')
    def test_retrieve_server_max_cons_not_none_and_max_cons_per_ip_none(self, args_mock, ftp_server_mock):
        # arrange
        handler = 'Fake handler'
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 8, 'failure_rate': 5,
                                                             'max_conns': 5, 'max_conns_ip': None, 'port': 2121}
        # act
        server = CustomServer().retrieve_server(handler)

        # assert
        self.assertEqual(ftp_server_mock.mock_calls, [call(('', 2121), 'Fake handler')])
        self.assertEqual(server.max_cons, 5)
        self.assertEqual(server.max_cons_per_ip.mock_calls, [])

    @patch('src.servers.custom_server.FTPServer')
    @patch('src.servers.custom_server.Args')
    def test_retrieve_server_max_cons_none_and_max_cons_per_ip_not_none(self, args_mock, ftp_server_mock):
        # arrange
        handler = 'Fake handler'
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 8, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': 230, 'port': 2121}

        # act
        server = CustomServer().retrieve_server(handler)

        # assert
        self.assertEqual(ftp_server_mock.mock_calls, [call(('', 2121), 'Fake handler')])
        self.assertEqual(server.max_cons_per_ip, 230)
        self.assertEqual(server.max_cons.mock_calls, [])

    @patch('src.servers.custom_server.FTPServer')
    @patch('src.servers.custom_server.Args')
    def test_retrieve_server_max_cons_and_max_cons_per_ip_not_none(self, args_mock, ftp_server_mock):
        # arrange
        handler = 'Fake handler'
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 8, 'failure_rate': 5,
                                                             'max_conns': 5, 'max_conns_ip': 230, 'port': 2121}

        # act
        server = CustomServer().retrieve_server(handler)

        # assert
        self.assertEqual(ftp_server_mock.mock_calls, [call(('', 2121), 'Fake handler')])
        self.assertEqual(server.max_cons, 5)
        self.assertEqual(server.max_cons_per_ip, 230)

    @patch('src.servers.custom_server.FTPServer')
    @patch('src.servers.custom_server.Args')
    def test_retrieve_server_max_cons_and_max_cons_per_ip_none(self, args_mock, ftp_server_mock):
        handler = 'Fake handler'
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 8, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        server = CustomServer().retrieve_server(handler)

        self.assertEqual(ftp_server_mock.mock_calls, [call(('', 2121), 'Fake handler')])
        self.assertEqual(server.max_cons.mock_calls, [])
        self.assertEqual(server.max_cons_per_ip.mock_calls, [])

    @patch('src.servers.custom_server.FTPServer')
    @patch('src.servers.custom_server.Args')
    def test_retrieve_server_different_port(self, args_mock, ftp_server_mock):
        handler = 'Fake handler'
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 8, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 8081}

        CustomServer().retrieve_server(handler)

        self.assertEqual(ftp_server_mock.mock_calls, [call(('', 8081), 'Fake handler')])
