import os,sys
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
from default_prediction.config.configuration import Configuration


def demo():
    try:
        logging.info("------------demo log started--------------------")
        config_info = Configuration()
        logging.info("---------------demo log finished----------------------")
        return config_info.get_data_ingestion_config(),config_info.get_training_pipeline_config()
    except Exception as e:
        raise ExceptionHandler(e,sys) from e