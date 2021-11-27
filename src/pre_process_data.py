# author: Thomas Siu (Group 24)
# contributors: Ramiro Francisco Mejia, Jasmine Ortega, Shi Yan Wang
# date: 2021-11-25
# last updated: 2021-11-27

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

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier

opt = docopt(__doc__)


def main(out_path):

    drop_features = ["HUNDRED_BLOCK"]
    categorical_feature_n = ["NEIGHBOURHOOD"]
    categorical_features = ["YEAR", "MONTH", "DAY", "HOUR", "MINUTE"]
    numerical_features = ["X", "Y"]

    # preprocessor for EDA and model training
    preprocessor = make_column_transformer(

        (make_pipeline(
            SimpleImputer(strategy="constant", fill_value="most_frequent"),
            OneHotEncoder(handle_unknown="ignore", sparse=False),
        ), categorical_feature_n,
        ),

        (OneHotEncoder(handle_unknown="ignore", drop='if_binary',
                       sparse=False), categorical_features),

        (make_pipeline(
            SimpleImputer(strategy="most_frequent"),  # these are coordinates
            StandardScaler(),
        ), numerical_features
        ),

        ("drop", drop_features),
    )

    models = {
        "DummyClassifier": DummyClassifier(),
        "LogisticRegression": LogisticRegression(max_iter=1000, multi_class="ovr"),
        "RandomForest": RandomForestClassifier(),
        "RidgeClassifier": RidgeClassifier()
    }

    # Save pre-processed data
    try:
        filename = 'preprocessor.p'
        outfile = open(out_path + "/" + filename, 'wb')
        pickle.dump(preprocessor, outfile)
        outfile.close()

        print(f"Pre-processor is loaded successfully at %s" %
              (out_path + filename))

    except Exception as error:
        print(f"Error message: %s" % error)
        print("Error while saving pre-processor!")

    # Save models dictionary
    try:
        filename = 'models.p'
        outfile = open(out_path + "/" + filename, 'wb')
        pickle.dump(models, outfile)
        outfile.close()

        print(f"models is loaded successfully at %s" % (out_path + filename))

    except Exception as error:
        print(f"Error message: %s" % error)
        print("Error while saving models!")


if __name__ == "__main__":
    main(opt['--out_path'])
