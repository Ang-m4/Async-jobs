"""
This module contains utility functions for the asyncjobs package.

"""

import logging
import os
import shutil
import zipfile
from datetime import datetime

logger = logging.getLogger(__name__)


def compress_old_files(backup_folder):
    """
    Compresses old files in the specified backup folder into a ZIP archive.

    Args:
        backup_folder (str): The path to the backup folder.

    Raises:
        OSError: If there is an error creating the archive folder or
        compressing the files.

        Exception: If there is any other error during the compression process.

    Returns:
        None

    """

    current_time = datetime.now()
    archive_folder = f"{backup_folder}/backup_archive"

    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    try:
        folders_to_compress = []
        for folder in os.listdir(backup_folder):
            logger.info('Folder: %s', folder)
            folder_path = os.path.join(backup_folder, folder)
            if os.path.isdir(folder_path) and folder != 'backup_archive':
                logger.info('Folder: %s complies **', folder)
                folder_date = datetime.strptime(
                    folder, '%Y-%m-%d_%H-%M-%S')
                if folder_date < current_time:
                    logger.info('Folder: %s is older than %s',
                                folder, current_time)
                    folders_to_compress.append(folder_path)
                else:
                    logger.info('Folder: %s is newer than %s',
                                folder, current_time)

        # Compress the folders into a ZIP file
        if folders_to_compress:
            zip_file_path = os.path.join(
                archive_folder,
                f"backup_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.zip")
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for folder in folders_to_compress:
                    for root, _, files in os.walk(folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Maintain relative path inside the zip
                            arcname = os.path.relpath(
                                file_path, backup_folder)
                            zipf.write(file_path, arcname)
                            logger.info('Compressed: %s', file_path)

                    shutil.rmtree(folder)
                    logger.info('Removed folder: %s', folder)

            logger.info('Created ZIP file: %s', zip_file_path)

    except OSError as e:
        logger.error('Error compressing old files: %s', e)
