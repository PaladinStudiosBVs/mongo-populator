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

from populator import SSHPopulator
from populator.source import MongoSource


class SSHSource(SSHPopulator, MongoSource):
    def __init__(self, ssh_host=None, ssh_user=None, ssh_password=None):
        SSHPopulator.__init__(ssh_host=ssh_host, ssh_user=ssh_user, ssh_password=ssh_password)
        
    def get_dump_dir(self):
        mongo_data_dir = os.path.dirname(os.path.abspath(__file__)) + "/../db"
        self.dump_dir = mongo_data_dir + "/dump/"
    
        os.mkdir(self.dump_dir)
        for p in prefixes:
            for f in glob.glob(f"{mongo_data_dir}/{p}*"):
                shutil.copy(f, self.dump_dir)
