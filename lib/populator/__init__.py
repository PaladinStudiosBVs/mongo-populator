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

import boto3
import paramiko
from paramiko.client import SSHClient
from scp import SCPClient

from populator.errors import MongoPopulatorUnknownCmdError
from populator.utils.common import info
from populator.utils.mongo import check_for_mongo_tools


class MongoConfig(object):
    def __init__(self, db_name, host=None, db_user=None, db_password=None,
                 use_ssl=False, db_restore_indexes=False, drop_db=True,
                 auth_db=None):
        """
        :type db_name: str
        :param db_name:
        :type host: str
        :param host:
        :type db_user: str
        :param db_user:
        :type db_password: str
        :param db_password:
        :type use_ssl: bool
        :param use_ssl:
        :type db_restore_indexes: bool
        :param db_restore_indexes:
        :type drop_db: bool
        :param drop_db:
        :type auth_db: str
        :param auth_db:
        """
        self.db_name = db_name
        self.host = host
        self.db_user = db_user
        self.db_password = db_password
        self.db_restore_indexes = db_restore_indexes
        self.use_ssl = use_ssl
        self.drop_db = drop_db
        self.auth_db = auth_db

    def _get_cmd_str(self, cmd):
        """
        :param cmd:
        :return:
        """
        common_opts = ''
        if self.db_user:
            common_opts += '-u {} '.format(self.db_user)
        if self.db_password:
            common_opts += '-p {} '.format(self.db_password)
        common_opts += '--db {} '.format(self.db_name)
        if self.use_ssl:
            common_opts += '--ssl '
        if self.host:
            common_opts += '-h {} '.format(self.host)
        if self.auth_db:
            common_opts += '--authenticationDatabase {}'.format(self.auth_db)

        if cmd == 'dump':
            return 'mongodump {} --out %s'.format(common_opts)

        elif cmd == 'restore':
            drop_db = '--drop' if self.drop_db else ''
            restore_indexes = '--noIndexRestore' if not self.db_restore_indexes else ''

            return 'mongorestore {} {} {} %s'.format(
                common_opts, restore_indexes, drop_db
            )

        else:
            raise MongoPopulatorUnknownCmdError()

    def get_dump_str(self):
        return self._get_cmd_str('dump')

    def get_restore_str(self):
        return self._get_cmd_str('restore')


class PopulatorCtxManager(object):
    def __enter_extra_init(self):
        """
        Override if you want to do extra stuff when
        you enter the context.
        """
        pass

    def __enter__(self):
        check_for_mongo_tools()
        info("Performing extra pre-population tasks...", color='blue')
        self.__enter_extra_init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class SSHPopulator(object):
    """
    Both source and destination populators should inherit from this class if they are
    to use SSH to communicate with the database.
    """
    def __init__(self, ssh_host=None, ssh_user=None, ssh_password=None, ssh_key_file=None):
        """
        :type ssh_host: str
        :param ssh_host: Hostname we're connecting to
        :type ssh_user: str
        :param ssh_user:
        :type ssh_password: str
        :param ssh_password:
        :type ssh_key_file: str
        :param ssh_key_file: Full path to an identity file.
        """
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(**{
            'hostname': ssh_host,
            'username': ssh_user,
            'password': ssh_password,
            'key_filename': ssh_key_file
        })

        self.scp_client = SCPClient(self.ssh_client.get_transport(), socket_timeout=10.0)

    def __enter_extra_init(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scp_client.close()
        self.ssh_client.close()


class AmazonS3Populator(object):
    """ todo """
    def __init__(self, bucket, s3_prefix=None, aws_access_key_id=None, aws_secret_access_key=None,
                 region_name=None):
        """
        todo
        :type bucket: str
        :param bucket:
        :type s3_prefix: str
        :param s3_prefix:
        :type aws_access_key_id: str
        :param aws_access_key_id:
        :type aws_secret_access_key: str
        :param aws_secret_access_key:
        :type region_name: str
        :param region_name:
        """
        self.client = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.bucket = self.client.Bucket(bucket)
        self.s3_prefix = s3_prefix
