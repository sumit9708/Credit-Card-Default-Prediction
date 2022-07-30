from setuptools import setup,find_packages
from typing import List

## declearing variables for the setup function

PROJECT_NAME = "default_prediction"
VERSION = "0.0.1"
AUTHOR = "Sumit Bhagat"
DESCRIPTION = "This is the project to identify credict card customer who may be defult in next 2 years"
#PACKAGES = ['housing']
REQUIREMENT_FILE_NAME='requirements.txt'
HYPHEN_E_DOT="-e ."

"""
Description - This function is going to return list of requirements mention in requirements.txt file.

return: this function is going to return a list which contains the list of libraries
mentioned in requiremnts.txt file.
"""
def get_requirements_list()->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = [requirement.replace("\n","")  for requirement in requirement_file.readlines()]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list


setup(

name = PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESCRIPTION,
packages=find_packages(), # PACKAGES
install_requires=get_requirements_list()

)
