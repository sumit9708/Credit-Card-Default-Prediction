from email import message
import os,sys
from tkinter import E
from default_prediction.config.configuration import Configuration
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
from default_prediction.util.util import read_yaml_file
from six.moves import urllib
from  default_prediction.entity.artifact_entity import DataIngestionArtifact
from default_prediction.entity.config_entity import DataIngestionConfig
import shutil
import pandas as pd
import numpy as np

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_dowloaded_data(self):
        try:
            download_url = self.data_ingestion_config.data_download_url

            csv_download_dir = self.data_ingestion_config.csv_download_dir

            if os.path.exists(csv_download_dir):
                os.remove(csv_download_dir)

            os.makedirs(csv_download_dir,exist_ok=True)

            csv_file_name = os.path.basename(download_url)

            csv_file_path = os.path.join(csv_download_dir,csv_file_name)

            urllib.request.urlretrieve(download_url,csv_file_path)

            return csv_file_path

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_raw_csv_data(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            csv_download_dir = self.data_ingestion_config.csv_download_dir

            download_url = self.data_ingestion_config.data_download_url

            file_name = os.path.basename(download_url)

            file_path = os.path.join(raw_data_dir,file_name)

            urllib.request.urlretrieve(download_url,file_path)

            shutil.copy(raw_data_dir,raw_data_dir)

            return raw_data_dir

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def split_into_train_and_test_data(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            print(raw_data_dir)

            file_name = os.listdir(raw_data_dir)[0]

            file_path = os.path.join(raw_data_dir,file_name)

            print(file_path)

            default_prediction_dataframe = pd.read_csv(file_path)

            train_set = default_prediction_dataframe[:120000]

            test_set = default_prediction_dataframe[120000:]

            return train_set,test_set

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            train_set,test_set = self.split_into_train_and_test_data()

            ingested_test_dir = self.data_ingestion_config.ingested_test_dir
            ingested_train_dir = self.data_ingestion_config.ingested_train_dir

            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            train_file_path = os.path.join(ingested_train_dir,file_name)

            os.makedirs(train_file_path,exist_ok=True)
            logging.info(f"Exporting Training Dataset To file:[{train_file_path}]")

            test_file_path = os.path.join(ingested_test_dir,file_name)

            os.makedirs(test_file_path,exist_ok=True)
            logging.info(f"Exporting Test Dataset To file:[{test_file_path}]")

            train_arr_data = train_set.to_numpy()

            np.save(train_file_path,train_arr_data)

            test_arr_data = test_set.to_numpy()

            np.save(test_file_path,test_arr_data)

            is_ingested = True

            message = "Data Ingestion Completed Successfuly"

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path, 
                test_file_path, 
                is_ingested, 
                message
            )

            logging.info(f"data_ingestion_artifact is : [{data_ingestion_artifact}]")

            return data_ingestion_artifact
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")