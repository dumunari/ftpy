import os
import socket
import sys
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer

from src.handlers.custom_handler import CustomHandler

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
try:
    import ssl
except ImportError:
    ssl = None
if sys.version_info < (2, 7):
    import unittest2 as unittest  # pip install unittest2
else:
    import unittest
if not hasattr(unittest.TestCase, "assertRaisesRegex"):
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
sendfile = None
if os.name == 'posix':
    try:
        import sendfile
    except ImportError:
        pass

# Attempt to use IP rather than hostname (test suite will run a lot faster)
try:
    HOST = socket.gethostbyname('localhost')
except socket.error:
    HOST = 'localhost'
USER = 'user'
PASSWD = '12345'
HOME = os.getcwd() + '/public/'
TIMEOUT = 2
BUFSIZE = 1024
INTERRUPTED_TRANSF_SIZE = 32768


def try_address(host, port=0, family=socket.AF_INET):
    """Try to bind a socket on the given host:port and return True
    if that has been possible."""
    try:
        sock = socket.socket(family)
        sock.bind((host, port))
    except (socket.error, socket.gaierror):
        return False
    else:
        sock.close()
        return True


SUPPORTS_IPV4 = try_address('127.0.0.1')
SUPPORTS_IPV6 = socket.has_ipv6 and try_address('::1', family=socket.AF_INET6)
SUPPORTS_SENDFILE = hasattr(os, 'sendfile') or sendfile is not None


class FTPd(threading.Thread):
    """A threaded FTP server used for running tests.
    This is basically a modified version of the FTPServer class which
    wraps the polling loop into a thread.
    The instance returned can be used to start(), stop() and
    eventually re-start() the server.
    """
    handler = CustomHandler
    server_class = FTPServer

    def __init__(self, addr=None):
        threading.Thread.__init__(self)
        self.__timeout = TIMEOUT
        self.__serving = False
        self.__stopped = False
        self.__lock = threading.Lock()
        self.__flag = threading.Event()
        if addr is None:
            addr = (HOST, 0)
        authorizer = DummyAuthorizer()
        authorizer.add_user(USER, PASSWD, HOME, perm='elradfmwM')  # full perms
        authorizer.add_anonymous(HOME)
        self.handler.authorizer = authorizer
        # lower buffer sizes = more "loops" while transfering data
        # = less false positives
        self.handler.dtp_handler.ac_in_buffer_size = 4096
        self.handler.dtp_handler.ac_out_buffer_size = 4096
        self.server = self.server_class(addr, self.handler)
        self.host, self.port = self.server.socket.getsockname()[:2]

    def __repr__(self):
        status = [self.__class__.__module__ + "." + self.__class__.__name__]
        if self.__serving:
            status.append('active')
        else:
            status.append('inactive')
        status.append('%s:%s' % self.server.socket.getsockname()[:2])
        return '<%s at %#x>' % (' '.join(status), id(self))

    @property
    def running(self):
        return self.__serving

    def start(self, timeout=0.001):
        """Start serving until an explicit stop() request.
        Polls for shutdown every 'timeout' seconds.
        """
        if self.__serving:
            raise RuntimeError("Server already started")
        if self.__stopped:
            # ensure the server can be started again
            FTPd.__init__(self, self.server.socket.getsockname())
        threading.Thread.start(self)
        self.__flag.wait()

    def run(self):
        self.__serving = True
        self.__flag.set()
        while self.__serving:
            self.__lock.acquire()
            self.server.serve_forever(timeout=self.__timeout, blocking=False)
            self.__lock.release()
        self.server.close_all()

    def stop(self):
        """Stop serving (also disconnecting all currently connected
        clients) by telling the serve_forever() loop to stop and
        waits until it does.
        """
        if not self.__serving:
            raise RuntimeError("Server not started yet")
        self.__serving = False
        self.__stopped = True
        self.join()
