# coding=utf-8
import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('lib'))
from populator.release import __author__, __version__

setup(
    name='mongo_populator',
    version=__version__,
    description='Ridiculously easy to use tool for populating Mongo databases',
    author=__author__,
    url='https://github.com/PaladinStudiosBVs',
    license='GPLv3',
    install_requires=['paramiko'],
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    scripts=[
        'bin/mongo_populator'
    ]
)
