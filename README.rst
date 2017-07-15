debi: Debian Package Installer (via GitHub releases)
===================================================

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
      --beta  Install the beta version of the package
      --help  Show this message and exit.

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
    

License
-----

MIT

