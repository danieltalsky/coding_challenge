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

Below is a summary of `@TODO`'s in code:

`@TODO`'s in code represent things I could expand 
on with more time or a more production-like situation.

`@FIXME`'s in code represent things I would have
asked for clarification on, and picked a sane default.

### routes.py: main application

- **Important:** In Routes line #33 I have GitHub "language" and "tags" turned off since they soak up a lot of API calls.
  Just turn both variables to `True` to get the full language and tags list.  In real life this would almost certainly
  require an async call.

### adapters.py: adapter abstractions for specific APIs

- Use version information - I added a parameter for checking version, but didn't implement it
- This isn't the accurate way to check forks for bitbucket, fix if time: Didn't see an easy way to check for forks
- The API assumes it will get all its information as a single page.  This is true in all cases I used except
  the list of watchers in BitBucket.  Ordinarily I would add a paging mechanism.

### network.py: models all API calls and network handling in one place

- Right now all network errors stop the whole process, more sophisticated network handling would be better
- Store some state about retries, network state, etc.
- Implement a caching layer: Incredibly important in any real-life application.  Cache by URL, have some
  invalidation mechanism, and rely even on an older cache for network errors
- Handle network resilience, **incremental backoff**, some kind of async layer 
- NAIVELY ASSUMING 403's are rate limit errors
- DETECT 404's and throw specific error to handle in api output message

### organization.py: Object model for an organization

- It's only checking for GitHub's version of a valid organization name
- In a real life version I'd want to use something better than a regex compiled every time

### tests

- See unimplemented functions