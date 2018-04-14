#!/usr/bin/env python3
# znc-backup
# This script compresses your znc data dir and emails it to you once a week.

import os
import json
import smtplib
import mimetypes
import subprocess

from datetime import datetime

from email.message import EmailMessage

with open('config.json', 'r') as f:
    config = json.load(f)

def sendEmail(backupFile):

    host = config['smtp']['host']
    port = config['smtp']['port']
    username = config['smtp']['username']
    password = config['smtp']['password']

    toAddr = config['email']['to']
    fromAddr = config['email']['from']

    message = """
It's that time of week again. Here's your weekly backup of your znc data on `Chell`.
    """

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Weekly ZNC Backup'
    msg['From'] = fromAddr
    msg['To'] = toAddr

    with open(backupFile, 'rb') as bf:
        msg.add_attachment(bf.read(), maintype="application",
            subtype="x-7z-compressed", filename=os.path.basename(backupFile))

    with smtplib.SMTP(host, port) as s:
        s.starttls()
        s.login(username, password)

        s.send_message(msg)


def main():

    path = os.getenv("HOME") + "/.znc"
    tempPath = os.getenv("HOME") + "/znc-backup-staging"
    timestamp = datetime.now().strftime("%d-%h-%y - %H-%M-%S")

    if not os.path.isdir(tempPath):
        print("Backup dir doesn't exist. Creating...")
        try:
            subprocess.call(['mkdir', '-p', tempPath])
            print("Backup dir created.")
            createdBackupDir = True
        except:
            print("Something went wrong creating backup dir.")
            exit()
    else:
        print("Backup dir exists.")
        print("Skipping.")
        createdBackupDir = False

    filename = "znc - " + timestamp
    outFile = tempPath + "/" + filename + ".7z"
    print(outFile)

    if not os.path.isdir(path):
        print('Uh oh... check to make sure the path is right.')
        print(f'`path`: {path}')
    else:
        cmd = []
        cmd.append("7z")
        cmd.append("a")
        cmd.append(outFile)
        cmd.append(path)
        try:
            subprocess.call(cmd)
        except:
            print("Something went wrong attempting to send email.")
            exit()

        sendEmail(outFile)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Something went terribly wrong:\n\t{e}')
