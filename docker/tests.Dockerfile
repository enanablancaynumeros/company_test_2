FROM python:3.7.2-slim

COPY tests/requirements.txt /src/tests/requirements.txt
RUN pip install --no-cache-dir -r /src/tests/requirements.txt

COPY api /src/api
COPY celery_workers /src/celery_workers
COPY data_handlers /src/data_handlers
COPY tests /src/tests/

RUN pip install -e /src/data_handlers \
                -e /src/celery_workers \
                -e /src/api \
                -e /src/tests

COPY .flake8 /src
COPY docker/test_entrypoint.sh /entrypoint.sh
WORKDIR /src

ENTRYPOINT ["bash", "/entrypoint.sh"]
