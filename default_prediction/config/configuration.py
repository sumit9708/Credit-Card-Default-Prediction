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
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
            csv_download_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_CSV_DOWNLOAD_DIR_KEY]
            )
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY],
            )

            preprocessed_dataset_path = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_PREPROCESSED_DATASET_DIR_KEY])

            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            ingested_train_dir = os.path.join(ingested_data_dir,
            data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir = os.path.join(ingested_data_dir,
            data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url,
                csv_download_dir,
                raw_data_dir,
                preprocessed_dataset_path,
                ingested_train_dir, 
                ingested_test_dir,
            )
            logging.info(f"data_ingestion_config is : [{data_ingestion_config}]")

            return data_ingestion_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            logging.info("get_training_pipeline_config log Started")
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            #training_pipeline_config_name = self.config_info[TRAINING_PIPELINE_NAME_KEY]
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