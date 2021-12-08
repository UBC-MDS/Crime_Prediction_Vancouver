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
    'pandas' \
    'docopt' \
    'altair_saver=0.5.*' \
    'scikit-learn=1.0.*'   \    
    'r-base=4.1.*'  \
    'r-rmarkdown' \
    'nodejs=14.17.*' && \
    #   'pandoc=1.19.*'
    #   'rpy2' && \
    mamba clean --all -f -y

# extra installation for python packages using conda
RUN conda install -c conda-forge -y \
    'altair_saver=0.5.*'

# extra installation for python packages using pip
RUN pip3 install \
    'dataframe_image==0.1.1' \
    'lxml==4.6.*' 

#RUN Rscript -e "install.packages('rmarkdown', dependencies=TRUE, repos='http://cran.r-project.org')"

#RUN apt-get update --yes && \
#    apt-get install --yes --no-install-recommends \
#   r-base \
