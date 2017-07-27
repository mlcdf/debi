#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debi: Installing Debian packages via GitHub releases."""

import shutil
import subprocess
import os

import click
import requests
import logsymbols


class Config:
    """Store the configuration"""
    DOWNLOAD_DIR = os.path.expanduser('~') + '/.cache/debi/'


class Package:
    """Represents a package"""

    def __init__(self, owner, repo, beta, arch):
        """Initialize a package

        :param owner: GitHub owner name
        :param repo: GitHub repo name
        :param beta: beta flag
        :param arch: architecture, either '32' or '64'
        """
        self.owner = owner
        self.repo = repo
        self.beta = beta
        self.arch = arch

    def resolve_latest_release(self):
        """Resolve the latest release

        :return: Release
        """
        latest_release = None

        res = requests.get('https://api.github.com/repos/' + self.owner + '/' +
                           self.repo + '/releases')

        if res.status_code != 200:
            raise Exception(logsymbols.error + ' ' + str(res.status_code) + ' ' +
                            res.json()['message'] + ': ' + self.owner + '/' +
                            self.repo)

        releases = res.json()

        for release in releases:
            tag = release['tag_name']
            latest_release = release

            if 'beta' in tag:
                if self.beta is True:
                    break
            else:
                break

        for assets in latest_release['assets']:
            if '.deb' in assets['name'] and (
                (self.arch == '64' and '64' in assets['name']) or
                    (self.arch == '32' and '64' not in assets['name'])):
                return Release(self, latest_release['tag_name'],
                               assets['browser_download_url'], assets['size'])

        raise Exception(logsymbols.error +
                        ' This repository does not provide a Debian package.')


class Release:
    """Represents a release"""

    def __init__(self, package, version, download_url, size):
        """Initialize a release

        :param package: package Package
        :param version: version of the release
        :param download_url: url to download the release
        :param size: release size (in bit)
        """
        self.package = package
        self.version = version
        self.download_url = download_url
        self.local_path = Config.DOWNLOAD_DIR + package.repo.lower().replace(' ', '-') + \
            '-' + version + '.deb'
        self.size = size

    def is_in_cache(self):
        """Check if the release has already been cached.

        :return: True if valid release found it cache
        """
        return os.path.isfile(self.local_path) and os.path.getsize(
            self.local_path) == self.size

    def fetch(self):
        """Fetch the release from GitHub."""
        res = requests.get(self.download_url, stream=True)

        # Check if download dir exist
        if os.path.exists(Config.DOWNLOAD_DIR) is False:
            os.makedirs(Config.DOWNLOAD_DIR)

        with open(self.local_path, 'wb') as file:
            shutil.copyfileobj(res.raw, file)

    def install(self):
        """Install the release on the machine."""
        process = subprocess.Popen(
            'sudo dpkg -i ' + self.local_path,
            stdout=subprocess.PIPE,
            shell=True)
        (output, err) = process.communicate()
        process.wait()


@click.command()
@click.argument('owner')
@click.argument('repo')
@click.option(
    '--beta',
    default=False,
    is_flag=True,
    help="Install the beta version of the package")
@click.option(
    '--thirtytwo',
    default=False,
    is_flag=True,
    help="Install the 32-bits version (instead of the 64-bits)")
def cli(owner, repo, beta, thirtytwo):
    """Installing Debian packages via GitHub releases."""

    arch = '32' if thirtytwo else '64'
    pkg = Package(owner, repo, beta, arch)
    try:
        print('Finding the latest release for ' + pkg.owner + '/' +
              pkg.repo)
        release = pkg.resolve_latest_release()

        if release.is_in_cache():
            print('Retrieving from cache')
        else:
            print('Fetching ' + release.download_url)
            release.fetch()

        print('Installing ' + release.package.repo + ' ' +
              release.version)
        release.install()
        print(logsymbols.success + ' Successfully installed!')
        exit(0)
    except Exception as message:
        print(message)
        exit(1)
