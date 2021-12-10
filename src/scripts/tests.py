import altair as alt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import random
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge, RidgeCV, RidgeClassifier
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    ShuffleSplit,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.svm import SVC, SVR
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, average_precision_score, balanced_accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import pickle
import warnings
from scipy.stats import lognorm, loguniform, randint
from sklearn.metrics import classification_report




def test_cv_models(models, X_train, y_train):
    '''
    test the output of the cross validation is in a correct format
    and if it evaluates all required models
    Parameters
    ----------
    models : dict
        a dictionary containing the models
    X_train: pd.dataframe
        A dataframe object of the features used in the model
    y_train: pd.dataframe.series
        A Series containing the target variable

    '''
    #The ouput is not a dataframe type
    assert(isinstance(cv_models(models, X_train, y_train), pd.DataFrame), "Error not a df type")
    #Test if all models are being trained
    assert(cv_models(models, X_train, y_train).shape[1]== 4, 'Not all the models are evaluated')


def test_bestLR(X_train, y_train, preprocessor):
    '''
    test if the output of the hyperparameter optimization of the logistic regression
    is correct
    Parameters
    ----------
    preprocessor : Pipeline object
        A preprocessor with the column transformations of our data
    X_train: pd.dataframe
        A dataframe object of the features used in the model
    y_train: pd.dataframe.series
        A Series containing the target variable

    '''
    # Testing if our output dictionary is complete
    assert(len(best_LR_model(X_train, y_train))== 2, 'Error dict is not complete')
    # testiing that we have a dictionary as an output
    assert(isinstance(best_LR_model(X_train, y_train), dict), "Error not a dict type")

def test_printscores(pipe, X_train, y_train, X_test, y_test, preprocessor):
    '''
    test if the output of the scores is correct

    Parameters
    ----------
    preprocessor : Pipeline object
        A preprocessor with the column transformations of our data
    pipe: Pipeline object
        A pipeline with the best model
    X_train: pd.dataframe
        A dataframe object of the features used in the model
    y_train: pd.dataframe.series
        A Series containing the target variable

    '''
    # Testing if our output dictionary is complete
    assert(len(print_scores(pipe, X_train, y_train, X_test, y_test, preprocessor))== 2, 'Error dict is not complete')
    # testiing that we have a dictionary as an output
    assert(isinstance(print_scores(pipe, X_train, y_train, X_test, y_test, preprocessor), dict), "Error not a dict type")