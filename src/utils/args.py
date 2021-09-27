import argparse
import logging
from src.utils.singleton_meta import SingletonMeta


class Args(metaclass=SingletonMeta):
    def __init__(self):
        self.arg_parse = argparse.ArgumentParser()
        self.arg_parse.add_argument("-md", "--max-delay", required=False,
                                    help="Max delay on STOR and RETR, in seconds. Min is always set to 1s. "
                                         "Will have no effect if delay-rate is 0. "
                                         "Defaults to 5s",
                                    type=int,
                                    default=5)
        self.arg_parse.add_argument("-dr", "--delay-rate", required=False,
                                    help="Desired delay rate on STOR and RETR, from 0 to 10, where 1 means 10 percent. "
                                         "0 means no delay. "
                                         "Defaults to 80 percent",
                                    type=int,
                                    default=8)
        self.arg_parse.add_argument("-fr", "--failure-rate", required=False,
                                    help="Desired failure rate on STOR and RETR, from 1 to 10, where 1 means 10 percent. "
                                         "0 means no failure rate. "
                                         "Defaults to 50 percent",
                                    type=int,
                                    default=5)
        self.arg_parse.add_argument("-mc", "--max-conns", required=False,
                                    help="General server maximum connections. "
                                         "Defaults to none.",
                                    type=int)
        self.arg_parse.add_argument("-mci", "--max-conns-ip", required=False,
                                    help="Maximum connections per client ip. "
                                         "Defaults to none.",
                                    type=int)
        self.arg_parse.add_argument("-p", "--port", required=False,
                                    help="Server port. This must be greater than 1023 unless you run this script as root."
                                         "Defaults to 2121.",
                                    type=int,
                                    default=2121)
        self.__log_args()

    def __log_args(self):
        args = vars(self.arg_parse.parse_args())
        logging.getLogger("config").info(f"Max delay set to {args['max_delay']}")
        logging.getLogger("config").info(f"Delay rate set to {args['delay_rate']}")
        logging.getLogger("config").info(f"Failure rate set to {args['failure_rate']}")
        logging.getLogger("config").info(f"General maximum connections set to {args['max_conns']}")
        logging.getLogger("config").info(f"Connections per client ip set to {args['max_conns_ip']}")

    def retrieve_args(self):
        return vars(self.arg_parse.parse_args())
