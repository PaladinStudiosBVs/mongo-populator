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

import os
import subprocess

from populator.utils.common import die, info
from populator.utils.text import to_text


def get_dump_from_container(db_name, dump_str, host_dump_dir, container_name, ssh_client=None):
    """
    :type ssh_client: paramiko.SSHClient
    :param ssh_client:
    :type db_name: str
    :param db_name:
    :type dump_str: str
    :param dump_str:
    :type host_dump_dir: str
    :param host_dump_dir:
    :type container_name: str
    :param container_name:
    """
    cmd = 'docker exec -i {} {}'.format(container_name, dump_str)
    info('Creating dump inside container: {}'.format(cmd), color='purple')
    
    if ssh_client:
        _, stdout, stderr = ssh_client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            info('Dump successfully created inside container.', color='green')
        else:
            die(to_text(stdout.channel.recv_stderr(65536)))
    else:
        mongo_dump = subprocess.check_output(
            cmd,
            encoding="utf-8",
            stderr=subprocess.STDOUT,
            shell=True
        )
    
        info(mongo_dump, color='dark gray')
    
    # Copy dump from container to remote host
    cmd = 'docker cp {}:{} {}'.format(
        container_name,
        os.path.join(host_dump_dir, db_name),
        host_dump_dir
    )
    info(
        'Copying dump from container to host: {}'.format(cmd),
        color='purple'
    )
    
    if ssh_client:
        _, stdout, _ = ssh_client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            info('Dump successfully extracted from container.', color='green')
        else:
            die('Problems extracting dump from container.')
    else:
        mongo_dump = subprocess.check_output(
            cmd,
            encoding="utf-8",
            stderr=subprocess.STDOUT,
            shell=True
        )
    
        info(mongo_dump, color='dark gray')
