# author: Group 24
# date: 2021-11-25

'''This script models for the Crime Vancouver

Usage: modelling.py --input_path=<input_path> --out_path=<out_path>

Options:
--input_path=<input_path>   Path to directory where the data are stored
--out_path=<out_path>       Path to directory where the results are stored
'''
import dataframe_image as dfi
from sklearn.metrics import classification_report
import warnings
import pickle
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, average_precision_score, balanced_accuracy_score
from sklearn.metrics import make_scorer
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    PolynomialFeatures,
    StandardScaler,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    ShuffleSplit,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.linear_model import LogisticRegression, Ridge, RidgeCV, RidgeClassifier
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.compose import ColumnTransformer, make_column_transformer
import random
import altair as alt
import pandas as pd
import numpy as np
from docopt import docopt
import os
from sklearn.model_selection import train_test_split
alt.data_transformers.enable('data_server')
alt.renderers.enable('mimetype')

opt = docopt(__doc__)


def main(input_path, out_path):

    if not os.path.exists(out_path):
        os.makedirs(os.path.dirname(out_path))

    # using the objects that are in the folder
    X_train = pd.read_csv(
        input_path + '/training_feature.csv', index_col="index")

    y_train = pd.read_csv(
        input_path + '/training_target.csv', index_col="index").loc[:, "TYPE"]

    X_test = pd.read_csv(
        input_path + '/test_feature.csv', index_col="index")
    y_test = pd.read_csv(input_path + '/test_target.csv',
                         index_col="index").loc[:, "TYPE"]

    file = open(input_path + '/preprocessor.p', 'rb')
    preprocessor = pickle.load(file)
    file.close()

    file = open(input_path + '/models.p', 'rb')
    models = pickle.load(file)
    file.close()

    # Cross validation
    # Exports the result into png file
    results_cv = cv_models(models, X_train, y_train,
                           preprocessor, cv=5)

    filename = 'models_results_cv.png'
    outfile = open(out_path + "/" + filename, 'wb')
    dfi.export(results_cv, outfile, table_conversion='matplotlib')

    # Hyperparameter tuning of the best model
    # Creates a pipeline of the best results
    best_results = best_LR_model(X_train, y_train, preprocessor)

    best_result_df = best_results["scores"]
    pipe_best = make_pipeline(preprocessor, best_results['best_model'])

    filename = 'best_LR_model.png'
    outfile = open(out_path + "/" + filename, 'wb')
    dfi.export(best_result_df, outfile,
               table_conversion="matplotlib")

    # Save pipe_best data
    try:
        filename = 'pipe_best.p'
        outfile = open(out_path + "/" + filename, 'wb')
        pickle.dump(pipe_best, outfile)
        outfile.close()

        print("")
        print(f"Best pipe is loaded successfully at %s" %
              (out_path + filename))

    except Exception as error:
        print(f"Error message: %s" % error)
        print("Error while saving pipe")

    classification_report = print_scores(
        pipe_best, X_train, y_train, X_test, y_test, preprocessor)['report']

    filename = 'classification_report.png'

    outfile = open(out_path + "/" + filename, 'wb')

    dfi.export(classification_report.T, outfile, table_conversion='matplotlib')

    # it is saved inside the function, just need to call

    print_confusion_matrix(pipe_best, X_train, y_train,
                           X_test, y_test, out_path)


# Adopted from lecture notes of DSCI 571 and DSCI 573

def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean and std of cross validation

    Parameters
    ----------
    model :
        scikit-learn model
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train :
        y in the training data

    Returns
    ----------
        pandas Series with mean scores from cross_validation
    """

    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" %
                       (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)


def cv_models(models, X_train, y_train, preprocessor, cv=5):
    """Returns CV f1 scores
    Parameters
    ----------
    models : list
        A list of sklearn classifiers
    X_train : numpy ndarray
        The feature matrix
    y_train : numpy ndarray
        The target labels
    cv : int, optional
        Number of folds, default 5

    Returns
    -------
    pandas DataFrame
        The results of cross validation for the given models
    """
    # X_train = pd.read_csv(
    #    '../data/processed/training_feature.csv', index_col="index")
    # y_train = pd.read_csv(
    #    '../data/processed/training_target.csv', index_col="index").loc[:, "TYPE"]

    #file = open('../data/processed/preprocessor.p', 'rb')
    #preprocessor = pickle.load(file)

    #file = open('../data/processed/models.p', 'rb')
    #models = pickle.load(file)

    print("")
    print("Start cross validation.")

    f1_scorer = make_scorer(f1_score, average='micro')

    scoring_metrics = {

        "f1": f1_scorer,
    }

    results = {}

    for name, model in models.items():

        print(f"running %s" % name)
        pipe = make_pipeline(preprocessor, model)

        results[name] = mean_std_cross_val_scores(
            pipe, X_train, y_train, cv=cv, return_train_score=True, scoring=scoring_metrics
        )

    results_df = pd.DataFrame(results)

    print("")
    print("Completed cross validation of different models.")

    return results_df


def best_LR_model(X_train, y_train, preprocessor):
    """
    Finds the best LR model based on C and weight class, based on f1 scorer

    Parameters
    ----------
    models : list
        A list of sklearn classifiers
    X_train : numpy ndarray
        The feature matrix


    Returns
    -------
    dictionary 
        dictionary with scores and best model with optimized hyperparameters
    """

    # X_train = pd.read_csv(
    #    '../data/processed/training_feature.csv', index_col="index")
    # y_train = pd.read_csv(
    #    '../data/processed/training_target.csv', index_col="index").loc[:, "TYPE"]

    # X_test = pd.read_csv(
    #    '../data/processed/test_feature.csv', index_col="index")
    # y_test = pd.read_csv('../data/processed/test_target.csv',
    #                     index_col="index").loc[:, "TYPE"]

    #file = open('../data/processed/preprocessor.p', 'rb')
    #preprocessor = pickle.load(file)

    print("")
    print("Start hyperparameter tuning")

    pipe = make_pipeline(preprocessor,
                         LogisticRegression(max_iter=2000,
                                            multi_class='ovr',))

    f1_scorer = make_scorer(f1_score, average='micro')

    scoring_metrics = {

        "f1": f1_scorer,
    }

    param_grid = {
        "logisticregression__C": [0.01, 0.1, 1, 10, 100],
        "logisticregression__class_weight": [None, "balanced"]
    }

    search = RandomizedSearchCV(
        pipe,
        param_grid,
        verbose=1,
        n_jobs=6,
        n_iter=10,
        return_train_score=True,
        scoring=make_scorer(f1_score, average='micro'),
        random_state=123,
    )
    search.fit(X_train, y_train)

    search_df = pd.DataFrame(search.cv_results_).loc[pd.DataFrame(search.cv_results_)['rank_test_score'] == 1, ["mean_test_score",
                                                                                                                "mean_train_score",
                                                                                                                "param_logisticregression__C",
                                                                                                                "param_logisticregression__class_weight"]].T

    search_df = search_df.rename(index={'param_logisticregression__C': "Best C",
                                        "param_logisticregression__class_weight": "Best weight"}, columns={2: 'value'})

    best_C = search.best_params_['logisticregression__C']
    best_weight = search.best_params_['logisticregression__class_weight']

    dict = {'scores': search_df,
            'best_model': LogisticRegression(max_iter=1000,
                                             multi_class='ovr',
                                             C=best_C,
                                             class_weight=best_weight)
            }

    print("")
    print("Completed hyperparameter tuning.")

    return dict


def print_scores(pipe, X_train, y_train, X_test, y_test, preprocessor):

    # X_train = pd.read_csv(
    #    '../data/processed/training_feature.csv', index_col="index")
    # y_train = pd.read_csv(
    #    '../data/processed/training_target.csv', index_col="index").loc[:, "TYPE"]

    # X_test = pd.read_csv(
    #    '../data/processed/test_feature.csv', index_col="index")
    # y_test = pd.read_csv('../data/processed/test_target.csv',
    #                     index_col="index").loc[:, "TYPE"]

    #file = open('../data/processed/preprocessor.p', 'rb')
    #preprocessor = pickle.load(file)

    #file = open('../results/pipe_best.p', 'rb')
    #pipe = pickle.load(file)

    print("Start printing the score of X_test prediction")

    warnings.filterwarnings("ignore")

    pipe.fit(X_train, y_train)

    out = pd.DataFrame(classification_report(y_test, pipe.predict(X_test),
                                             target_names=pipe.classes_,
                                             output_dict=True))

    y_preb_probs = pipe.predict_proba(X_test)
    roc = roc_auc_score(y_test, y_preb_probs,
                        average='weighted', multi_class='ovr')

    dict = {'report': out,
            'roc': roc}

    print("")
    print("Completed print scores of test data.")

    return dict


def print_confusion_matrix(pipe, X_train, y_train, X_test, y_test, out_path):

    # X_train = pd.read_csv(
    #    '../data/processed/training_feature.csv', index_col="index")
    # y_train = pd.read_csv(
    #    '../data/processed/training_target.csv', index_col="index").loc[:, "TYPE"]

    # X_test = pd.read_csv(
    #    '../data/processed/test_feature.csv', index_col="index")
    # y_test = pd.read_csv('../data/processed/test_target.csv',
    #                     index_col="index").loc[:, "TYPE"]

    #file = open('../data/processed/preprocessor.p', 'rb')
    #preprocessor = pickle.load(file)

    #file = open('../results/pipe_best.p', 'rb')
    #pipe = pickle.load(file)

    print("")
    print("Start printing the confusion matrix of X_test")

    pipe.fit(X_train, y_train)

    cm = ConfusionMatrixDisplay.from_estimator(
        pipe, X_test, y_test, values_format="d", display_labels=pipe.classes_,
        xticks_rotation=-40
    )
    cm.ax_.set_title("Confusion Matrix")
    cm.figure_.set_size_inches(30, 20)

    filename = 'confusion_matrix.png'

    outfile = open(out_path + "/" + filename, 'wb')

    cm.figure_.savefig(outfile)

    print("")
    print("Completed saving confusion matrix.")


if __name__ == "__main__":
    main(opt['--input_path'], opt['--out_path'])
