import os,sys
from collections import namedtuple
from default_prediction.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from default_prediction.exception import ExceptionHandler
from default_prediction.constant import *
from default_prediction.util.util import read_yaml_file
from default_prediction.logger import logging

class Configuration:
    def __init__(self):
        try:
            self.config_info = read_yaml_file(file_path=CONFIG_FILE_PATH)
            self.training_pipeline_config =  self.get_training_pipeline_config()
            self.time_stamp = get_current_time_stamp()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            logging.info("-------------------Training Pipeline Config Log Started-----------------------")
            self.data_ingestion_config = self.config_info[DATA_INGESTION_CONFIG_KEY]
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
            DATA_INGESTION_ARTIFACT_DIR_NAME,self.time_stamp
            )

            logging.info(f"data_ingestion_artifact_dir_path is : [{data_ingestion_artifact_dir}]")

            dataset_import_url = self.data_ingestion_config[DATA_INGESTION_DATASET_IMPORT_LINK]
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                self.data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )
            logging.info(f"dataset_import_url is : [{dataset_import_url}]")

            ingested_train_dir = os.path.join(data_ingestion_artifact_dir,
                self.data_ingestion_config[DATA_INGESTION_INGESTED_DATA_DIR_KEY],
                self.data_ingestion_config[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
            )
            logging.info(f"ingested_train_file_path is : [{ingested_train_dir}]")
            ingested_test_dir = os.path.join(data_ingestion_artifact_dir,
                self.data_ingestion_config[DATA_INGESTION_INGESTED_DATA_DIR_KEY],
                self.data_ingestion_config[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
            )
            logging.info(f"ingested_test_dir is : [{ingested_test_dir}]")

            data_ingestion_config = DataIngestionConfig(dataset_import_url, 
            raw_data_dir, 
            ingested_train_dir, 
            ingested_test_dir
            )

            logging.info(f"data_ingestion_config is : [{data_ingestion_config}]")

            return data_ingestion_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            logging.info("get_training_pipeline_config log Started")
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            training_pipeline_config_name = self.config_info[TRAINING_PIPELINE_NAME_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config:{training_pipeline_config}")

            logging.info(f"training_pipeline_config is : [{training_pipeline_config}]")
        
            return training_pipeline_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e