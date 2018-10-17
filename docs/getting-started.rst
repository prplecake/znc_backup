Getting Started
===============

Prerequisites
-------------

The following is required:

#. Python 3

Installation
------------

Clone the repo::
    
    cd ~/
    git clone https://github.com/mtthwjrgnsn/znc_backup.git
    cd znc_backup/

Run the setup script, this will ask for thins like your SMTP server host, port 
(TLS), username and password - pretty standard stuff::
    
    ./setup.py

You'll now find a ``config.json`` file at the project root. Keep this secure,
since it contains a password in plain text.

It's a good idea to test the script to be sure everything runs properly. After
running the setup script, go ahead and give the main script a go::

    ./znc_backup.py

If everything goes well, you should have an archive waiting in your inbox! If
something went wrong, feel free to open an issue with an relevant information
and I'll do my best to help out.

Scheduling
----------

After you've determined the script is working properly, you might want to set
up a crontab entry to do all the remembering for you. My crontab looks like
this::

    */10 * * * * /usr/bin/znc >/dev/null 2>&1
    0 4 * * 4 cd /home/matthewjorgensen/znc_backup; ,/znc_backup.py >/dev/null 2>&1

The first line checks to see in znc is running every ten minutes. The second
line will run the ``znc_backup.py`` script on Thursdays at 0400.