#!/usr/bin/python3
"""Installing Debian packages via GitHub releases."""

import shutil
import subprocess
import os

import click
import requests


class Config:
    """Store the configuration"""
    DOWNLOAD_DIR = os.path.expanduser("~") + '/.cache/debi/'


class Package:
    """Represents a package"""

    name = ''  ## package name
    owner = ''  ## GitHub repo name
    repo = ''  ## GitHub owner name
    version = ''
    beta = False  ## by default, we assume you want to download the none-beta version of the package
    file_path = ''

    def __init__(self, name, owner, repo, beta):
        self.name = name
        self.owner = owner
        self.repo = repo
        self.beta = beta
        self.file_name = name.lower().replace(' ', '_')

    def resolve_download_url(self):
        """Resolve the download url"""
        print('Finding the latest release for ' + self.owner + '/' + self.repo)
        latest_release = None

        res = requests.get('https://api.github.com/repos/' + self.owner + '/' +
                           self.repo + '/releases')

        if res.status_code != 200:
            raise Exception(
                str(res.status_code) + ' ' + res.json()['message'] + ': ' +
                self.owner + '/' + self.repo)

        releases = res.json()

        for release in releases:
            tag = release['tag_name']

            if 'beta' in tag:
                if self.beta is True:
                    latest_release = release
                    break
            else:
                latest_release = release
                break

        self.version = latest_release['tag_name']

        for assets in latest_release['assets']:
            if '.deb' in assets['name']:
                return assets['browser_download_url']

    def fetch(self):
        """Fetch the .deb file from GitHub."""
        download_url = self.resolve_download_url()

        print('Fetching ' + self.repo + ' ' + self.version)
        res = requests.get(download_url, stream=True)

        # Check if download dir exist
        if os.path.exists(Config.DOWNLOAD_DIR) is False:
            os.makedirs(Config.DOWNLOAD_DIR)

        self.file_path = Config.DOWNLOAD_DIR + self.file_name + '-' + self.version + '.deb'

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
        print('Successfully installed!')


@click.command()
@click.argument('owner')
@click.argument('repo')
@click.option(
    '--beta',
    default=False,
    is_flag=True,
    help="Install the beta version of the package")
def cli(owner, repo, beta):
    """Installing Debian packages via GitHub releases."""
    pkg = Package('Atom', owner, repo, beta)
    try:
        pkg.fetch()
        pkg.install()
    except Exception as message:
        print(message)
