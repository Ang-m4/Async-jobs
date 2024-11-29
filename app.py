"""
This module is used to create a Celery instance and configure it
with the CeleryConfig class.
"""

from celery import Celery
from decouple import config

from asyncjobs.config import CeleryConfig

APP_NAME = "jobs"
BROKER_IP = config("REDIS_HOST")
BROKER_PORT = config("REDIS_PORT")
BROKER_DB = config("REDIS_TASKS_DB")
BACKEND_DB = config("REDIS_TASK_RESULTS_DB")


app = Celery(
    APP_NAME,
    broker=f"redis://{BROKER_IP}:{BROKER_PORT}/{BROKER_DB}",
    backend=f"redis://{BROKER_IP}:{BROKER_PORT}/{BACKEND_DB}",
)

app.config_from_object(CeleryConfig)

from asyncjobs.tasks import notifications
from asyncjobs.tasks import maintenance
