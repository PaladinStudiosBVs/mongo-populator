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

import subprocess
from subprocess import CalledProcessError

from populator import MongoConfig
from populator.destination import MongoDestination


class LocalDestination(MongoConfig, MongoDestination):
    def __init__(self, db_name, source):
        MongoConfig.__init__(self, db_name)
        MongoDestination.__init__(self, source)
        
    def _populate(self):
        try:
            subprocess.run(
                self.get_restore_str() % self.dump_dir,
                stderr=subprocess.STDOUT,
                shell=True
            )
            return 0
        except CalledProcessError as e:
            print(e.output)
            return e.returncode
