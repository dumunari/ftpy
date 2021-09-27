from src.utils.args import Args
import logging
import random
import time
from pyftpdlib.handlers import FTPHandler


class CustomHandler(FTPHandler):

    @property
    def args(self):
        return Args().retrieve_args()

    def ftp_STOR(self, file, mode='w'):
        if self.args['failure_rate'] != 0 and random.randint(1, 10) <= self.args['failure_rate']:
            super().ftp_STOR('', mode)
            logging.info(f"[STOR] [{file}] - Abrupt failure inserted.")
            return
        super().ftp_STOR(file, mode)
        self.__add_delay('STOR', file)

    def ftp_RETR(self, file):
        if self.args['failure_rate'] != 0 and random.randint(1, 10) <= self.args['failure_rate']:
            super().ftp_RETR('')
            logging.info(f"[RETR] [{file}] - Abrupt failure inserted.")
            return
        super().ftp_RETR(file)
        self.__add_delay('RETR', file)

    def __add_delay(self, action, file):
        if self.args['delay_rate'] != 0 and random.randint(1, 10) <= self.args['delay_rate']:
            delay = random.randint(1, 5)
            logging.info(f"Adding {delay}s delay to your action: {action} [{file}]")
            time.sleep(delay)
            logging.info(f"Delay released")



