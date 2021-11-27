# Crime Prediction in Vancouver

- contributors: Ramiro Francisco Mejia, Jasmine Ortega, Thomas Siu, Shi Yan Wang

This is the data analysis project of group 24 (Cohort 6, 2022) for DSCI 522 (Data Science workflows); a course in the Master of Data Science program at the University of British Columbia.

## Our Motivation

One of the famous science fictions *The Minority Report* plots the future world, where police utilize technology to predict and arrest criminals before the crime happens. Put aside the ethical debates of the arrestment, we believe it is still essential to identify and predict crimes with good purpose. For example, can we predict the kinds of crime would possibly happen, given a certain neighbourhood and time? Police would then be able to strengthen specific skillsets to cater such law-breaching activities. Also, local government officials could utilize the prediction to adjust related policies.

We are going to build a classification prediction model to predict the types of crimes that happens in Vancouver, based on the location and the time of the day. The data set that is used in the project is originated from The Vancouver Police Department (VPD), with the data set called `GEODASH OPEN DATA`. The data can be found [here](https://geodash.vpd.ca/opendata/). The data set represents the types of crime reported in different areas of Vancouver at a particular time from 2003 to 2021. Since the data is being updated by the VPD every week, we will cut-off the data up to 2020 December to ensure our analysis and model are reproducible.

To construct a meaningful prediction model, we will address the association between various crime types and areas in Vancouver. We will also study the trends of the number of crimes committed over the years in order to adjust the model with better prediction capability.

## EDA and Analysis

Before we begin the analysis, we split the data into train data(80%) and test data(20%). We performed an initial EDA against the train data. In particular, we summarised the number of crimes committed by locations throughout the years in a table. We also identified the correlation chart of the data features with the crime types. Detailed EDA report that includes other EDA results can be found [here](src/Crime_in_Vancouver_eda.ipynb).

After EDA, we will adopt the methodology in supervised machine learning for the prediction. Necessary data transformation will be applied based on the reults of initial data analysis. During EDA, we will revisit the scoring method to be used, as well as to decide if we are more concerned on False Positive error or False Negative error, which will determine on our identication of the suitable model. Then we will examine different machine learning models through techniques of cross validation. Models to be assessed will be Dummy Classifier, Decision Tree, K-nearest neighbours, and Logistic Regression. The process will be repeated with different hyperparameters so that we are able to gather enough statistics to identify the best performing model.

Once the prediction model is completed, we will publish an executive summary in HTML format to this repository that describes the results and implications. An detailed report in HTML and PDF format will also be published that includes necessary analysis results in the form of table and graphs.

## Usage

### Analysis execution

Execute the data analysis pipeline of the `Crime Vancouver` data set by running the following command in `terminal`:

```bash
sh pipeline.sh
```

### Conda environment

To replicate the analysis and run the predictor, download the conda environment file to your computer [here](crime_predictor.yaml). Then create and activate the conda environment as follows:

```bash
conda env create -f crime_predictor.yaml
conda activate crime_predictor
```

### R

Download the latest version of R at `https://cran.r-project.org`. Follow the installer instructions.



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
  - jupyter-book
  - dataframe-image

- R version 4.1.1 and R packages:
  - knitr
  - tidyverse
  - ggthemes

### Mac M1 specific considerations

  Due to the default installation version or R and RStudio is at arm64, it does not compatible with python rpy when executing R scripts together with Python in Jupyter notebook. To resolve, refer to the steps in this [issue](https://github.com/UBC-MDS/DSCI_522_Crime_Prediction_Vancouver/issues/12).

## Legal Disclaimer (Data set)

Refer to [here](data/raw/legal_disclaimer.txt) for the legal disclaimer of using the data set.

## References

Vancouver Police Department Open Data <https://geodash.vpd.ca/opendata/>
