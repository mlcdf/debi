debi: Debian Package Installer (via GitHub releases)
====================================================

.. image:: https://img.shields.io/pypi/v/debi.svg
    :target: https://pypi.python.org/pypi/debi

.. image:: https://img.shields.io/pypi/l/debi.svg
    :target: https://pypi.python.org/pypi/debi

.. image:: https://img.shields.io/pypi/wheel/debi.svg
    :target: https://pypi.python.org/pypi/debi

.. image:: https://img.shields.io/pypi/pyversions/debi.svg
    :target: https://pypi.python.org/pypi/debi

---------------

A command-line interface for installing Debian packages via GitHub releases.

Install
-------

::

    $ pip install debi


Usage
-----

::

    $ debi --help
    Usage: debi [OPTIONS] OWNER REPO

      Installing Debian packages via GitHub releases.

    Options:
      --beta        Install the beta version of the package
      --thirtytwo   Install the 32-bits version (instead of the 64-bits)
      --help        Show this message and exit.

::

    $ debi atom atom
    Finding the latest release for atom/atom
    Fetching atom v1.18.0
    Installing atom v1.18.0
    Successfully installed!

::

    $ debi atom atom --beta
    Finding the latest release for atom/atom
    Fetching atom v1.19.0-beta4
    Installing atom v1.19.0-beta4
    Successfully installed!

By default, ``debi`` will look for the 64-bits version (based on the name of the release). If you want to install the 32-bits version instead, add the flag ``--thirtytwo``.

::

    $ debi webtorrent webtorrent-desktop --thirtytwo
    Finding the latest release for webtorrent/webtorrent-desktop
    Fetching webtorrent-desktop v0.18.0
    Installing webtorrent-desktop v0.18.0
    Successfully installed!


License
-------

MIT

