# redis-om-fastapi

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
