#!/usr/bin/env python
import setuptools
from ccptools import __version__


readme = None
try:
    with open('README.md') as f:
        readme = f.read()
except Exception as ex:
    pass


lic = None
try:
    with open('LICENSE') as f:
        lic = f.read()
except Exception as ex:
    pass


setuptools.setup(
    name='ccptools',
    version=__version__,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    description='The CCP Tools team utilities for date and/or time objects and values and messing with types.',
    long_description_content_type='text/markdown',
    long_description=readme,
    license=lic,
    author='Thordur Matthiasson',
    author_email='thordurm@ccpgames.com',
    url='https://github.com/ccpgames/ccptools',
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=[]
)
