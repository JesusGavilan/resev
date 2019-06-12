import psycopg2
import os
import configparser
from itertools import chain

API_NAME = 'Resev'

SECRET_KEY = 'lxHtkOOGIGdEc2D3FSbIskeSF9t92bw8VRJT2X-CV6I='
UUID_LEN = 10
UUID_ALPHABET = ''.join(map(chr, range(48, 58)))
TOKEN_EXPIRES = 3600

INI_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../config/dev.ini')

CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)
DATABASE = CONFIG['database']

DB_CONFIG = (DATABASE['user'], DATABASE['password'], DATABASE['host'], DATABASE['database'])
DATABASE_URL = "postgresql+psycopg2://%s:%s@%s/%s" % DB_CONFIG

DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG['logging']['level']