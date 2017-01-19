# coding=utf-8

# (c) 2017, Pedro Rodrigues <pedro@paladinstudios.com>
#
# This file is part of Mongo Populator
#
# Mongo Populator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mongo Populator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mongo Populator.  If not, see <http://www.gnu.org/licenses/>.

########################################################

import os

import unittest


class CLITestCase(unittest.TestCase):
    @staticmethod
    def populate_environment_variables():
        os.environ['MONGO_POPULATOR_SOURCE_DB_NAME'] = 'test_db_1'
        os.environ['MONGO_POPULATOR_SOURCE_DB_USER'] = 'test_user_1'
        os.environ['MONGO_POPULATOR_SOURCE_DB_PASSWORD'] = 'test_password_1'
        os.environ['MONGO_POPULATOR_SOURCE_USE_LOCAL_DB'] = '0'
    
    @staticmethod
    def delete_environment_variables():
        try:
            del os.environ['MONGO_POPULATOR_SOURCE_DB_NAME']
            del os.environ['MONGO_POPULATOR_SOURCE_DB_USER']
            del os.environ['MONGO_POPULATOR_SOURCE_DB_PASSWORD']
            del os.environ['MONGO_POPULATOR_SOURCE_USE_LOCAL_DB']
        except KeyError:
            pass
