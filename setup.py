#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='debi',
    version='0.2.0',
    author='Maxime Le Conte des Floris',
    author_email='hello@mlcdf.com',
    description='Command-line interface for installing Debian packages via GitHub releases',
    py_modules=['debi'],
    install_requires=['Click', 'requests', 'logsymbols'],
    python_requires='>=3',
    entry_points='''
        [console_scripts]
        debi=debi:cli
    ''',
    license='MIT',
    url='https://github.com/mlcdf/debi',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System',
    ], )
