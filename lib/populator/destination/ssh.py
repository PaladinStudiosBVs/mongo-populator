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

from datetime import datetime

from populator.utils.common import info, die
from populator import SSHPopulator, MongoConfig
from populator.destination import MongoDestination


class SSHDestination(SSHPopulator, MongoConfig, MongoDestination):
    def __init__(self, db_name=None, db_user=None, db_password=None, ssh_host=None, ssh_user=None, ssh_password=None,
                 ssh_key_file=None, source=None):
        MongoConfig.__init__(self, db_name, db_user=db_user, db_password=db_password)
        MongoDestination.__init__(self, source)
        SSHPopulator.__init__(
            self,
            ssh_host=ssh_host,
            ssh_user=ssh_user,
            ssh_password=ssh_password,
            ssh_key_file=ssh_key_file
        )
        
    def _populate(self):
        # We now have a directory with the database dump, so we must first
        # copy that to the destination
        remote_dump_dir = '/tmp/mongodumps/{}'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))
        _, stdout, _ = self.ssh_client.exec_command('mkdir -p {}'.format(remote_dump_dir))
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            info(
                'Temporary directory created in remote source: {}'.format(remote_dump_dir),
                color='green'
            )
        else:
            die('Problems creating temporary directory in remote source')
        
        self.scp_client.put(self.dump_dir, remote_dump_dir, recursive=True)
        # Then we run mongoresture in the remote host
        restore_str = self.get_restore_str() % \
                      '{}/{}'.format(remote_dump_dir, self.dump_dir.split('/')[-1])
        stdin, stdout, stderr = self.ssh_client.exec_command(
            restore_str
        )
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            info(
                'Successfully restored remote database: {}'.format(restore_str),
                color='green'
            )
        else:
            die('Problems restoring remote database ({})'.format(exit_status))
