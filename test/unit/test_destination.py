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

from unit.mock import (
    SCPClientMock,
    SSHClientMock
)

from populator.destination.direct import DirectDestination
from populator.destination.ssh import SSHDestination


class TestDestination(unittest.TestCase):
    def test_direct_destination(self):
        dd = DirectDestination(
            db_name='test_db',
            db_host='localhost:27017',
            db_user='test_user',
            db_password='test_password',
            db_auth='admin',
            drop_db=True,
            direct_use_ssl=True,
            db_restore_indexes=None
        )

        self.assertEqual(
            dd.get_restore_str(),
            'mongorestore -u test_user -p test_password --db test_db --ssl -h localhost:27017 --authenticationDatabase admin --noIndexRestore --drop %s'
        )

    def test_ssh_destination(self):
        sshd = SSHDestination(
            db_name='test_db',
            db_user='test_user',
            ssh_host='127.0.0.1',
            ssh_user='ssh_user',
            ssh_client=SSHClientMock(),
            scp_client=SCPClientMock()
        )

        sshd._populate()

