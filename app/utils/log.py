import sys
import logging
import os

from ..config import config

# A basic logger for the application.

logging.basicConfig(level=config.LOG_LEVEL)
LOG = logging.getLogger('API')
LOG.propagate = False

INFO_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
DEBUG_FORMAT = '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
TIMESTAMP_FORMAT = '%m/%d/%Y %H:%M:%S %z'


def create_log_folder():
    if not os.path.exists('log'):
        os.mkdir('log')

if config.APP_ENV == 'prod':
    from logging.handlers import RotatingFileHandler
    create_log_folder()
    file_handler = RotatingFileHandler('log/app.log', 'a', 1*1024*1024, 10)
    formatter = logging.Formatter(INFO_FORMAT, TIMESTAMP_FORMAT)
    LOG.addHandler(file_handler)

if config.APP_ENV in ['dev', 'test']:
    from logging.handlers import RotatingFileHandler
    create_log_folder()
    if os.path.exists('log/app.log'):
        os.remove('log/app.log')
    file_handler = RotatingFileHandler('log/app.log', 'a', 1*1024*1024, 10)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(DEBUG_FORMAT, TIMESTAMP_FORMAT)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    LOG.addHandler(file_handler)
    LOG.addHandler(stream_handler)


def get_logger():
    return LOG
