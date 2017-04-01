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

import unittest

from populator.destination.direct import DirectDestination

class TestDestination(unittest.TestCase):
    def test_direct_destination(self):
        dd = DirectDestination(
            db_name='test_db',
            host='localhost:27017',
            db_user='test_user',
            db_password='test_password',
            drop_db=True,
            use_ssl=True,
            db_restore_indexes=None
        )

        self.assertEqual(
            dd.get_restore_str(),
            'mongorestore --ssl --noIndexRestore -u test_user -p test_password --drop --db test_db %s'
        )
