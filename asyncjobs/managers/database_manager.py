from ctypes import cast
from pymongo import MongoClient
from decouple import config
import logging
from datetime import datetime, timedelta
import json
from bson import json_util
import os
from asyncjobs.managers import util

logger = logging.getLogger(__name__)


class DatabaseManager():
    CENTRAL_DB_HOST = config("CENTRAL_DB_HOST")
    CENTRAL_DB_PORT = config("CENTRAL_DB_PORT")
    CENTRAL_DB_NAME = config("CENTRAL_DB_NAME")
    CENTRAL_DB_USER = config("CENTRAL_DB_USER")
    CENTRAL_DB_PASS = config("CENTRAL_DB_PASS")
    CENTRAL_DB_AUTH_SOURCE = config("CENTRAL_DB_AUTH_SOURCE")
    collections = [
        'User',
        'Role',
        'Bus',
        'Concessionaire',
        'Request',
        'VerificationCode'
    ]

    def __init__(self):
        try:
            self.client = MongoClient(
                self.CENTRAL_DB_HOST,
                int(self.CENTRAL_DB_PORT),
                username=self.CENTRAL_DB_USER,
                password=self.CENTRAL_DB_PASS,
                authSource=self.CENTRAL_DB_AUTH_SOURCE
            )
            self.db = self.client[self.CENTRAL_DB_NAME]
        except Exception as e:
            logger.error('Error connecting to the database: %s', e)

    def generate_backup(self):
        """
        This function is used to generate a backup file of each collection
        in the database, organized by date and time.

        """

        time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = f'{config("BACKUP_FOLDER")}/database/{time_str}/'

        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        for collection in self.collections:
            try:
                collection_data = self.db[collection].find()
                with open(f'{backup_path}{collection}.json', 'w') as f:
                    json.dump(list(collection_data), f,
                              default=json_util.default)

            except Exception as e:
                logger.error(
                    'Error getting data from collection %s: %s', collection, e)
                continue

            logger.info('Backup generated successfully!')

    def compress_old_files(self):
        """
        This function is used to compress old backup files to save space.
        """

        backup_folder = f"{config('BACKUP_FOLDER')}/database"
        util.compress_old_files(backup_folder)
