znc-backup
==========

``znc-backup`` is a script that creates a 7-zip archive of the ``$HOME/.znc``
directory and emails it to an email you provide during setup.

ZNC is an advanced IRC bouncer. <https://wiki.znc.in/ZNC>_.

Requirements
------------

This package requires python 3. 

Installation
------------

Clone the repo:

.. code-block::

    cd ~/
    git clone https://github.com/mattjorgs/znc-backup.git
    cd znc-backup/

Run the setup script, this will ask for things like your SMTP server host, port
(tls), username and password - pretty standard stuff:

.. code-block::

    python3 setup.py

You'll now find a ``config.json`` file in at the project root. Keep this secure,
since it contains a password in plain text.

It's a good idea to test the script to be sure everything runs properly. After
running the setup script, go ahead and give the main script a go:

.. code-block::

    python3 znc_backup.py

If everything goes well, you should have an archive waiting in your inbox! If
things did not go well, feel free to open an issue with any relevant information
and I'll do my best to help out.
