from setuptools import setup

setup(
    name='debi',
    version='0.1.0.dev1',
    author='Maxime Le Conte des Floris',
    author_email='hello@mlcdf.com',
    description=
    'A command-line interface for installing Debian packages via GitHub releases',
    py_modules=['debi'],
    install_requires=['Click', 'requests'],
    python_requires='>=3',
    entry_points='''
        [console_scripts]
        debi=debi:cli
    ''',
    license='MIT',
    url='https://github.com/mlcdf/debi',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ], )
