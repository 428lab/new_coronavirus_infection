#!/bin/bash
cd src
kaggle datasets download sudalairajkumar/novel-corona-virus-2019-dataset
rm -rf *.csv && unzip *.zip && rm -rf *.zip
rm -rf *.png

#python3 estimate_new_coronavirus_infection.py covid_19_data.csv
python3 estimate_new_coronavirus_infection.py "Japan"
python3 estimate_new_coronavirus_infection.py "Mainland China"
python3 estimate_new_coronavirus_infection.py "South Korea"
python3 estimate_new_coronavirus_infection.py "France"
python3 estimate_new_coronavirus_infection.py "Italy"
python3 estimate_new_coronavirus_infection.py "Germany"
python3 estimate_new_coronavirus_infection.py "UK"
python3 estimate_new_coronavirus_infection.py "Spain"
python3 estimate_new_coronavirus_infection.py "Italy"
python3 estimate_new_coronavirus_infection.py "US"
python3 estimate_new_coronavirus_infection.py "Iran"
python3 estimate_new_coronavirus_infection.py "Russia"
python3 estimate_new_coronavirus_infection.py "Canada"
python3 estimate_new_coronavirus_infection.py "Hong Kong"
cd ..

cd web
yarn install
yarn build
yarn generate

rm -rf /var/www/html/*
cp -r dist/* /var/www/html 
chown -R www-data:www-data /var/www/html

