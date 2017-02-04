# coding=utf-8
import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('lib'))
from release import __author__, __version__

setup(
    name='mongo-populator',
    version=__version__,
    description='Ridiculously easy to use tool for populating Mongo databases',
    author=__author__,
    url='https://github.com/PaladinStudiosBVs/mongo-populator',
    license='GPLv3',
    install_requires=['boto3', 'paramiko', 'scp'],
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    scripts=[
        'bin/mongo-populator'
    ],
    test_suite='test.runner.run_all',
    tests_require=['nose', 'coverage', 'nosexcover']
)
