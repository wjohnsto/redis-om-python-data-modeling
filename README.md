# redis-om-python-retail

This repository contains several example sub-projects:



1. Tthe `api` directory contains an example of how to use [Redis OM Python](https://github.com/redis/redis-om-python) with FastAPI.
1. The `one_to_one` directory contains a 1-to-1 data modeling example project.

## Installing

You install this project with Poetry.

First, [install Poetry](https://python-poetry.org/docs/#installation). You can probably pip install it into your Python environment:

    $ pip install poetry

Then install the example app's dependencies:

    $ poetry install

## Running the Projects

### Environment Variables

This project expects you to set a `REDIS_OM_URL` environment variable, which should be the connection string to your Redis instance following the redis-py URL format:

    redis://[[username]:[password]]@localhost:6379/[database number]

#### API

To try the API, first, start the server:

    $ poetry run uvicorn main:app --app-dir api

Once it is running you can visit http://127.0.0.1:8000/docs to see the API documentation.


### 1-to-1

To run the one-to-one "separate" example run:

    $ poetry run python ./one_to_one/separate.py

To run the one-to-one "embedded" example run:

    $ poetry run python ./one_to_one/embedded.py


## About the projects

### The API
- **main.py**: The FastAPI application entrypoint
- **api.py**: Contains the FastAPI API routes
- **generate.py**: Contains functionality for clearing and regenerating data on your Redis instance
- **models.py**: Contains the redis-om-python models
  - There is some additional code in the models to make things a little bit cleaner in the database
- **utils.py**: Contains utility functions

### One-to-One
- **separate.py**: A 1-to-1 data modeling example using separate models
- **embedded.py**: A 1-to-1 data modeling example using embedded models
- **utils.py**: Contains utility functions
