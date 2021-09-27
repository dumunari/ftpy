from pyftpdlib.servers import FTPServer
from src.utils.args import Args


class CustomServer:

    @property
    def args(self):
        return Args().retrieve_args()

    def retrieve_server(self, handler):
        address = ('', self.args['port'])
        server = FTPServer(address, handler)
        self.__configure_max_conns(server)
        return server

    def __configure_max_conns(self, server):
        if self.args["max_conns"]:
            server.max_cons = self.args['max_conns']
        if self.args['max_conns_ip']:
            server.max_cons_per_ip = self.args['max_conns_ip']
