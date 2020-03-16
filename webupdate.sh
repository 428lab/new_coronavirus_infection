#!/bin/bash
cd src
kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset
rm -rf *.csv && unzip *.zip && rm -rf *.zip
rm -rf *.png

#python3 estimate_new_coronavirus_infection.py covid_19_data.csv
python3 estimate_new_coronavirus_infection.py Japan
cd ..

cd web
yarn install
yarn build
yarn generate

rm -rf /var/www/html/*
cp -r dist/* /var/www/html 
chown -R www-data:www-data /var/www/html

