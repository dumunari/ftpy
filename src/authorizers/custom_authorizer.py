from pyftpdlib.authorizers import DummyAuthorizer
from src import config


class CustomAuthorizer:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        # Define a new user having full r/w permissions.
        self.authorizer.add_user(config.FTP_USER, config.FTP_PASSWORD, config.FTP_DIRECTORY, perm=config.FTP_PERM)

    def retrieve_authorizer(self):
        return self.authorizer
