from os import getenv, getcwd

FTP_USER = getenv("FTP_USER", 'user')  # pragma: no mutate
FTP_PASSWORD = getenv("FTP_PASSWORD", 'pass')  # pragma: no mutate
FTP_DIRECTORY = getenv("FTP_DIRECTORY", getcwd() + '/public/')  # pragma: no mutate
FTP_PERM = getenv("FTP_PERM", 'elradfmw')  # pragma: no mutate

