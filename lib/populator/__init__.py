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

import boto3
import paramiko
from paramiko.client import SSHClient
from scp import SCPClient

from populator.utils.common import info
from populator.utils.mongo import check_for_mongo_tools


class MongoConfig(object):
    def __init__(self, db_name, db_user=None, db_password=None, drop_db=True):
        """
        :type db_name: str
        :param db_name:
        :type db_user: str
        :param db_user:
        :type db_password: str
        :param db_password:
        :type drop_db: bool
        :param drop_db:
        """
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.drop_db = drop_db
        
    def _get_cmd_str(self, cmd):
        """
        
        :param cmd:
        :return:
        """
        user = '-u {}'.format(self.db_user) if self.db_user else ''
        password = '-p {}'.format(self.db_password) if self.db_password else ''
        db = '--db {}'.format(self.db_name)
        
        if cmd == 'dump':
            return 'mongodump {} {} --out %s {}'.format(user, password, db)
        elif cmd == 'restore':
            drop_db = '--drop' if self.drop_db else ''
            return 'mongorestore {} {} {} {} %s'.format(user, password, drop_db, db)
        
        # todo - raise proper exception
        
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
            
        self.scp_client = SCPClient(self.ssh_client.get_transport())
        
    def __enter_extra_init(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scp_client.close()
        self.ssh_client.close()
        
        
class AmazonS3Populator(object):
    """ todo """
    def __init__(self, bucket, prefix=None, aws_access_key_id=None, aws_secret_access_key=None):
        """
        todo
        :type bucket: str
        :param bucket:
        :type prefix: str
        :param prefix:
        :type aws_access_key_id: str
        :param aws_access_key_id:
        :type aws_secret_access_key: str
        :param aws_secret_access_key:
        """
        self.client = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket = self.client.Bucket(bucket)
