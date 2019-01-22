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

def startLogger():
    if not os.path.isdir('log'):
        subprocess.call(['mkdir', 'log'])
    logging.config.dictConfig(lc.LOGGER_CONFIG)
    logger = logging.getLogger(__name__)
    logger.debug('Logger initialized.')
    return logger


class Emailer:
    def __init__(self, host=None, port=None, username=None,
                password=None, toAddr=None, fromAddr=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.toAddr = toAddr
        self.fromAddr = fromAddr

    def sendSuccessEmail(self, backupFile):
        message = """
It's that time of week again.
Here's your weekly backup of your znc data on `Chell`.
        """
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Weekly ZNC Backup'
        msg['From'] = self.fromAddr
        msg['To'] = self.toAddr
        with open(backupFile, 'rb') as bf:
            msg.add_attachment(
                bf.read(), maintype="application",
                subtype="x-7z-compressed", filename=os.path.basename(backupFile)
                )
        try:
            logger.debug('Attempting to send mail...')
            with smtplib.SMTP_SSL(self.host, self.port) as s:
                s.login(self.username, self.password)
                s.send_message(msg)
            logger.debug('Mail sent.')
        except Exception as e:
            logger.critical('Unable to send mail. Exception: {}'.format(e))

    def sendErrorEmail(self, e=None):
        message = """
Something went very wrong sending the backup email.\n\nError is:\n```\n
{e}\n```\n
"""

def main():
    global logger
    logger = startLogger()
    global config
    if not os.path.exists('config.json'):
        logger.warning('Configuration file doesn\'t exist.')
        setup.createConfig()
    with open('config.json', 'r') as f:
        config = json.load(f)
    path = os.getenv("HOME") + "/.znc"
    emailer = Emailer()
    emailer.host = config['smtp']['host']
    emailer.port = config['smtp']['port']
    emailer.username = config['smtp']['username']
    emailer.password = config['smtp']['password']
    emailer.toAddr = config['email']['to']
    emailer.fromAddr = config['email']['from']
    tempPath = os.getenv("HOME") + "/znc-backup-staging"
    timestamp = datetime.now().strftime("%d-%h-%y - %H-%M-%S")
    logger.debug('Checking if backup source location exists.')
    if not os.path.isdir(tempPath):
        logger.warning('Backup dir doesn\'t exist. Creating...')
        try:
            subprocess.call(['mkdir', '-p', tempPath])
            logger.debug('Backup dir created.')
            # createdBackupDir = True
        except Exception:
            logger.error('Something went wrong creating backup dir.')
            exit()
    else:
        logger.debug('Backup dir exists - skipping')
        # createdBackupDir = False
    filename = "znc - " + timestamp
    outFile = tempPath + "/" + filename + ".7z"
    logger.info(outFile)
    if not os.path.isdir(path):
        logger.error('Uh oh... check to make sure the path is right.')
        logger.error('`path`: {}'.format(path))
    else:
        cmd = ["7z", "a", outFile, path]
        try:
            subprocess.call(cmd)
        except Exception:
            logger.error('Something went wrong creating archive.')
            exit()
        emailer.sendSuccessEmail(outFile)


if __name__ == '__main__':
    main()
