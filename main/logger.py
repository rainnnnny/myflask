import logging
import os
from . import config


def getlogger(name):
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        print('hasHandlers', logger)
        return logger

    formatter = logging.Formatter('%(asctime)s  %(filename)s  %(funcName)s  %(levelname)s:  %(message)s')

    path = os.path.join(config.LOG_DIR, '%s.log' % name)

    # use open to create file if not existed
    if not os.path.isfile(path):
        f = open(path, 'w+')
        f.close()

    handler = logging.FileHandler(path)
    handler.formatter = formatter
    
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger
