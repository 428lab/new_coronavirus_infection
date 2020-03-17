#!/bin/bash

docker-compose build --no-cache
docker-compose up -d
docker-compose exec covid_19_seir_model bash update.sh
docker-compose exec covid_19_seir_model bash -c "echo \"{}\" > output.json"
docker-compose exec covid_19_seir_model bash generate.sh

docker-compose run web_build ash -c "cd /var/www && ash update.sh"

docker-compose down

rm -rf /var/www/html/*
cp -r web/dist/* /var/www/html 
chown -R www-data:www-data /var/www/html

