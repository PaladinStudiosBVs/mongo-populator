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
from datetime import datetime

from populator import SSHPopulator, MongoConfig
from populator.source import MongoSource
from populator.utils.common import info, die


class SSHSource(SSHPopulator, MongoConfig, MongoSource):
    def __init__(self, db_name=None, db_user=None, db_password=None, ssh_host=None, ssh_user=None, ssh_password=None,
                 ssh_key_file=None, tmp_dir=None):
        """
        :type db_name: str
        :param db_name:
        :type ssh_host: str
        :param ssh_host:
        :type ssh_user: str
        :param ssh_user:
        :type ssh_password: str
        :param ssh_password:
        :type ssh_key_file: str
        :param ssh_key_file: Path to identity file
        :type tmp_dir: str
        :param tmp_dir:
        """
        MongoConfig.__init__(self, db_name, db_user=db_user, db_password=db_password)
        MongoSource.__init__(self, tmp_dir=tmp_dir)
        SSHPopulator.__init__(
            self,
            ssh_host=ssh_host,
            ssh_user=ssh_user,
            ssh_password=ssh_password,
            ssh_key_file=ssh_key_file
        )
        
    def get_dump_dir(self):
        """
        :rtype: str
        :return:
        """
        # We first create a dump in the remote DB
        prefix = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        # mongodump creates a directory named after the database, se we
        # exclude the db_name from the remote dump directory. It will be
        # created implicitly.
        remote_dump_dir = os.path.join('/tmp/mongodumps', prefix)
        _, stdout, _ = self.ssh_client.exec_command('mkdir -p {}'.format(remote_dump_dir))
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            info(
                'Temporary directory created in remote source: {}'.format(remote_dump_dir),
                color='green'
            )
        else:
            die('Problems creating temporary directory in remote source')
        
        # Then we run mongodump in the remote host
        dump_str = self.get_dump_str() % remote_dump_dir
        stdin, stdout, stderr = self.ssh_client.exec_command(
            dump_str
        )
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            info(
                'Created a dump in the remote source: {}'.format(dump_str),
                color='green'
            )
        else:
            die('Problems creating a dump in the remote source')
        
        # Now we need to add the db_name to the remote_dump_dir
        remote_dump_dir = os.path.join(remote_dump_dir, self.db_name)
        
        # Create the local dump dir
        tmpdir = os.path.join(self.tmp_dir, prefix)
        info('Creating local dump dir: {}'.format(tmpdir))
        os.makedirs(tmpdir)
        self.scp_client.get(remote_dump_dir, tmpdir, recursive=True)
        tmpdir = os.path.join(tmpdir, self.db_name)
        
        return tmpdir, prefix
