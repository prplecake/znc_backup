#!/usr/bin/env python3
# znc-backup
# version: 0.2
# This script compresses your znc data dir and emails it to you once a week.
import os
import json
import logging
import logging.config
import smtplib
import subprocess

from datetime import datetime
from email.message import EmailMessage

import setup
import conf.logger_config as lc


def start_logger():
    if not os.path.isdir('log'):
        subprocess.call(['mkdir', 'log'])
    logging.config.dict_config(lc.LOGGER_CONFIG)
    logger = logging.get_logger(__name__)
    logger.debug('Logger initialized.')
    return logger


class Emailer:
    def __init__(self, host=None, port=None, username=None,
                 password=None, to_addr=None, from_addr=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.to_addr = to_addr
        self.from_addr = from_addr

    def send_success_email(self, backup_file):
        message = """
It's that time of week again.
Here's your weekly backup of your znc data on `Chell`.
        """
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Weekly ZNC Backup'
        msg['From'] = self.fromAddr
        msg['To'] = self.toAddr
        with open(backup_file, 'rb') as bf:
            msg.add_attachment(
                bf.read(), maintype="application",
                subtype="x-7z-compressed", filename=os.path.basename(
                    backup_file))
        try:
            logger.info('Attempting to send mail...')
            with smtplib.SMTP_SSL(self.host, self.port) as s:
                s.login(self.username, self.password)
                s.send_message(msg)
            logger.info('Mail sent.')
        except Exception as e:
            self.send_error_email(e)
            logger.critical('Unable to send mail. Exception: {}'.format(e))

    def send_error_email(self, msg=None, err=None):
        message = """
Something went very wrong sending the backup email.\n\nError is:\n```\n
{err}\n```\n
{msg}
\n
Perhaps the logs have more information?\n
        """
        em = EmailMessage()
        em.set_content(message)
        em['Subject'] = 'ERROR: Weekly ZNC Backup'
        em['From'] = self.from_addr
        em['To'] = self.to_addr
        try:
            logger.info('Attempting to send error notification..')
            with smtplib.SMTP_SSL(self.host, self.port) as s:
                s.login(self.username, self.password)
                s.send_message(em)
            logger.info('Error notification sent.')
        except Exception as e:
            logger.critical('Unable to send mail. Exception: {}'.format(e))


def main():
    global logger
    logger = start_logger()
    global config
    if not os.path.exists('config.json'):
        logger.warning('Configuration file doesn\'t exist.')
        setup.create_config()
    with open('config.json', 'r') as f:
        config = json.load(f)
    path = os.getenv("HOME") + "/.znc"
    emailer = Emailer()
    emailer.host = config['smtp']['host']
    emailer.port = config['smtp']['port']
    emailer.username = config['smtp']['username']
    emailer.password = config['smtp']['password']
    emailer.to_addr = config['email']['to']
    emailer.from_addr = config['email']['from']
    temp_path = os.getenv("HOME") + "/znc-backup-staging"
    timestamp = datetime.now().strftime("%d-%h-%y - %H-%M-%S")
    logger.debug('Checking if backup source location exists.')
    if not os.path.isdir(temp_path):
        logger.warning('Backup dir doesn\'t exist. Creating...')
        try:
            subprocess.call(['mkdir', '-p', temp_path])
            logger.debug('Backup dir created.')
        except Exception:
            logger.error('Something went wrong creating backup dir.')
            exit()
    else:
        logger.debug('Backup dir exists - skipping')
    filename = "znc - " + timestamp
    out_file = temp_path + "/" + filename + ".7z"
    logger.info(out_file)
    if not os.path.isdir(path):
        logger.error('Uh oh... check to make sure the path is right.')
        logger.error('`path`: {}'.format(path))
    else:
        cmd = ["7z", "a", out_file, path]
        try:
            subprocess.call(cmd)
        except Exception:
            logger.error('Something went wrong creating archive.')
            exit()
        emailer.send_success_email(out_file)


if __name__ == '__main__':
    main()
