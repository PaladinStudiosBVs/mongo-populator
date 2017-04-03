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

import subprocess
from subprocess import CalledProcessError

from populator.destination import MongoDestination
from populator.utils.common import info


class DirectDestination(MongoDestination):
    def __init__(self, db_name=None, db_host=None, db_user=None, db_password=None,
                 drop_db=True, direct_use_ssl=False, db_restore_indexes=False, source=None,
                 db_auth=None):
        MongoDestination.__init__(
            self,
            source=source,
            db_name=db_name,
            host=db_host,
            db_user=db_user,
            db_password=db_password,
            auth_db=db_auth,
            drop_db=drop_db,
            use_ssl=direct_use_ssl,
            db_restore_indexes=db_restore_indexes
        )

    def _populate(self):
        try:
            info(self.get_restore_str())
            subprocess.run(
                self.get_restore_str() % self.dump_dir,
                stderr=subprocess.STDOUT,
                shell=True
            )
            return 0
        except CalledProcessError as e:
            print(e.output)
            return e.returncode
