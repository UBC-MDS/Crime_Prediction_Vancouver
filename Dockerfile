# Copyright (c) 2021  Thomas Siu, Ramiro Francisco Mejia, Jasmine Ortega, Shi Yan Wang
# Distributed under the terms of the MIT License.

# authors: Thomas Siu, Ramiro Francisco Mejia, Jasmine Ortega, Shi Yan Wang
# last update: 9-Dec-2021

# Introduction: The docker runs the prediction of crimes in vancouver
# Note: For Mac M1 users two separate dockers are required. See README for details
# Usage:
# - Operating systems except Mac M1:
#    docker build -t crime_predictor .
# - Mac M1:
#    docker build --platform linux/amd64 -t crime_predictor .

# Base image adopted from Jupyter Development Team:
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook:latest
FROM $BASE_CONTAINER

USER root

# install pre-requisits for the base environment
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    fonts-dejavu && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


USER ${NB_UID}

# mamba installation for extra python and R packages
RUN mamba install --quiet --yes \
    'docopt=0.6.*' \
    'r-base=4.1.*' \
    'r-ggthemes' \
    'r-ggridges' \    
    'altair_saver=0.5.*' \
    'nodejs=14.17.*' \    
    'rpy2' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# further R packages installation for non M1 Mac users
RUN set -x && \
    arch=$(uname -m) && \
    if [ "${arch}" == "x86_64" ]; then \
    mamba install --quiet --yes \
    'r-rmarkdown' \
    'r-tidyverse' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"; \
    fi;

# extra python packages for rendering images from Pandas table
RUN pip3 install \
    'dataframe_image==0.1.1' \
    'lxml'

# set the working directory of the docker environment
WORKDIR "${HOME}"
