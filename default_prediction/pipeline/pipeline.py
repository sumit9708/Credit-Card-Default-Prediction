import os,sys
from default_prediction.component.data_ingestion import DataIngestion
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
from default_prediction.config.configuration import Configuration
from default_prediction.entity.artifact_entity import DataIngestionArtifact
from default_prediction.component.data_ingestion import DataIngestion

class Pipeline:

    def __init__(self, config: Configuration=Configuration()) -> None:
        try:
            self.config = Configuration()
        except Exception as e:
            raise ExceptionHandler(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise ExceptionHandler(e, sys) from e


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info(f"data_ingestion_artifact is : [{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise ExceptionHandler(e,sys) from e
