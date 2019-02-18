#!make

SHELL := /bin/bash

##############
# Docker commands for build, run, cleanups
##############

build:
	cd docker && \
	find . -type d -name __pycache__ -exec rm -r {} \+ && \
	docker-compose build

up: build
	cd docker && \
	docker-compose up -d --remove-orphans --scale celerybeat=0 --scale tests=0 # This will run everything but celerybeat and tests.

db_up:
	cd docker && docker-compose up --remove-orphans -d postgres

docker_cleanup:
	docker image prune --force && \
	docker volume prune --force

docker_full_cleanup: docker_down
	docker image prune -a --force && \
	docker volume prune --force

docker_down:
	cd docker && \
	docker-compose down -v --remove-orphans

restart: docker_down up


##############
# Testing commands
##############

tests: format static_analysis tests_no_slow

tests_migration_container: build
	cd docker && \
	docker-compose up --exit-code-from db_migrations db_migrations

unittests_locally: format pep8_checks db_up
	CELERY_EAGER=True $(shell cat docker/.env docker/.localenv | xargs) POSTGRES_HOST=localhost Apytest -xsvv --lf -p no:warnings --durations=3 tests/unit_tests && \
	find . -name \*.pyc -delete

integration_slow_tests_locally: format pep8_checks stub_dbs_up
	$(shell cat docker/.env docker/.env | xargs) CELERY_EAGER=True POSTGRES_HOST=localhost FLOWER_HOST=localhost pytest -m "slow" -xsvv --lf -p no:warnings tests/integration_tests && \
	find . -name \*.pyc -delete

##############
# Data migration commands and helpers
##############

alembic_new_migration_file: db_up
	cd api/weather_api && \
	$(shell cat docker/.env | xargs) POSTGRES_HOST=localhost flask create_database_and_upgrade && \
	$(shell cat docker/.env | xargs) POSTGRES_HOST=localhost flask alembic_autogenerate_revision

##############
# static code analysis
##############

format:
	black --skip-string-normalization .

pep8_checks:
	flake8

safety_check:
	safety check

static_analysis: pep8_checks format_check safety_check

format_check:
	black --skip-string-normalization --check .


##############
# Misc
##############

run_api_locally:
	cd api/weather_api && \
	$(shell cat docker/.env | xargs) RABBITMQ_HOST=0.0.0.0 POSTGRES_HOST=0.0.0.0 API_PORT=8008 flask run

ipython:
	$(shell cat docker/.env | xargs) POSTGRES_HOST=localhost ipython