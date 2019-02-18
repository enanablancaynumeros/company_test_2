#!/usr/bin/env bash

set -e

: "${POSTGRES_HOST:?Need to set POSTGRES}"
: "${POSTGRES_PORT:?Need to set POSTGRES_PORT}"

bash wait-for-it.sh --timeout=10 ${POSTGRES_HOST}:${POSTGRES_PORT}

cd /src/api/weather_api

if [[ "$@" == *--migrations* ]]; then
    flask create_database_and_upgrade
elif [[ "$@" == *--api* ]]; then
    uwsgi --socket 0.0.0.0:${API_PORT} --yaml /src/api/uwsgi.yaml
fi
