import os,sys
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
from default_prediction.config.configuration import Configuration

class Pipeline:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise ExceptionHandler(e,sys) from e