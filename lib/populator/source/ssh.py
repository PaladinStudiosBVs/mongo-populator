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

from populator.source import MongoPopulator


class MongoSSHPopulator(MongoPopulator):
    def __init__(self, ssh_host, mongo_credentials_file=None):
        super().__init__()
        self.mongo_credentials_file = mongo_credentials_file \
            or ".local/.env.dev"
        self.host = ssh_host
        self.client = SSHClient()

    def __enter_extra_init(self):
        self.client.connect(self.host)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_dump_dir(self):
        # The credentials file contains 3 key/value pairs:
        # DB_USER_READWRITE_PASS, CACHE_REDIS_PASS and DB_PASS
        with open(self.mongo_credentials_file) as f:
            d = dict([line.strip().split("=") for line in f])
