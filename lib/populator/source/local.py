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

from populator import MongoConfig
from populator.source import MongoSource


class LocalDumpSource(MongoSource):
    def __init__(self, dump_dir):
        self.source_dump_dir = dump_dir
        
    def get_dump_dir(self):
        return self.source_dump_dir
    

class LocalDbSource(MongoConfig, MongoSource):
    def __init__(self, db_name):
        MongoConfig.__init__(self, db_name)
        
    def get_dump_dir(self):
        # todo
        return ''
