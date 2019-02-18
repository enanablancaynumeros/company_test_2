import os
from distutils.util import strtobool

from connectors.db_connection import db_config


rabbit_config = {
    "rabbit_mq_user": os.environ.get("RABBITMQ_USER"),
    "rabbit_mq_password": os.environ.get("RABBITMQ_PASSWORD"),
    "rabbit_mq_host": os.environ.get("RABBITMQ_HOST"),
    "rabbit_mq_port": os.environ.get("RABBITMQ_PORT"),
}
broker_url = "pyamqp://{rabbit_mq_user}:{rabbit_mq_password}@{rabbit_mq_host}:{rabbit_mq_port}/".format(
    **rabbit_config
)
broker_api = "http://{rabbit_mq_user}:{rabbit_mq_password}@{rabbit_mq_host}:15672/api/".format(
    **rabbit_config
)

broker_heartbeat = 120.0
accept_content = ["json"]
timezone = "UTC"
database_short_lived_sessions = True

result_backend = "db+postgresql://{user}:{password}@{address}/{name}".format(
    **db_config
)
result_serializer = "json"
result_expires = 0
result_persistent = True

worker_prefetch_multiplier = 1
worker_concurrency = int(os.environ.get("WORKER_CONCURRENCY", 1))
worker_max_tasks_per_child = 1
worker_send_task_events = True

task_send_sent_event = True
task_ignore_result = False
task_serializer = "json"
task_acks_late = True
task_always_eager = strtobool(os.environ.get("CELERY_EAGER", "False"))
task_eager_propagates = True  # if eager == True the this applies
task_track_started = True

include = ["tasks.weather_etl"]

task_routes = ([("tasks.weather_etl.*", {"queue": "default"})],)
