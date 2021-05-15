#!/usr/bin/env python3
# setup.py
# version: 0.1.0
# This script asks the user a few questions and saves the answers in
# JSON format.

import os
import json


def createConfig(file):
    """Creates the required configuration and saves it to a file.

    Keyword arguments:
    file -- the name of the configuration file.
    """

    if input("Create config now? (Y/n) ") in ['y', 'Y']:
        config = {'smtp': {}, 'email': {}}
        config['smtp']['host'] = str(input("Your SMTP Host: "))
        config['smtp']['port'] = int(input("SMTP port (TLS): "))
        config['smtp']['username'] = str(input("SMTP username: "))
        config['smtp']['password'] = str(input("SMTP password: "))
        config['email']['from'] = str(input("Sender's email address: "))
        config['email']['to'] = str(input("Recipient's email address: "))
        with open(file, 'w') as cf:
            json.dump(config, cf, indent=4)
    else:
        print("You chose not to create config now.")
        exit()


def main():
    global CONFIG_FILE
    CONFIG_FILE = 'config.json'

    print("""
Welcome to the znc-backup script. Very simply, this script creates a 7zip
archive of $HOME/.znc and emails you the archive. This script simply creates
the configuration file.
    """)

    if os.path.exists(CONFIG_FILE):
        if input("""
The configuration file already exists. Would you like to overwrite it? (Y/n)
""") not in ['y', 'Y']:
            print("Exiting.")
            exit()
        else:
            createConfig(CONFIG_FILE)
    else:
        createConfig(CONFIG_FILE)


if __name__ == '__main__':
    main()
