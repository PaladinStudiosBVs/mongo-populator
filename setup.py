# coding=utf-8
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
from populator.release import __author__, __version__

from setuptools import setup, find_packages

setup(
    name='mongo_populator',
    version=__version__,
    description='Ridiculously easy to use tool for populating Mongo databases',
    author=__author__,
    url='https://github.com/PaladinStudiosBVs',
    license='GPLv3',
    install_requires=['paramiko'],
    scripts=[
        'bin/mongo_populator'
    ]
)
