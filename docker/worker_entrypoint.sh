#!/usr/bin/env bash

set -e

bash wait-for-it.sh --timeout=10 ${RABBITMQ_HOST}:${RABBITMQ_PORT}
rm -f /src/celeryd.pid

if [[ "$@" == *--celerybeat* ]]; then
    celery -A workers_config.celery_beat beat --loglevel INFO --pidfile=/src/celeryd.pid
elif [[ "$@" == *--worker* ]]; then
    : "${WORKER_QUEUE:?Need to set WORKER_QUEUE when running a worker}"
    celery -A workers_config.celery_app worker --loglevel=INFO -Ofair -Q ${WORKER_QUEUE} -n ${WORKER_NAME}@%h
elif [[ "$@" == *--flower* ]]; then
    flower -A workers_config.celery_app --conf=/src/celery_workers/workers_config/flower_config.py
fi
