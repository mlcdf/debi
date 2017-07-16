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

    owner = ''  #  GitHub repo name
    repo = ''  # GitHub owner name
    version = ''
    file_path = ''
    beta = False
    thirtytwo = False

    def __init__(self, owner, repo, beta, thirtytwo):
        self.owner = owner
        self.repo = repo
        self.beta = beta
        self.file_name = owner.lower().replace(' ', '_')
        self.thirtytwo = thirtytwo

    def resolve_download_url(self):
        """Resolve the download url"""
        print('Finding the latest release for ' + self.owner + '/' + self.repo)
        latest_release = None

        res = requests.get('https://api.github.com/repos/' + self.owner + '/' +
                           self.repo + '/releases')

        if res.status_code != 200:
            raise Exception(logsymbols.error + ' ' +
                            str(res.status_code) + ' ' + res.json()['message'] + ': ' +
                            self.owner + '/' + self.repo)

        releases = res.json()

        for release in releases:
            tag = release['tag_name']
            latest_release = release

            if 'beta' in tag:
                if self.beta is True:
                    break
            else:
                break

        self.version = latest_release['tag_name']

        for assets in latest_release['assets']:
            if '.deb' in assets['name'] and (
                    (self.thirtytwo is False and '64' in assets['name']) or
                    (self.thirtytwo is True and '64' not in assets['name'])):
                return assets['browser_download_url']

        raise Exception(
            logsymbols.error + ' This repository does not provide a Debian package.')

    def fetch(self):
        """Fetch the .deb file from GitHub."""
        download_url = self.resolve_download_url()

        print('Fetching ' + download_url)
        res = requests.get(download_url, stream=True)

        # Check if download dir exist
        if os.path.exists(Config.DOWNLOAD_DIR) is False:
            os.makedirs(Config.DOWNLOAD_DIR)

        self.file_path = Config.DOWNLOAD_DIR + \
            self.file_name + '-' + self.version + '.deb'

        with open(self.file_path, 'wb') as file:
            shutil.copyfileobj(res.raw, file)

    def install(self):
        """Install the package."""
        print('Installing ' + self.repo + ' ' + self.version)
        process = subprocess.Popen(
            'sudo dpkg -i ' + self.file_path,
            stdout=subprocess.PIPE,
            shell=True)
        (output, err) = process.communicate()
        process.wait()
        print(logsymbols.success + ' Successfully installed!')


@click.command()
@click.argument('owner')
@click.argument('repo')
@click.option(
    '--beta',
    default=False,  #  by default, we assume you want to install the none-beta version
    is_flag=True,
    help="Install the beta version of the package")
@click.option(
    '--thirtytwo',
    default=False,  #  by default, we assume you want to install 64-bits version
    is_flag=True,
    help="Install the 32-bits version (instead of the 64-bits)")
def cli(owner, repo, beta, thirtytwo):
    """Installing Debian packages via GitHub releases."""
    pkg = Package(owner, repo, beta, thirtytwo)
    try:
        pkg.fetch()
        pkg.install()
        exit(0)
    except Exception as message:
        print(message)
        exit(1)
