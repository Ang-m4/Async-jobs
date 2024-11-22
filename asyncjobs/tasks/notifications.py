"""
This module contains the tasks for sending notifications to users.

"""

from time import sleep

from celery.utils.log import get_task_logger

from app import app

logger = get_task_logger(__name__)
QUEUE = 'notifications'


@app.task(name='tasks.notifications.send_verification_code', queue=QUEUE)
def send_verification_code(to: str, code: str):
    """
    This function is used to send a verification code to the user.

    """

    logger.info(f'Sending verification code... {code} -> {to}')
    sleep(3)
    logger.info('Verification code sent!')


@app.task(name='tasks.notifications.send_request_update_email', queue=QUEUE)
def send_request_update_email(to: str, approver: str, data: dict):
    """
    This function is used to send an email to the user requesting an update
    on their request.

    """

    logger.info('Sending request update email...')
    sleep(3)
    logger.info('Email sent!')


@app.task(name='tasks.notifications.send_request_upload_email', queue=QUEUE)
def send_request_upload_email(to: str, requester: str, data: dict):
    """
    This function is used to send an email to the user requesting an upload
    of a file.

    """

    logger.info('Sending request upload email...')
    sleep(3)
    logger.info('Email sent!')
