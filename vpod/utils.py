from vpod import mail 
from flask_mail import Message
from datetime import datetime
from vpod.config import config

import os

def send_error_email(error_msg=None):
    file_name = 'error.log'
    today = datetime.today()
    today = today.strftime("%m/%d/%Y, %H:%M:%S")
    subject = 'VPOD Error - ' + today
    msg = Message(
                    sender=str(config.MAIL_DEFAULT_SENDER),
                    subject=subject,
                    recipients = config.SUPPORT
                )
    body = 'There was a server error when trying to perform an opperation on CDL VPOD. Please check app log to see error'
    if error_msg is not None: 
        body = body + str(error_msg)
    msg.body = body
    if file_name in os.listdir():
        file = open(file_name, 'rb')
        msg.attach(file_name, 'text/plain', file.read())
    mail.send(msg)