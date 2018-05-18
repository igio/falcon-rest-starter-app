import os
import configparser


SECRET_KEY = "374ec40b-0a8c-4a10-9e7d-ae27a4217478"
TOKEN_EXPIRES = 3600

APP_ENV = os.environ.get('APP_ENV') or 'dev'

INI_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '%s.ini' % APP_ENV
)
CONFIG = configparser.ConfigParser()
CONFIG.read(INI_FILE)

POSTGRES = CONFIG['postgres']
DATABASE_URL = "postgresql+psycopg2://%s:%s@%s/%s" % (POSTGRES['user'], POSTGRES['password'],
                                                      POSTGRES['host'], POSTGRES['database'])
DB_ECHO = True if CONFIG['database']['echo'] == 'yes' else False
DB_AUTOCOMMIT = True

LOG_LEVEL = CONFIG['logging']['level']
