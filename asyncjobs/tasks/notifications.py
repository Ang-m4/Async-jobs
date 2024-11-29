"""
This module contains the tasks for sending notifications to users.

"""

from time import sleep

from celery.utils.log import get_task_logger

from app import app
from asyncjobs.managers.email_manager import EmailNotificationManager

logger = get_task_logger(__name__)
QUEUE = 'notifications'

manager = EmailNotificationManager()

@app.task(name='tasks.notifications.send_verification_code', queue=QUEUE)
def send_verification_code(to: str, code: str):
    """
    This function is used to send a verification code to the user.

    """

    logger.info(f'Sending verification code... {code} -> {to}')
    manager.send_verification_email(to, code)
    logger.info('Verification code sent!')


@app.task(name='tasks.notifications.firmware_request_upload', queue=QUEUE)
def send_request_upload_email(to: list[str], data: dict):
    """
    This function is used to send an email to the user requesting an upload
    of a file.

    """

    logger.info('Sending firmware request upload email...')
    manager.send_firmware_request_email(to, data)
    logger.info('Email sent!')


@app.task(name='tasks.notifications.certificates_request_upload', queue=QUEUE)
def send_request_upload_email(to: list[str], data: dict):
    """
    This function is used to send an email to the user requesting an upload
    of a file.

    """

    logger.info('Sending certificates request upload email...')
    manager.send_certificates_request_email(to, data)
    logger.info('Email sent!')


# @app.task(name='tasks.notifications.send_new_user_created_email', queue=QUEUE)
# def send_new_user_created_email(to: list[str], data: dict):
#     """
#     This function is used to send an email to the user when their account
#     is created.

#     """

#     logger.info('Sending new user created email...')
#     for email in to:
#         logger.info('%s %s -> %s', data['username'], data['email'], email)
#     sleep(3)
#     logger.info('Email sent!')


# @app.task(name='tasks.notifications.send_request_update_email', queue=QUEUE)
# def send_request_update_email(to: str, approver: str, data: dict):
#     """
#     This function is used to send an email to the user requesting an update
#     on their request.

#     """

#     logger.info('Sending request update email...')
#     logger.info('%s -> %s', to, approver)

#     for key, value in data.items():
#         logger.info('%s: %s', key, value)

#     sleep(3)
#     logger.info('Email sent!')
