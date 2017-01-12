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

import glob
import os
import shutil

from populator.source import MongoPopulator


class MongoLocalPopulator(MongoPopulator):
    """
    Populates your local Mongo database from a local dump. This
    local dump is located in <pangaea-db-dir>/db.
    """
    def create_dump_dir(self):
        prefixes = [
            "config_groups",
            "game_configs",
            "games",
            "mirage_config",
            "adminusers",
            "keystone_users",
            "users"
        ]

        mongo_data_dir = os.path.dirname(os.path.abspath(__file__)) + "/../db"
        self.dump_dir = mongo_data_dir + "/dump/"

        os.mkdir(self.dump_dir)
        for p in prefixes:
            for f in glob.glob(f"{mongo_data_dir}/{p}*"):
                shutil.copy(f, self.dump_dir)
