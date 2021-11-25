# author: Group 24
# date: 2021-11-25

'''This script creates pre-processor for the Crime Vancouver data (from https://geodash.vpd.ca/opendata/)

Usage: pre_process_data.py --out_path=<out_path>

Options:
--out_path=<out_path>       Path to directory where the processed data and pre-processor object should be written
'''
import pandas as pd
import numpy as np
from docopt import docopt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    PolynomialFeatures,
    StandardScaler,
)

opt = docopt(__doc__)

def main(out_path):
   
    # Define columns for transformation
    drop_features = ["HUNDRED_BLOCK"]
    neighbour_feature = ["NEIGHBOURHOOD"]
    categorical_features = ["YEAR", "MONTH", "DAY", "HOUR", "MINUTE"]
    numeric_features = ["X", "Y"]

    # preprocessor for EDA and model training
    preprocessor = make_column_transformer(
        (
            make_pipeline(
                SimpleImputer(strategy="constant", fill_value="Central Business District"),
                OneHotEncoder(handle_unknown="ignore", sparse=False),
            ),
            neighbour_feature,
        ),
        (OneHotEncoder(handle_unknown="ignore", sparse=False), categorical_features),
       (
           make_pipeline(
               SimpleImputer(strategy="median"),
               StandardScaler(),
           ),
           numeric_features
       ),
        ("drop", drop_features),
    )
    

    # Save pre-processed data        
    try:
        filename = 'preprocessor.p'
        outfile = open(out_path+ "/" + filename,'wb')
        pickle.dump(preprocessor, outfile)
        outfile.close()
        
        print(f"Pre-processor is loaded successfully at %s" %(out_path + filename))    
        
    except Exception as error:
        print(f"Error message: %s" %error)
        print("Error while saving pre-processor!")
    
if __name__ == "__main__":
    main(opt['--out_path'])
