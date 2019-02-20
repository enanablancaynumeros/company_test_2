#!/usr/bin/env bash

set -e

: "${POSTGRES_HOST:?Need to set POSTGRES}"
: "${POSTGRES_PORT:?Need to set POSTGRES_PORT}"

bash wait-for-it.sh --timeout=10 ${POSTGRES_HOST}:${POSTGRES_PORT}



if [[ "$@" == *--migrations* ]]; then
    cd /src/
    python -c "from connectors.db_connection import create_db_if_not_exists;create_db_if_not_exists();"
    python -c "from alembic_scripts.utils import alembic_upgrade_head;alembic_upgrade_head();"
    python -c "from tasks.weather_etl import update_station_locations; update_station_locations.delay()"
elif [[ "$@" == *--api* ]]; then
    cd /src/api/weather_api
    uwsgi --socket 0.0.0.0:${API_PORT} --yaml /src/api/uwsgi.yaml
fi
