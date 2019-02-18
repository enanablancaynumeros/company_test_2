from celery.schedules import crontab

from workers_config.celery_app import celery_app
from tasks.weather_etl import pull_weather_data, update_station_locations

celery_app.conf.beat_schedule = {
    "weather_etl": {
        "task": pull_weather_data.name,
        "schedule": crontab(hour=0, minute=30),
    }
}
