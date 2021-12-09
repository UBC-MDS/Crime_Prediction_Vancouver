# Copyright (c) 2021  Thomas Siu, Ramiro Francisco Mejia, Jasmine Ortega, Shi Yan Wang
# Distributed under the terms of the MIT License.

# authors: Thomas Siu, Ramiro Francisco Mejia, Jasmine Ortega, Shi Yan Wang
# last update: 9-Dec-2021

# Introduction: A special docker to render report on Mac M1 for project crime predictor in Vancouver
# Usage:
#    docker build -t crime_predictor_renderer .

# The docker file is build based on the base image from continuumio/miniconda3 
FROM continuumio/miniconda3 

# set the working directory of the docker environment
WORKDIR /home/crime_predictor

# essential components for docker environment
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    fonts-dejavu \
    make

# add conda-forge channel
RUN conda config --add channels conda-forge

# install mamba for package installations
RUN conda install mamba -n base -c conda-forge -y

# mamba installation for python packages
RUN mamba install --quiet --yes \
    'docopt=0.6.*' \
    'r-base=4.1.*'  \
    'r-rmarkdown' && \
    mamba clean --all -f -y
