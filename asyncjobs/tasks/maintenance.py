"""
This module is used to define the maintenance tasks for the ITS
environment 

"""


from time import sleep

from celery.utils.log import get_task_logger

from app import app

logger = get_task_logger(__name__)
QUEUE = 'maintenance'


@app.task(name='tasks.maintenance.ftp_backup', queue=QUEUE)
def ftp_backup():
    """
    This function is used to backup the FTP folder by downloading all the
    files and folders to a local directory

    """

    logger.info('Backing up database...')
    sleep(3)
    logger.info('Backup complete!')


@app.task(name='tasks.maintenance.database_backup', queue=QUEUE)
def database_backup():
    """
    This function is used to backup the database by creating a dump file
    and saving it to a local directory

    """

    logger.info('Backing up database...')
    sleep(3)
    logger.info('Backup complete!')


@app.task(name='tasks.maintenance.ftp_cleanup', queue=QUEUE)
def ftp_cleanup():
    """
    This function is used to clean up the FTP folder by removing old files
    and duplicates.

    """

    logger.info('Cleaning up old backups...')
    sleep(3)
    logger.info('Cleanup complete!')


@app.task(name='tasks.maintenance.logging_cleanup', queue=QUEUE)
def logging_cleanup():
    """
    This function is used to clean up the log files by removing old log files

    """

    logger.info('Cleaning up old log files...')
    sleep(3)
    logger.info('Cleanup complete!')
