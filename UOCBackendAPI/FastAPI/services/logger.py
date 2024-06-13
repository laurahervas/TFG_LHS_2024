import logging
import os
from domain.models.log import Log

class Logger:
    def __init__(self):
        level =os.environ.get("LOG_LEVEL")
        logging_config = { 
            'version': 1,
            'formatters': { 
                'standard': { 
                    'format': '%(asctime)s - %(file)s - %(funcname)s - %(levelname)s - %(title)s - %(request)s - %(response)s'
                },
            },
            'handlers': { 
                'stream': { 
                    'level': level,
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                },
            },
            'loggers': { 
                __name__: { 
                    'handlers': ['stream'],
                    'level': level,
                    'propagate': False
                },
            } 
        }
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(__name__)
        self.setLevel(level)

    def debug(self, log: Log):
        self.logger.debug(log.title, extra=log.getLog())

    def info(self, log: Log):
        self.logger.info(log.title, extra=log.getLog())

    def warning(self, log: Log):
        self.logger.warning(log.title, extra=log.getLog())

    def error(self, log: Log):
        self.logger.error(log.title, extra=log.getLog())
    
    def setLevel(self, level):
            if level == "DEBUG":
                self.logger.setLevel(logging.DEBUG)
            elif level == "INFO":
                self.logger.setLevel(logging.INFO)
            elif level == "WARNING":
                self.logger.setLevel(logging.WARNING)
            elif level == "ERROR":
                self.logger.setLevel(logging.ERROR)
            elif level == "CRITICAL":
                self.logger.setLevel(logging.CRITICAL)
            else:
                print("Invalid log level")