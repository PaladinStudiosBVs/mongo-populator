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

from abc import ABCMeta, abstractmethod

from populator import MongoConfig, PopulatorCtxManager


class MongoDestination(MongoConfig, PopulatorCtxManager, metaclass=ABCMeta):
    def __init__(self, source, db_name=None, db_user=None, db_password=None, drop_db=True, db_restore_indexes=False):
        """
        :type source: populator.source.MongoSource
        :param source:
        """
        MongoConfig.__init__(
            self,
            db_name=db_name,
            db_user=db_user,
            db_password=db_password,
            drop_db=drop_db,
            db_restore_indexes=db_restore_indexes
        )
        self.source = source
        self.dump_dir = None
        self.prefix = None
        
    @abstractmethod
    def _populate(self):
        pass
    
    def run(self):
        self.dump_dir, self.prefix = self.source.get_dump_dir()
        self._populate()
