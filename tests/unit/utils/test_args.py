import unittest
from argparse import Namespace
from unittest.mock import patch, call
from src.utils.args import Args


class TestArgs(unittest.TestCase):

    @patch('src.utils.args.argparse')
    @patch('src.utils.args.logging')
    def test_retrieve_args(self, logging_mock, argparse_mock):
        # arrange
        argparse_mock.ArgumentParser().parse_args.return_value = Namespace(max_delay=5, delay_rate=8, failure_rate=5,
                                                                           max_conns=None, max_conns_ip=None, port=2121)
        # act
        Args().retrieve_args()

        # assert
        self.assertEqual(argparse_mock.mock_calls, [call.ArgumentParser(),
                                                    call.ArgumentParser(),
                                                    call.ArgumentParser().add_argument('-md', '--max-delay', required=False, help='Max delay on STOR and RETR, in seconds. Min is always set to 1s. Will have no effect if delay-rate is 0. Defaults to 5s', type=int, default=5),
                                                    call.ArgumentParser().add_argument('-dr', '--delay-rate', required=False, help='Desired delay rate on STOR and RETR, from 0 to 10, where 1 means 10 percent. 0 means no delay. Defaults to 80 percent', type=int, default=8),
                                                    call.ArgumentParser().add_argument('-fr', '--failure-rate', required=False, help='Desired failure rate on STOR and RETR, from 1 to 10, where 1 means 10 percent. 0 means no failure rate. Defaults to 50 percent', type=int, default=5),
                                                    call.ArgumentParser().add_argument('-mc', '--max-conns', required=False, help='General server maximum connections. Defaults to none.', type=int),
                                                    call.ArgumentParser().add_argument('-mci', '--max-conns-ip', required=False, help='Maximum connections per client ip. Defaults to none.', type=int),
                                                    call.ArgumentParser().add_argument('-p', '--port', required=False, help='Server port. This must be greater than 1023 unless you run this script as root.Defaults to 2121.', type=int, default=2121),
                                                    call.ArgumentParser().parse_args(),
                                                    call.ArgumentParser().parse_args()])
        self.assertEqual(logging_mock.mock_calls, [call.getLogger('config'),
                                                   call.getLogger().info('Max delay set to 5'),
                                                   call.getLogger('config'),
                                                   call.getLogger().info('Delay rate set to 8'),
                                                   call.getLogger('config'),
                                                   call.getLogger().info('Failure rate set to 5'),
                                                   call.getLogger('config'),
                                                   call.getLogger().info('General maximum connections set to None'),
                                                   call.getLogger('config'),
                                                   call.getLogger().info('Connections per client ip set to None')])
