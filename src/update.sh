#!/bin/bash

mkdir -p ~/.kaggle
API_DATA="{\"username\":\"${API_NAME}\",\"key\":\"${API_KEY}\"}" && \
    echo ${API_DATA} > ~/.kaggle/kaggle.json && \
    chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset
rm -rf *.csv && unzip *.zip && rm -rf *.zip

rm *.png
python estimate_new_coronavirus_infection.py covid_19_data.csv