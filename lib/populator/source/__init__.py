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
import shutil
import subprocess

from populator.utils.common import info, die


def check_for_mongo_tools():
    """
    Make sure that at least we have `mongorestore`
    command line tool.
    """
    info("Checking for Mongo Tools...")

    mongo_exists = subprocess.check_output(
        "which mongorestore; exit 0",
        encoding="utf-8",
        stderr=subprocess.STDOUT,
        shell=True
    ).strip() != ""

    if not mongo_exists:
        die("Perhaps you need to install Mongo Tools?")


class MongoPopulator(object):
    DB_NAME = "pangaea"

    def __init__(self):
        self.dump_dir = None

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

    def create_dump_dir(self):
        """
        Creates a directory with the dump data
        """
        raise Exception("Not implemented")

    def populate(self):
        """
        Where the actual population takes place.
        """
        info("Creating data dump directory...")
        self.create_dump_dir()

        info("Populating database...")

        subprocess.check_output(
            "mongorestore --drop --db {} {}".format(self.DB_NAME, self.dump_dir),
            stderr=subprocess.STDOUT,
            shell=True
        )

        info("Done! Just cleaning whatever mess we've made...")
        shutil.rmtree(self.dump_dir)
