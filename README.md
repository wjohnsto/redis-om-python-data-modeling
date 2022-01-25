# redis-om-python-tasks

This repository contains an example of how to use [Redis OM Python](https://github.com/redis/redis-om-python) with FastAPI.

## Installing

You install this project with Poetry.

First, [install Poetry](https://python-poetry.org/docs/#installation). You can probably pip install it into your Python environment:

    $ pip install poetry

Then install the example app's dependencies:

    $ poetry install

## Running the Project

This project contains a FastAPI application (main.py). It uses Redis OM for Python to save and retrieve data from Redis.

### Environment Variables

This project expects you to set a `REDIS_OM_URL` environment variable, which should be the connection string to your Redis instance following the redis-py URL format:

    redis://[[username]:[password]]@localhost:6379/[database number]

To try the API, first, start the server:

    $ poetry run uvicorn main:app

Once it is running you can visit http://127.0.0.1:8000/docs to see the API documentation.


## About the project

- **main.py**: The FastAPI application entrypoint
- **api.py**: Contains the FastAPI API routes
- **generate.py**: Contains functionality for clearing and regenerating data on your Redis instance
- **models.py**: Contains the redis-om-python models
  - There is some additional code in the models to make things a little bit cleaner in the database
