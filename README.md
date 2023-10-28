# Word Translation Microservice

This service may be run in Docker Compose or in non-Docker environment.

## Run in non-Docker Environment

Install Python 3.10, PostgreSQL

Setup database locally:

```
psql postgres
create database <database>;
create user <user> with password '<password>';
alter user <user> with superuser;
grant all privileges on database <database> to <user>;
```
Note: set environment variables in `.env` file should match `database`, `password`, used.

Run tests:

    make test

Run tests with coverage:

    make test-coverage

Run service:

    make run

Note: set environment variables using `.env` file.

## Run in Docker Compose

Install Docker Compose.

Build Docker image:

    docker compose build

Run tests:

    docker compose run --rm app pytest tests

Run service:

    docker compose up

Note: set environment variables using `.env` file.

## Service Environment Variables

`DATABASE_URL`
: Database url.

`GOOGLETRANS_SERVICE_URLS`
: Google translate url list.

`GOOGLETRANS_RAISE_EXCEPTION`
: Whether to raise exception if something will go wrong.

`GOOGLETRANS_PROXIES`
: Dictionary mapping protocol or protocol and host to the URL of the proxy.

`LOGGING_LEVEL`
: Logging level (One of: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
Default: `DEBUG`.

`NO_DOT_ENV`
: Disable reading of `.env` file (set to any non-empty string). Recommend to
set this in production environment or when using Docker Compose.

`SENTRY_DSN`
: Sentry DSN.

`SENTRY_ENVIRONMENT`
: Sentry environment name.


## Uvicorn Environment Variables

`UVICORN_HOST`
: Bind socket to this host. Default: `127.0.0.1`.

`UVICORN_PORT`
: Bind socket to this port. Default: `8000`.

See full list of settings: https://www.uvicorn.org/settings/

## Usage Example

Run service. Then run:

```
curl --request GET \
  --url 'http://127.0.0.1:8000/api/translations/word?target_lang=ru&word=challenge'
```
See full list of available [endpoints](ENDPOINTS.md).

## Pre-commit

Install pre-commit hooks:

    make pre-commit-install
