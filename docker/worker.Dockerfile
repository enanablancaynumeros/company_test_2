FROM python:3.6.8-slim

ENV PYTHONUNBUFFERED 1
RUN apt-get update --fix-missing --no-install-recommends && \
    apt-get upgrade -y && \
    apt-get install -y build-essential \
    python-dev git \
    libffi-dev libssl-dev libpq-dev \
    wget && \
    pip install -U --no-cache-dir pip setuptools ipython && \
    wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/bin/ && chmod +x /usr/bin/wait-for-it.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

COPY celery_workers/requirements.txt /src/celery_workers/requirements.txt
COPY data_handlers/requirements.txt /src/data_handlers/requirements.txt

RUN pip install --no-cache-dir -r /src/celery_workers/requirements.txt \
                --no-cache-dir -r /src/data_handlers/requirements.txt

COPY celery_workers /src/celery_workers
COPY data_handlers /src/data_handlers

RUN pip install -e /src/data_handlers \
                -e /src/celery_workers

COPY docker/worker_entrypoint.sh /entrypoint.sh
WORKDIR /src

ENTRYPOINT ["bash", "/entrypoint.sh"]
