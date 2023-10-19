FROM ghcr.io/pandora-isomemo/base-image:latest

RUN adduser --system --disabled-password --home /home/inwt inwt
ENV HOME /home/inwt 
USER inwt

ADD . .

RUN Rscript -e "reticulate::install_miniconda(); \
                reticulate::use_miniconda('r-reticulate'); \
                reticulate::conda_install('r-reticulate', c('python-kaleido', 'packaging')); \
                reticulate::conda_install('r-reticulate', 'plotly', channel = 'plotly'); \
                reticulate::use_miniconda('r-reticulate')" \
    && installPackage MpiIsoApp \
    && installPackage
# run app on container start
CMD ["R", "-e", "shiny::runApp('/app', host = '0.0.0.0', port = 3838)"]
    
    
## Base image https://hub.docker.com/u/rocker/
#FROM rocker/shiny:latest
#FROM --platform=linux/amd64 maven:3.6-jdk-8-slim

#FROM rocker/r-base:latest

## system libraries of general use
## install debian packages
#RUN apt-get update -qq && apt-get -y --no-install-recommends install \
#    libxml2-dev \
#    libcairo2-dev \
#    libsqlite3-dev \
#    libmariadbd-dev \
#    libpq-dev \
#    libssh2-1-dev \
#    unixodbc-dev \
#    libcurl4-openssl-dev \
#    libssl-dev

## update system libraries
#RUN apt-get update && \
#    apt-get upgrade -y && \
#    apt-get clean

## copy necessary files

## renv.lock file --/Users/johann/Documents/CausalR/
#COPY CausalR/renv.lock ./renv.lock
## app folder
#COPY CausalR/ ./app

# install renv & restore packages
#RUN Rscript -e 'install.packages("renv")'
#RUN Rscript -e 'renv::restore()'

# expose port
#EXPOSE 3838

# run app on container start
#CMD ["R", "-e", "shiny::runApp('/app', host = '0.0.0.0', port = 3838)"]