# coding=utf-8

# (c) 2017, Pedro Rodrigues <csixteen@gmail.com>
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

from datetime import datetime
import os

from populator import SSHPopulator, MongoConfig
from populator.errors import (
    MongoPopulatorRestoringRemoteDatabaseError,
    MongoPopulatorTemporaryRemoteDirectoryCreationError
)
from populator.destination import MongoDestination
from populator.utils.common import info


class SSHDestination(SSHPopulator, MongoDestination):
    def __init__(self, db_name=None, db_user=None, db_password=None, drop_db=True, db_restore_indexes=False,
                 ssh_host=None, ssh_user=None, ssh_password=None, ssh_key_file=None, source=None,
                 db_auth=None, db_host=None, scp_client=None, ssh_client=None):
        MongoDestination.__init__(
            self,
            db_name=db_name,
            host=db_host,
            auth_db=db_auth,
            db_user=db_user,
            db_password=db_password,
            drop_db=drop_db,
            db_restore_indexes=db_restore_indexes,
            source=source
        )

        if not scp_client or not ssh_client:
            SSHPopulator.__init__(
                self,
                ssh_host=ssh_host,
                ssh_user=ssh_user,
                ssh_password=ssh_password,
                ssh_key_file=ssh_key_file
            )
        else:
            self.scp_client = scp_client
            self.ssh_client = ssh_client

    def _populate(self):
        # We now have a directory with the database dump, so we must first
        # copy that to the destination
        self.prefix = self.prefix or datetime.now().strftime('%Y%m%d-%H%M%S')

        remote_dump_dir = os.path.join('/tmp/mongodumps', self.prefix)

        info(
            'Creating remote dump dir: {}'.format(remote_dump_dir),
            color='green'
        )

        _, stdout, _ = self.ssh_client.exec_command('mkdir -p {}'.format(remote_dump_dir))
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            info(
                'Temporary directory created in remote destination: {}'.format(remote_dump_dir),
                color='green'
            )
        else:
            raise MongoPopulatorTemporaryRemoteDirectoryCreationError()

        self.scp_client.put(self.dump_dir, remote_dump_dir, recursive=True)

        remote_dump_dir = os.path.join(remote_dump_dir, self.db_name)

        # Then we run mongorestore in the remote host
        restore_str = self.get_restore_str() % remote_dump_dir
        info(
            'Restoring remote database: {}'.format(restore_str),
            color='purple'
        )
        stdin, stdout, stderr = self.ssh_client.exec_command(restore_str)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            info(
                'Successfully restored remote database: {}'.format(restore_str),
                color='green'
            )
        else:
            raise MongoPopulatorRestoringRemoteDatabaseError()
