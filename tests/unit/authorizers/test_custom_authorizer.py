import os
import unittest
from unittest.mock import patch, call
from src.authorizers.custom_authorizer import CustomAuthorizer


class TestCustomAuthorizer(unittest.TestCase):

    @patch('src.authorizers.custom_authorizer.config')
    @patch('src.authorizers.custom_authorizer.DummyAuthorizer')
    def test_retrieve_authorizer(self, auth_mock, config_mock):
        # arrange
        config_mock.FTP_USER = 'user'
        config_mock.FTP_PASSWORD = 'pass'
        config_mock.FTP_DIRECTORY = os.getcwd() + '/public/'
        config_mock.FTP_PERM = 'elradfmw'

        # act
        CustomAuthorizer().retrieve_authorizer()

        # assert
        self.assertEqual(auth_mock.mock_calls, [call(),
                                                call().add_user('user', 'pass', os.getcwd() + '/public/',
                                                                perm='elradfmw')])
