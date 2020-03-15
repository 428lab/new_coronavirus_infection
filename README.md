# new_coronavirus_infection

Estimation of new coronavirus infection people in Japan and China

# Usage

You need install docker machine in your PC.  

## Setup to docker machine.

The following steps are for starting Docker.

```
$ docker-compose build --no-cache
$ docker-compose up -d
$ docker-compose exec covid_19_seir_model bash
```

Run script at next command on the docker machine console.

```
python estimate_new_coronavirus_infection.py [country_name]
```

## Setup Environment

If you are a kaggle user, you can get the latest data with the API.

Copy .env.sample to .env.

```
$ cp .env.sample .env
```

Set API_NAME and API_KEY in `.env` file.

```
API_NAME=[KAGGLE_USER_NAME]
API_KEY=[KAGGLE_USER_KEY]
```

Again, set up docker.  

```
$ docker-compose down
$ docker-compose build --no-cache
$ docker-compose up -d
$ docker-compose exec covid_19_seir_model bash
```

Enter sh in the container.

```
$ bash update.sh
$ python estimate_new_coronavirus_infection.py [country_name]
```

This command output two *.png image files to current folder.
