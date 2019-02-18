#!/usr/bin/env bash

set -e
set -x

bash wait-for-it.sh --timeout=10 ${POSTGRES_HOST}:${POSTGRES_PORT}
bash wait-for-it.sh --timeout=10 ${API_HOST}:${API_PORT}

pytest tests/integration_tests --cov=./ --cov-config /src/tests/.coveragerc --cov-report term-missing -p no:warnings "$PYTEST_TAGS"
