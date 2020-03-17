#!/bin/bash

mkdir -p ~/.kaggle
API_DATA="{\"username\":\"${KAGGLE_USER_NAME}\",\"key\":\"${KAGGLE_API_KEY}\"}" && \
    echo ${API_DATA} > ~/.kaggle/kaggle.json && \
    chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset
rm -rf *.csv && unzip *.zip && rm -rf *.zip

rm -rf *.png
# python estimate_new_coronavirus_infection.py covid_19_data.csv
# bash generate.sh