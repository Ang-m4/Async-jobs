"""
This module is used to define the Celery configuration and logger
for the application.
"""


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

    # beat_schedule = {
    #     'backup-database-every-30-sec': {
    #         'task': 'tasks.maintenance.database_backup',
    #         'schedule': 30.0,
    #         'args': (),
    #     },

    #     'backup-ftp-every-1-min': {
    #         'task': 'tasks.maintenance.ftp_backup',
    #         'schedule': 60.0,
    #         'args': (),
    #     },

    #     'cleanup-ftp-every-2-min': {
    #         'task': 'tasks.maintenance.ftp_cleanup',
    #         'schedule': 120.0,
    #         'args': (),
    #     },

    #     'cleanup-logs-every-5-min': {
    #         'task': 'tasks.maintenance.logging_cleanup',
    #         'schedule': 300.0,
    #         'args': (),
    #     },

    # }
    
    task_default_queue = 'default'
    task_default_exchange = 'default'
    task_default_routing_key = 'default'
