import yaml
from default_prediction.exception import ExceptionHandler
import os,sys
import numpy as np
import dill
import pandas as pd
from default_prediction.constant import *
from default_prediction.logger import logging

### This file we have created to write all the helper function to use in pipepline component file

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise ExceptionHandler(e,sys)

def read_yaml_file(file_path:str)->dict:
    """
    This is the function to read config.yaml file and return file content as dictionary
    file_path:str
    """
    try:

        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ExceptionHandler(e,sys) from e

def read_training_file(file_path:str):
    try:
        with open(file_path,"rb") as csv_file:
            for training_file in csv_file:
                if training_file == "cs-training.csv":
                    return training_file
    except Exception as e:
        raise ExceptionHandler(e,sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise ExceptionHandler(e, sys) from e

column = ['CustomerID', 'RevolvingUtilizationOfUnsecuredLines', 'age', 'NumberOfTime30-59DaysPastDueNotWorse', 'DebtRatio', 'MonthlyIncome', 'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate', 'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfDependents','SeriousDlqin2yrs']