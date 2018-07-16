#!/usr/bin/env python3
# znc-backup
# version: 0.1.0
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
        subprocess.call(['mkdir','log'])

    logging.config.dictConfig(lc.LOGGER_CONFIG)

    logger = logging.getLogger(__name__)
    logger.debug('Logger initialized.')

    return logger


def sendEmail(backupFile):

    host = config['smtp']['host']
    port = config['smtp']['port']
    username = config['smtp']['username']
    password = config['smtp']['password']

    toAddr = config['email']['to']
    fromAddr = config['email']['from']

    message = """
It's that time of week again.
Here's your weekly backup of your znc data on `Chell`.
    """

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Weekly ZNC Backup'
    msg['From'] = fromAddr
    msg['To'] = toAddr

    with open(backupFile, 'rb') as bf:
        msg.add_attachment(
            bf.read(), maintype="application",
            subtype="x-7z-compressed", filename=os.path.basename(backupFile)
            )


    logger.debug('Attempting to send mail...')
    with smtplib.SMTP_SSL(host, port) as s:
        s.login(username, password)
        s.send_message(msg)
    logger.debug('Mail sent.')

def main():

    global logger
    logger = startLogger()

    global config
    if not os.path.exists('config.json'):
        logger.warning('Configuration file doesn\'t exist.')
        config = setup.createConfig()

    with open('config.json', 'r') as f:
        config = json.load(f)

    path = os.getenv("HOME") + "/.znc"
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
    print(outFile)

    if not os.path.isdir(path):
        logger.error('Uh oh... check to make sure the path is right.')
        logger.error('`path`: {}'.format(path))
    else:
        cmd = []
        cmd.append("7z")
        cmd.append("a")
        cmd.append(outFile)
        cmd.append(path)
        try:
            subprocess.call(cmd)
        except Exception:
            logger.error('Something went wrong attemping to send email.')
            exit()

        sendEmail(outFile)


if __name__ == '__main__':
    main()
