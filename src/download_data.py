# author: Group 24
# date: 2021-11-19

'''This script downloads data from 'wosaku/crime-in-vacouver' Kaggle.com using
its API and saves its to a data file path. This script takes an quoted file path.

Usage: download_data.py --kaggle_path=<kaggle_path> --file_path=<file_path>

Options:
--kaggle_path=<kaggle_path>   Path of the kaggle data set
--file_path=<file_path>   Path to the data file
'''
import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)


try:
    import kaggle
except ModuleNotFoundError:
    print('ERROR : Please install the kaggle module using : pip install kaggle')
except OSError:
    print ("ERROR :You must authenticate using an API token please follow the instructions")
    print("First, create a kaggle account. Go to account setting and create a 'New API Token'")
    print("then, move the downloaded .json file to your ~/.kaggle directory in your computer")


def main(kaggle_path, file_path):
    
    
    # if the files is not in the directory create one
    if not os.path.exists(os.path.dirname(file_path)):
        # create a data directory
        os.makedirs(os.path.dirname(file_path))
        
    # download the data in that directory
    kaggle.api.dataset_download_files(kaggle_path,
                                      path=file_path,
                                      unzip=True)
    
    
if __name__ == "__main__":
    main(opt['--kaggle_path'], opt['--file_path']
