"""
This module is used to define the maintenance tasks for the ITS
environment 

"""


from time import sleep

from celery.utils.log import get_task_logger

from app import app

from asyncjobs.managers.database_manager import DatabaseManager
from asyncjobs.managers.ftp_manager import FTPManager

logger = get_task_logger(__name__)
QUEUE = 'maintenance'

database_manager = DatabaseManager()
ftp_manager = FTPManager()
# log_manager = LogManager()


@app.task(name='tasks.maintenance.ftp_backup', queue=QUEUE)
def ftp_backup():
    """
    This function is used to backup the FTP folder by downloading all the
    files and folders to a local directory

    """

    ftp_manager.generate_ftp_backup()
    logger.info('FTP backup complete!')


@app.task(name='tasks.maintenance.database_backup', queue=QUEUE)
def database_backup():
    """
    This function is used to backup the database by creating a dump file
    and saving it to a local directory

    """
    database_manager.generate_backup()
    logger.info('Backup complete!')


@app.task(name='tasks.maintenance.compress_old_files', queue=QUEUE)
def compress_old_files():
    """
    This function is used to compress old files in the logs directory,
    backups directory, and other directories

    """
    database_manager.compress_old_files()
    ftp_manager.compress_old_backup_files()


@app.task(name='tasks.maintenance.local_store_cleanup', queue=QUEUE)
def local_store_cleanup():
    """
    This function is used to clean up the local store by removing old files,
    duplicates and tmp files.

    """

    logger.info('Cleaning up local store...')
    sleep(3)
    logger.info('Cleanup complete!')
