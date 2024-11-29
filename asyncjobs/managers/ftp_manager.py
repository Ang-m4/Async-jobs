import os
import ftplib
from decouple import config
from datetime import datetime
import logging

from asyncjobs.managers import util

logger = logging.getLogger(__name__)


class FTPManager():

    FTP_SERVER_HOST = config("FTP_SERVER_HOST")
    FTP_SERVER_USER = config("FTP_SERVER_USER")
    FTP_SERVER_PASS = config("FTP_SERVER_PASS")
    FTP_SERVER_ROOT = config("FTP_SERVER_ROOT")

    def generate_ftp_backup(self):
        """
        Connect to the FTP server and download the root directory to the local backup path.
        """
        time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_path = f"{config('BACKUP_FOLDER')}/ftp/{time_str}/"

        # Ensure the backup directory exists
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        try:
            with ftplib.FTP(self.FTP_SERVER_HOST, self.FTP_SERVER_USER, self.FTP_SERVER_PASS) as ftp:
                ftp.cwd(self.FTP_SERVER_ROOT)  # Change to the root directory
                self.download_directory(ftp, ".", backup_path)
                logger.info("FTP backup completed successfully.")
        except Exception as e:
            logger.error("Error downloading backup from FTP server: %s", e)

    def download_directory(self, ftp, remote_path, local_path):
        """
        Recursively download a directory from the FTP server.
        """
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        try:
            file_list = []
            # List directory contents
            ftp.retrlines(f"LIST {remote_path}", file_list.append)

            for entry in file_list:
                details = entry.split()
                name = details[-1]
                entry_type = details[0][0]

                remote_entry_path = os.path.join(
                    remote_path, name).replace("\\", "/")
                local_entry_path = os.path.join(local_path, name)

                if entry_type == "d":  # Directory
                    self.download_directory(
                        ftp, remote_entry_path, local_entry_path)
                else:  # File
                    with open(local_entry_path, "wb") as f:
                        ftp.retrbinary(f"RETR {remote_entry_path}", f.write)

        except Exception as e:
            logger.error("Error downloading directory from FTP: %s", e)

    def compress_old_backup_files(self):
        """
        This function is used to compress old backup files in the FTP backup directory.

        """
        backup_folder = f"{config('BACKUP_FOLDER')}/ftp"
        util.compress_old_files(backup_folder)
        
    