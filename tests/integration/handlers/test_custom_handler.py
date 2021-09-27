import ftplib
import os
import unittest
from io import BytesIO
from unittest.mock import patch, call
from pyftpdlib.handlers import FTPHandler
from src.handlers.custom_handler import CustomHandler
from tests.integration.helpers.FTPd import FTPd

USER = 'user'
PASSWD = '12345'
TESTFN = 'test.iml'
TIMEOUT = 2


class TestCustomHandler(unittest.TestCase):
    """Test FTPHandler class callback methods."""
    server_class = FTPd
    client_class = ftplib.FTP

    def setUp(self):
        self.client = None
        self.server = None
        self._tearDown = True

    def _setUp(self, handler, connect=True, login=True):
        FTPd.handler = handler
        self.server = self.server_class()
        self.server.start()
        self.client = self.client_class()
        if connect:
            self.client.connect(self.server.host, self.server.port)
            self.client.sock.settimeout(TIMEOUT)
            if login:
                self.client.login(USER, PASSWD)
        self.file = open(TESTFN, 'w')
        self.dummyfile = BytesIO()
        self._tearDown = False

    def tearDown(self):
        if not self._tearDown:
            FTPd.handler = FTPHandler
            self._tearDown = True
            if self.client is not None:
                self.client.close()
            if self.server is not None:
                self.server.stop()
            if not self.file.closed:
                self.file.close()
            if not self.dummyfile.closed:
                self.dummyfile.close()
            os.remove(TESTFN)

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_STOR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_STOR_no_delay_no_abrupt_failure(self, args_mock, logging_mock, random_mock, stor_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 0, 'failure_rate': 0,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        handler = CustomHandler
        self._setUp(handler=handler)

        # act
        try:
            self.client.storlines('stor ' + TESTFN, self.dummyfile)
        except:
            self.assertEqual(stor_mock.mock_calls, [call(os.getcwd() + '/public/test.iml', 'w')])
            self.assertEqual(random_mock.mock_calls, [])
            self.assertEqual(logging_mock.mock_calls, [])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_STOR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_STOR_delay_enabled_but_not_applied_no_abrupt_failure(self, args_mock, logging_mock, random_mock, stor_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 0,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.return_value = 6

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.storlines('stor ' + TESTFN, self.dummyfile)
        except:
            self.assertEqual(stor_mock.mock_calls, [call(os.getcwd() + '/public/test.iml', 'w')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10)])
            self.assertEqual(logging_mock.mock_calls, [])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_STOR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_STOR_delay_enabled_and_applied_no_abrupt_failure(self, args_mock, logging_mock, random_mock, stor_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 0,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.side_effect = [5, 3]
        time_mock.sleep.return_value = ''

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.storlines('stor ' + TESTFN, self.dummyfile)
        # assert
        except:
            self.assertEqual(stor_mock.mock_calls, [call(os.getcwd() + '/public/test.iml', 'w')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10),
                                                      call.randint(1, 5)])
            self.assertEqual(logging_mock.mock_calls, [call.info('Adding 3s delay to your action: STOR ['
                                                                 + os.getcwd() + '/public/test.iml]'),
                                                       call.info('Delay released')])
            self.assertEqual(time_mock.mock_calls, [call.sleep(3)])

        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_STOR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_STOR_abrupt_failure_enabled_but_not_applied_and_delay_enabled_and_applied(self, args_mock, logging_mock, random_mock, stor_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.side_effect = [7, 5, 3]
        time_mock.sleep.return_value = ''

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.storlines('stor ' + TESTFN, self.dummyfile)
        # assert
        except:
            self.assertEqual(stor_mock.mock_calls, [call(os.getcwd() + '/public/test.iml', 'w')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10),
                                                      call.randint(1, 10),
                                                      call.randint(1, 5)])
            self.assertEqual(logging_mock.mock_calls, [call.info('Adding 3s delay to your action: STOR ['
                                                                 + os.getcwd() + '/public/test.iml]'),
                                                       call.info('Delay released')])
            self.assertEqual(time_mock.mock_calls, [call.sleep(3)])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_STOR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_STOR_abrupt_failure_enabled_but_not_applied_and_delay_enabled_and_not_applied(self, args_mock, logging_mock, random_mock, stor_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.side_effect = [7, 6]

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.storlines('stor ' + TESTFN, self.dummyfile)
        # assert
        except:
            self.assertEqual(stor_mock.mock_calls, [call(os.getcwd() + '/public/test.iml', 'w')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10),
                                                      call.randint(1, 10)])
            self.assertEqual(logging_mock.mock_calls, [])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_STOR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_STOR_abrupt_failure_enabled_and_applied(self, args_mock, logging_mock, random_mock, stor_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.return_value = 5

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.storlines('stor ' + TESTFN, self.dummyfile)
        # assert
        except:
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10)])
            self.assertEqual(stor_mock.mock_calls, [call('', 'w')])
            self.assertEqual(logging_mock.mock_calls, [call.info('[STOR] [' +
                                                       os.getcwd() + '/public/test.iml] - Abrupt failure inserted.')])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_RETR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_RETR_no_delay_no_abrupt_failure(self, args_mock, logging_mock, random_mock, retr_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 0, 'failure_rate': 0,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.retrlines('retr ' + TESTFN)
        except:
            self.assertEqual(retr_mock.mock_calls, [call(os.getcwd() + '/public/test.iml')])
            self.assertEqual(random_mock.mock_calls, [])
            self.assertEqual(logging_mock.mock_calls, [])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_RETR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_RETR_delay_enabled_but_not_applied_no_abrupt_failure(self, args_mock, logging_mock, random_mock, retr_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 0,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.return_value = 6

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.retrlines('retr ' + TESTFN)
        except:
            self.assertEqual(retr_mock.mock_calls, [call(os.getcwd() + '/public/test.iml')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10)])
            self.assertEqual(logging_mock.mock_calls, [])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_RETR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_RETR_delay_enabled_and_applied_no_abrupt_failure(self, args_mock, logging_mock, random_mock, retr_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 0,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.side_effect = [5, 3]
        time_mock.sleep.return_value = ''

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.retrlines('retr ' + TESTFN)
        # assert
        except:
            self.assertEqual(retr_mock.mock_calls, [call(os.getcwd() + '/public/test.iml')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10),
                                                      call.randint(1, 5)])
            self.assertEqual(logging_mock.mock_calls, [call.info('Adding 3s delay to your action: RETR ['
                                                                 + os.getcwd() + '/public/test.iml]'),
                                                       call.info('Delay released')])
            self.assertEqual(time_mock.mock_calls, [call.sleep(3)])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_RETR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_RETR_abrupt_failure_enabled_but_not_applied_and_delay_enabled_and_applied(self, args_mock, logging_mock, random_mock, retr_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.side_effect = [7, 5, 3]
        time_mock.sleep.return_value = ''

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.retrlines('retr ' + TESTFN)
        # assert
        except:
            self.assertEqual(retr_mock.mock_calls, [call(os.getcwd() + '/public/test.iml')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10),
                                                      call.randint(1, 10),
                                                      call.randint(1, 5)])
            self.assertEqual(logging_mock.mock_calls, [call.info('Adding 3s delay to your action: RETR ['
                                                                 + os.getcwd() + '/public/test.iml]'),
                                                       call.info('Delay released')])
            self.assertEqual(time_mock.mock_calls, [call.sleep(3)])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_RETR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_RETR_abrupt_failure_enabled_but_not_applied_and_delay_enabled_and_not_applied(self, args_mock, logging_mock, random_mock, retr_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.side_effect = [7, 6]

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.retrlines('retr ' + TESTFN)
        # assert
        except:
            self.assertEqual(retr_mock.mock_calls, [call(os.getcwd() + '/public/test.iml')])
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10),
                                                      call.randint(1, 10)])
            self.assertEqual(logging_mock.mock_calls, [])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()

    @patch('src.handlers.custom_handler.time')
    @patch('src.handlers.custom_handler.FTPHandler.ftp_RETR')
    @patch('src.handlers.custom_handler.random')
    @patch('src.handlers.custom_handler.logging')
    @patch('src.handlers.custom_handler.Args')
    def test_ftp_RETR_abrupt_failure_enabled_and_applied(self, args_mock, logging_mock, random_mock, retr_mock, time_mock):
        # arrange
        args_mock.return_value.retrieve_args.return_value = {'max_delay': 5, 'delay_rate': 5, 'failure_rate': 5,
                                                             'max_conns': None, 'max_conns_ip': None, 'port': 2121}

        random_mock.randint.return_value = 5

        self._setUp(handler=CustomHandler)

        # act
        try:
            self.client.retrlines('retr ' + TESTFN)
        # assert
        except:
            self.assertEqual(random_mock.mock_calls, [call.randint(1, 10)])
            self.assertEqual(retr_mock.mock_calls, [call('')])
            self.assertEqual(logging_mock.mock_calls, [call.info('[RETR] [' +
                                                       os.getcwd() + '/public/test.iml] - Abrupt failure inserted.')])
            self.assertEqual(time_mock.mock_calls, [])
        finally:
            self.tearDown()