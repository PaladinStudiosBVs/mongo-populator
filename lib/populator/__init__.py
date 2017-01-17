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

from paramiko.client import SSHClient

from populator.utils.mongo import check_for_mongo_tools
from populator.utils.common import info


class MongoConfig(object):
    def __init__(self, db_name):
        self.db_name = db_name


class PopulatorCtxManager(object):
    def __enter_extra_init(self):
        """
        Override if you want to do extra stuff when
        you enter the context.
        """
        pass
    
    def __enter__(self):
        check_for_mongo_tools()
        info("Performing extra pre-population tasks...")
        self.__enter_extra_init()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    

class SSHPopulator(object):
    def __init__(self, ssh_host=None, ssh_user=None, ssh_password=None):
        self.client = SSHClient()
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        
    def __enter_extra_init(self):
        self.client.connect(self.ssh_host)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
