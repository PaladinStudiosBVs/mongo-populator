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
import subprocess

from populator import MongoConfig
from populator.source import MongoSource
from populator.utils.common import info
from populator.utils.docker import get_dump_from_container


class LocalDumpSource(object):
    def __init__(self, dump_dir, **kwargs):
        self.source_dump_dir = dump_dir

    def get_dump_dir(self):
        return self.source_dump_dir, None


class DirectSource(MongoSource):
    def __init__(self, db_name=None, db_host=None, db_user=None, db_password=None,
                 tmp_dir=None, direct_use_ssl=False, is_dockerized=False, docker_container_name=None,
                 db_auth=None, exclude=None, collection=None):
        MongoSource.__init__(
            self,
            db_name=db_name,
            host=db_host,
            db_user=db_user,
            db_password=db_password,
            auth_db=db_auth,
            use_ssl=direct_use_ssl,
            exclude=exclude,
            collection=collection,
            tmp_dir=tmp_dir,
            is_dockerized=is_dockerized,
            docker_container_name=docker_container_name
        )

    def get_dump_dir(self):
        # Create local dump directory
        prefix = datetime.now().strftime('%Y%m%d-%H%M%S')
        tmpdir = os.path.join(self.tmp_dir, prefix)
        info('Creating local dump dir: {}'.format(tmpdir), color='purple')
        os.makedirs(tmpdir)

        dump_str = self.get_dump_str() % tmpdir

        # Is our local database running inside Docker?
        if self.is_dockerized:
            get_dump_from_container(
                self.db_name,
                dump_str,
                tmpdir,
                self.container_name
            )
        else:
            # If not, just dump the database to the previously
            # created directory
            mongo_dump = subprocess.check_output(
                dump_str,
                encoding="utf-8",
                stderr=subprocess.STDOUT,
                shell=True
            )

            info(mongo_dump, color='dark gray')

        tmpdir = os.path.join(tmpdir, self.db_name)

        return tmpdir, prefix
