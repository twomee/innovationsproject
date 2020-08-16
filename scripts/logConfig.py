import logging.config
import logging
from os import path

class Log:
    LOG_FILE_NAME = 'logging.ini'
    LOGHER_CONFIG_NAME = 'innovations'

    def configureLogger():
        log_file_path = path.join(path.dirname(path.abspath(__file__)), Log.LOG_FILE_NAME,)
        print(log_file_path)
        logging.config.fileConfig(log_file_path)
        logger = logging.getLogger(Log.LOGHER_CONFIG_NAME)
        return logger