from cProfile import label
from cmath import e, inf
from genericpath import exists
from urllib import request

from sklearn import preprocessing
from default_prediction.constant import COLUMNS_KEY, CONFIG_DIR, NUMERICAL_COLUMN_KEY, ROOT_DIR, SCHEMA_FILE_NAME, TARGET_COLUMN_KEY
from default_prediction.entity.config_entity import DataIngestionConfig
from default_prediction.exception import ExceptionHandler
from default_prediction.logger import logging
import os,sys
from default_prediction.entity.artifact_entity import DataIngestionArtifact
import csv
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from default_prediction.constant import *
import shutil
from default_prediction.util.util import load_numpy_array_data,column
from default_prediction.config.configuration import Configuration


class DataIngestion:
    def __init__(self,config:Configuration()):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.config=Configuration()
            self.data_ingestion_config = self.config.get_data_ingestion_config()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def download_default_prediction_data(self)->str:
        try:
            ## Extrecting remote url to download dataset
            download_url = self.data_ingestion_config.data_download_url

            ## folder location to download file

            csv_download_dir= self.data_ingestion_config.csv_download_dir

            if os.path.exists(csv_download_dir):
                os.remove(csv_download_dir)

            os.makedirs(csv_download_dir,exist_ok=True)

            default_prediction_file_name = os.path.basename(download_url)

            csv_file_path = os.path.join(csv_download_dir,default_prediction_file_name)

            logging.info(f"downloading file from: [{download_url}] into directory: [{csv_file_path}]")

            urllib.request.urlretrieve(download_url,csv_file_path)
            logging.info(f"file: [{csv_file_path}] has been downloaded successfully.")

            return csv_file_path

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def extrect_csv_file(self):
        try:

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            csv_dir_path = self.data_ingestion_config.csv_download_dir

            download_url = self.data_ingestion_config.data_download_url

            file_name = os.path.basename(download_url)

            file_path = os.path.join(raw_data_dir,file_name)

            urllib.request.urlretrieve(download_url,file_path)

            #shutil.copy(csv_dir_path,raw_data_dir)

            raw_data_dir

            logging.info(f"extraction Completed")

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_modified_df(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            raw_data_file_path = os.path.join(raw_data_dir,file_name)

            default_prediction_data_frame =  pd.read_csv(raw_data_file_path)

            default_prediction_data_frame.rename(columns = {'Unnamed: 0' : 'CustomerID'},inplace=True)

            return default_prediction_data_frame

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_preprocessing_dataset(self):
        try:
            default_pred_df = self.get_modified_df()

            dataset_for_preprocessing = default_pred_df.drop(columns="SeriousDlqin2yrs",axis = 1)

            #dataset_target = default_pred_df["SeriousDlqin2yrs"]

            simple_imputer = SimpleImputer(strategy="mean")

            default_prediction_array_data = simple_imputer.fit_transform(dataset_for_preprocessing)

            scaler = StandardScaler()

            scalled_default_pred_arr = scaler.fit_transform(default_prediction_array_data)

            #preprocessed_df = pd.DataFrame(scalled_default_pred_arr)

            #default_pred_processed_df =  pd.concat([preprocessed_df,dataset_target],axis = 1)

            #default_pred_processed_df.columns = column

            preprocessed_dataset_file_dir = self.data_ingestion_config.preprocessed_dataset_path

            np.save(preprocessed_dataset_file_dir,scalled_default_pred_arr)

            preprocessed_dataset_file_path = os.path.join(preprocessed_dataset_file_dir,preprocessed_dataset_file_dir+".npy")

            preprocessed_numpy_arr_data = load_numpy_array_data(file_path=preprocessed_dataset_file_path)

            return preprocessed_numpy_arr_data

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:

            raw_data_dir = self.data_ingestion_config.raw_data_dir
            #download_url = self.data_ingestion_config.data_download_url

            file_name = os.listdir(raw_data_dir)[0]
            file_path = os.path.join(raw_data_dir,file_name)
            default_pred_df = pd.read_csv(file_path)

            target_coulmn_dataframe = default_pred_df["SeriousDlqin2yrs"]

            preprocessed_numpy_arr_data = self.get_preprocessing_dataset()

            preprocessed_dataframe = pd.DataFrame(preprocessed_numpy_arr_data)

            new_default_pred_df =  pd.concat([preprocessed_dataframe,target_coulmn_dataframe],axis = 1)

            new_default_pred_df.columns = column

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            #dataset_download_url = self.data_ingestion_config.data_download_url

            #file_name = os.path.basename(dataset_download_url)

            file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Spliting Data into Train and Test")
            train_set = None
            test_set = None

            train_set = new_default_pred_df.loc[:120000]
            #train_set_csv = train_set.to_csv()
            test_set= new_default_pred_df[120000:]
            #test_set_csv = test_set.to_csv()


            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_path)
            test_file_path =  os.path.join(self.data_ingestion_config.ingested_test_dir,file_path)

            if train_set is not None:
                os.makedirs(train_file_path,exist_ok=True)
                logging.info(f"Exporting Training Dataset To file:[{train_file_path}]")
                
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(test_file_path,exist_ok=True)
                logging.info(f"Exporting Test Dataset To file:[{test_file_path}]")
                
                test_set.to_csv(test_file_path,index=False)


            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path = test_file_path,
                                                            is_ingested= True,
                                                            message=f"Data Ingestion Completed Successfully"
                                                            )
            logging.info(f"Data Ingestion Artifact :[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise ExceptionHandler(e,sys) from e


    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            #csv_file_path = self.download_housing_data()

            #self.extrect_csv_file(csv_file_path=csv_file_path)

            return self.split_data_as_train_test()
        except Exception as  e:
            raise ExceptionHandler(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")
        