import sys, os
import logging
from logging.handlers import TimedRotatingFileHandler


class MyLogger():
    def init_app(self, app, dev):
        
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s')
        logger_handler = logging.StreamHandler(sys.stdout)

        if dev is True:            
            logger_handler.setFormatter(formatter)
            app.logger.addHandler(logger_handler)
            app.logger.setLevel(logging.DEBUG)

        else:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
            if not os.path.isdir(log_dir):
               os.makedirs(log_dir)

            log_path = os.path.join(log_dir, "log")
            logger_handler = TimedRotatingFileHandler(log_path, when="midnight", interval=1, encoding='utf-8', backupCount=90)
            logger_handler.suffix = "%Y-%m-%d"
            logger_handler.setFormatter(formatter)

            # set app logger
            app.logger.addHandler(logger_handler)
            app.logger.setLevel(logging.INFO)

my_logger = MyLogger()