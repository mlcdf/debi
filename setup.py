#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name='debi',
    version=about['__version__'],
    author='Maxime Le Conte des Floris',
    author_email='hello@mlcdf.com',
    description='Command-line interface for installing Debian packages via GitHub releases',
    long_description=long_description,
    py_modules=['debi'],
    install_requires=['Click', 'requests', 'logsymbols'],
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
