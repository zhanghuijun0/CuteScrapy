# coding:utf8
import logging

logger_dict = {

}

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
ch.setFormatter(formatter)


def getLogger(name='root', level='debug'):
    if name in logger_dict.keys():
        return logger_dict[name]
    else:
        logger = logging.getLogger(name)
        logger.propagate = False
        if level.lower() == 'debug':
            logger.setLevel(logging.DEBUG)
        if level.lower() == 'info':
            logger.setLevel(logging.INFO)
        if level.lower() == 'error':
            logger.setLevel(logging.ERROR)
        if not logger.handlers:
            logger.addHandler(ch)
        logger_dict[name] = logger
        return logger
