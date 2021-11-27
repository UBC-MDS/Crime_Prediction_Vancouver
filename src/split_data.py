# author: Group 24
# date: 2021-11-25

'''This script cleans, normalize and splits the Crime Vancouver data (from https://geodash.vpd.ca/opendata/)

Usage: split_data.py --input_path=<input_path> --out_path=<out_path>

Options:
--input_path=<input_path>   Path (inclujding filename) to the raw data (.csv file)
--out_path=<out_path>       Path to directory where the processed data and pre-processor object should be written
'''
import pandas as pd
import numpy as np
from docopt import docopt
import os
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


def main(input_path, out_path):

    # Read data from csv and filter the year
    df = pd.read_csv(input_path)
    df = df.query('2010 < YEAR <= 2020')

    # Split data into train and test
    train_df, test_df = train_test_split(df, test_size=0.20, random_state=123)

    # Data cleaning - normalize records which are with HOUR equals to 0
    rebase_zero_hour_count = len(train_df.query(
        "HOUR == 0")) - int(len(train_df["HOUR"] != 0)/23)
    rebase_zero_hour_index = train_df[train_df["HOUR"] == 0].sample(
        rebase_zero_hour_count).index
    train_df.loc[rebase_zero_hour_index, 'HOUR'] = np.random.randint(
        0, 24, rebase_zero_hour_count)

    # Split into feature and target
    X_train, y_train = train_df.drop(columns=["TYPE"]), train_df["TYPE"]
    X_test, y_test = test_df.drop(columns=["TYPE"]), test_df["TYPE"]

    # Save the train and test data
    try:
        X_train.to_csv(out_path + "/training_feature.csv", index_label="index")
        y_train.to_csv(out_path + "/training_target.csv", index_label="index")
        X_test.to_csv(out_path + "/test_feature.csv", index_label="index")
        y_test.to_csv(out_path + "/test_target.csv", index_label="index")

    except Exception as error:
        os.makedirs(os.path.dirname(out_path))

        X_train.to_csv(out_path + "/training_feature.csv", index_label="index")
        y_train.to_csv(out_path + "/training_target.csv", index_label="index")
        X_test.to_csv(out_path + "/test_feature.csv", index_label="index")
        y_test.to_csv(out_path + "/test_target.csv", index_label="index")

    #    print(f"Error message: %s" %error)
    #    print("Error while saving training and test data!")

    print("")
    print(f"X_train is loaded successfully at %s" %
          (out_path + "training_feature.csv"))
    print(f"y_train is loaded successfully at %s" %
          (out_path + "training_target.csv"))
    print(f"X_test is loaded successfully at %s" %
          (out_path + "test_feature.csv"))
    print(f"y_test is loaded successfully at %s" %
          (out_path + "test_target.csv"))


if __name__ == "__main__":
    main(opt['--input_path'], opt['--out_path'])
