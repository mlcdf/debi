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
    beta = False
    arch = ''

    def __init__(self, owner, repo, beta, arch):
        self.owner = owner
        self.repo = repo
        self.beta = beta
        self.arch = arch


class Release:
    """Represents a release"""
    package = None
    version = ''
    download_url = ''
    local_path = ''
    size = 0

    def __init__(self, package, version, download_url, size):
        self.package = package
        self.version = version
        self.download_url = download_url
        self.local_path = Config.DOWNLOAD_DIR + package.repo.lower().replace(' ', '-') + \
            '-' + version + '.deb'
        self.size = size


def resolve_latest_release(pkg):
    """Resolve the latest release"""
    latest_release = None

    res = requests.get('https://api.github.com/repos/' + pkg.owner + '/' +
                       pkg.repo + '/releases')

    if res.status_code != 200:
        raise Exception(logsymbols.error + ' ' +
                        str(res.status_code) + ' ' + res.json()['message'] + ': ' +
                        pkg.owner + '/' + pkg.repo)

    releases = res.json()

    for release in releases:
        tag = release['tag_name']
        latest_release = release

        if 'beta' in tag:
            if pkg.beta is True:
                break
        else:
            break

    for assets in latest_release['assets']:
        if '.deb' in assets['name'] and (
                (pkg.arch == '64' and '64' in assets['name']) or
                (pkg.arch == '32' and '64' not in assets['name'])):
            return Release(pkg, latest_release['tag_name'], assets['browser_download_url'], assets['size'])

    raise Exception(
        logsymbols.error + ' This repository does not provide a Debian package.')


def is_in_cache(release):
    """Check if the given release has already been cached."""
    return os.path.isfile(release.local_path) and os.path.getsize(release.local_path) == release.size


def fetch(release):
    """Fetch the .deb file from GitHub."""
    res = requests.get(release.download_url, stream=True)

    # Check if download dir exist
    if os.path.exists(Config.DOWNLOAD_DIR) is False:
        os.makedirs(Config.DOWNLOAD_DIR)

    with open(release.local_path, 'wb') as file:
        shutil.copyfileobj(res.raw, file)


def install(release):
    """Install the package."""
    process = subprocess.Popen(
        'sudo dpkg -i ' + release.local_path,
        stdout=subprocess.PIPE,
        shell=True)
    (output, err) = process.communicate()
    process.wait()


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

    arch = '32' if thirtytwo else '64'
    pkg = Package(owner, repo, beta, arch)
    try:
        click.echo('Finding the latest release for ' +
                   pkg.owner + '/' + pkg.repo)
        release = resolve_latest_release(pkg)

        if is_in_cache(release):
            click.echo('Fetching from cache')
        else:
            click.echo('Fetching ' + release.download_url)
            fetch(release)

        click.echo('Installing ' + release.package.repo +
                   ' ' + release.version)
        install(release)
        click.echo(logsymbols.success + ' Successfully installed!')
        exit(0)
    except Exception as message:
        print(message)
        exit(1)
