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
