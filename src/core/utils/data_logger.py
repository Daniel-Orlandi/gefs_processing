from core import utils
import os
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
import logging.config

class Logger:
    """ 
    Logger class 
    ...

    Attributes
    ----------
    logger_name:str
        logger choosen name.

    filename: str = None
        if not none, log file name, where the logs will be saved.
        else, filename will be log_file.log at project root.

    log_format: str = None
        if not none, change log formating.
        else, use standart log formating : 2020-12-23 14:23:05
    Methods
    -------
    get_logger(self):
        get logger.

    """

    def __init__(self, logger_name:str, filename:str = None, log_format: str = None):
        self.logger_name = logger_name
        self.logger = None        
        
        if (isinstance(filename, str)):
            self.filename = filename

        else:
            self.filename = "/usr/src/app/src/logs/log_file.log"
            file_name = Path(self.filename)          
            path = Path(file_name.parent)           
            path.mkdir(parents=True, exist_ok=True)

            if(file_name.is_file() == False):                              
               open(f'{path}/log_file.log','x')            

        if (isinstance(log_format, str)):
            self.log_format = logging.Formatter(log_format)
        
        else:
          logging.config.fileConfig("/usr/src/app/src/logger_config_file.conf")

        self.logger = logging.getLogger(self.logger_name)

    def get_logger(self):    
        return self.logger
    

        
