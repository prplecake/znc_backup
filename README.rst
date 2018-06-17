znc-backup
==========

``znc-backup`` is a script that creates a 7-zip archive of the ``$HOME/.znc``
directory and emails it to an email you provide during setup.

ZNC is an advanced IRC bouncer. https://wiki.znc.in/ZNC.

Requirements
------------

This package requires python 3. 

Installation
------------

Clone the repo::
    cd ~/
    git clone https://github.com/mattjorgs/znc-backup.git
    cd znc-backup/

Run the setup script, this will ask for things like your SMTP server host, port
(TLS), username and password - pretty standard stuff::

    ./setup.py

You'll now find a ``config.json`` file in at the project root. Keep this secure,
since it contains a password in plain text.

It's a good idea to test the script to be sure everything runs properly. After
running the setup script, go ahead and give the main script a go::

    ./znc_backup.py

If everything goes well, you should have an archive waiting in your inbox! If
things did not go well, feel free to open an issue with any relevant information
and I'll do my best to help out.

After you've determined the script is working properly, you might want to set
up crontab to do all the remembering for you. My crontab looks like this::

    */10 * * * *    /usr/bin/znc >/dev/null 2>&1
    0 4 * * 4   cd /home/matthewjorgensen/znc-backup; ./znc_backup.py >/dev/null 2>&1

The first line check to see if znc is running every ten minutes. The second line will run the script on Thursday at 0400.

License
-------

This project is licensed under the terms of the MIT license.
