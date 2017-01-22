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

from abc import ABCMeta, abstractmethod

from populator import PopulatorCtxManager


class MongoSource(PopulatorCtxManager, metaclass=ABCMeta):
    def __init__(self, tmp_dir=None, is_dockerized=False, docker_container_name=None):
        self.tmp_dir = tmp_dir
        self.is_dockerized = is_dockerized
        self.container_name = docker_container_name
        
    @abstractmethod
    def get_dump_dir(self):
        """
        :rtype: tuple[str, str]
        :return:
        """
        pass
