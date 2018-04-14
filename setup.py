import os
import json

def createConfig(file='config.json'):
    if input("Create config now? (Y/n) ") in ['y', 'Y']:
        config = {'smtp': {}, 'email': {}}
        config['smtp']['host'] = str(input("Your SMTP Host: "))
        config['smtp']['port'] = int(input("SMTP port (TLS): "))
        config['smtp']['username'] = str(input("SMTP username: "))
        config['smtp']['password'] = str(input("SMTP password: "))
        config['email']['from'] = str(input("Sender's email address: "))
        config['email']['to'] = str(input("Recipient's email address: "))
        dump = json.dumps(config, indent=4)
        with open('config.json', 'w') as cf:
            json.dump(config, cf, indent=4)
    else:
        print("You chose not to create config now.")
        exit()

def main():
    print("""
Welcome to the znc-backup script. Very simply, this script creates a 7zip
archive of $HOME/.znc and emails you the archive. This script simply creates
the configuration file.
    """)

    if os.path.exists('config.json'):
        if input("The configuration file already exists. Would you like to overwrite it? (Y/n) ") not in ['y', 'Y']:
            print("Exiting.")
            exit()
        else:
            createConfig()
    else:
        createConfig()

if __name__ == '__main__':
    main()
