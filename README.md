# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install and Run Locally:

### Use Conda:
```shell
conda env create -f environment.yml
source activate user-profiles
```
### Spin up the service
```shell
# start up local server
python -m run 
```
### Run tests
```shell
python -m pytest
```

## Install and Run With Docker:

Build container and install conda dependencies
```shell
docker-compose build
```
Run using gunicorn:
```shell
docker-compose up app
```
Run tests
```shell
docker-compose up test
```

### Making Requests
```
curl -i "http://127.0.0.1:5000/health-check"
```
```
curl -i "http://127.0.0.1:5000/organization/mailchimp"
```

## What'd I'd like to improve on...
