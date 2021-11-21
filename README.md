# Crime prediction in Vancouver

- contributors: Francisco Mejia, Jasmine Ortega, Thomas Siu, Shi Yan Wang

This is the data analysis project of group 24 (Cohort 6, 2022) for DSCI 522 (Data Science workflows); a course in the Master of Data Science program at the University of British Columbia.

## Our Motivation

One of the famous science fictions *The Minority Report* plots the future world, where police utilize technology to predict and arrest criminals before the crime happens. Put aside the ethical debates of the arrestment, we believe it is still essential to identify and predict crimes with good purpose. For example, can we predict the kinds of crime would possibly happen, given a certain neighbourhood and time? Police would then be able to strengthen specific skillsets to cater such law-breaching activities. Also, local government officials could utilize the prediction to adjust related policies.

We are going to build a classification prediction model to predict the types of crimes that happens in Vancouver, based on the location and the time of the day. The data set that is used in the project is originated from the Vancouver Open Data Catalogue, which was extracted and modified by Wilian Osaku in July 2017. It is sourced from Kaggle and can be found [here](https://www.kaggle.com/wosaku/crime-in-vancouver). The data set represents the types of crime reported in different areas of Vancouver at a particular time from 2003 to 2017.

To construct a meaningful prediction model, we will address the association between various crime types and areas in Vancouver. We will also study the trends of the number of crimes committed over the years in order to adjust the model with better prediction capability.

## EDA and Analysis

Before we begin the analysis, we split the data into train data(80%) and test data(20%). We performed an initial EDA against the train data. In particular, we summarised the number of crimes committed by locations throughout the years in a table. We also identified the correlation chart of the data features with the crime types. Detailed EDA report that includes other EDA results can be found [here](src/eda.md).

After EDA, we will adopt the methodology in supervised machine learning for the prediction. Necessary data transformation will be applied based on the reults of initial data analysis. During EDA, we will revisit the scoring method to be used, as well as to decide if we are more concerned on False Positive error or False Negative error, which will determine on our identication of the suitable model. Then we will examine different machine learning models through techniques of cross validation. Models to be assessed will be Dummy Classifier, Decision Tree, K-nearest neighbours, and Logistic Regression. The process will be repeated with different hyperparameters so that we are able to gather enough statistics to identify the best performing model.

Once the prediction model is completed, we will publish an executive summary in HTML format to this repository that describes the results and implications. An detailed report in HTML and PDF format will also be published that includes necessary analysis results in the form of table and graphs.

## Usage

### Conda environment

To replicate the analysis and run the predictor, download the conda environment file to your computer [here](crime_predictor.yaml). Then create and activate the conda environment as follows:

```bash
conda env create -f crime_predictor.yaml
conda activate crime_predictor
```

### R

Download the latest version of R at `https://cran.r-project.org`. Follow the installer instructions.

### Kaggle API

In order to download the dataset from Kaggle, generate an API token by the following steps:

1. Sign up or login Kaggle at `https://www.kaggle.com`
2. Go to the `Account` tab of your user profile
3. Select `Create New API Token` under `API session`. This will trigger the download of kaggle.json.
4. Place the file in the necessary location, for example:
    - Mac: `~/.kaggle/kaggle.json`
    - Windows: `C:\Users\<Windows-username>\.kaggle\kaggle.json`

## Dependencies

In case of replicating the analysis without using `conda`, the following are the dependencies of the libraries:

- Python 3.9 and Python packages:
  - docopt=0.6.2
  - ipykernal
  - ipython=7.29.0
  - vega_datasets
  - altair_saver
  - matplotlib>=3.2.2
  - request>=2.24.0
  - scikit-learn>=1.0
  - pandas>=1.3.*
  - graphviz
  - python-graphviz
  - pip
  - rpy2
  - kaggle

- R version 4.1.1 and R packages:
  - knitr
  - tidyverse
  - ggthemes

## License

The data set used in this project `Crime in Vancouver` is made available under the Open Database License: <http://opendatacommons.org/licenses/odbl/1.0/>. Any rights in individual contents of the database are licensed under the Database Contents License: <http://opendatacommons.org/licenses/dbcl/1.0/>

## References

### Data set

Wilian Osaku. 2017 "Crime in Vancouver" <https://www.kaggle.com/wosaku/crime-in-vancouver>
