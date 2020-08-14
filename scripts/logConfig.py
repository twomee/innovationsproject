import logging.config
import logging
from os import path

class Log:
    def configureLogger():
        log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.config',)
        print(log_file_path)
        logging.config.fileConfig(log_file_path,defaults={'logfilename': "logsoutput.log"},disable_existing_loggers=False)
        logger = logging.getLogger('dev')
        return logger