"""Tests for debi. Run via `pytest`"""
# pylint: disable=C0111

import delegator


def test_package_64bits():
    assert delegator.run('debi atom atom').return_code == 0


def test_package_64bits_beta():
    assert delegator.run('debi atom atom --beta').return_code == 0


def test_package_32bits():
    assert delegator.run(
        'debi webtorrent webtorrent-desktop').return_code == 0
