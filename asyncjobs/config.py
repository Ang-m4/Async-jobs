"""
This module is used to define the Celery configuration and logger
for the application.
"""

from celery.schedules import crontab


class CeleryConfig():
    """
    This class is used to configure the Celery instance.

    """
    enable_utc = True
    timezone = 'America/Bogota'

    task_queues = {
        'maintenance': {
            'exchange': 'maintenance',
            'routing_key': 'maintenance',
        },
        'notifications': {
            'exchange': 'notifications',
            'routing_key': 'notifications',
        }
    }

    beat_schedule = {
        'backup-database-every-3-days': {
            'task': 'tasks.maintenance.database_backup',
            'schedule': crontab(day_of_month='*/3', hour=0, minute=0),
            'args': (),
        },

        'compress-old-files-every-month': {
            'task': 'tasks.maintenance.compress_old_files',
            'schedule': crontab(day_of_month=1, hour=0, minute=0),
            'args': (),
        },

        'backup-ftp-every-friday': {
            'task': 'tasks.maintenance.ftp_backup',
            'schedule': crontab(day_of_week=5, hour=0, minute=0),
            'args': (),
        },
    }

    task_default_queue = 'default'
    task_default_exchange = 'default'
    task_default_routing_key = 'default'
