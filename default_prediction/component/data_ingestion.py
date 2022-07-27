import os,sys
from default_prediction.entity.config_entity import DataIngestionConfig
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
from default_prediction.entity.artifact_entity import DataIngestionArtifact
from default_prediction.config.configuration import Configuration

class DataIngestion:
    def __init__(self,config_info:Configuration=Configuration())->DataIngestionArtifact:
        try:
            self.config_info = Configuration()
            self.training_pipeline_config = config_info.get_training_pipeline_config()
            self.data_ingestion_config = config_info.get_data_ingestion_config()

            artifact_dir = self.training_pipeline_config.artifact_dir
            
        except Exception as e:
            raise ExceptionHandler(e,sys) from e
