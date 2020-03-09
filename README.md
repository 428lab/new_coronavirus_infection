# new_coronavirus_infection

Estimation of new coronavirus infection people in Japan and China

# Usage

You need install docker machine in your PC.  

Setup to docker machine.

```
$ docker-compose build --no-cache
$ docker-compose up -d
$ docker-compose exec covid_19_seir_model bash
```

Run script at next command on the docker machine console.

```
python estimate_new_coronavirus_infection.py covid_19_data.csv
```

If you are a kaggle user, you can get the latest data with the API
```
API_NAME=xxxxx API_KEY=xxxxxx bash update.sh
```

This command output two *.png image files to current folder.
