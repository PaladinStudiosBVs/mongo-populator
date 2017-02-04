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

import sys
import nose
import os


def run_all(argv=None):
    if argv is None:
        argv = [
            'nosetests', '--with-xunit',
            '--with-xcoverage', '--cover-package=populator', '--cover-erase',
            '--logging-filter=mongo-populator', '--logging-level=DEBUG',
            '--verbose',
        ]

    os.environ['MONGO_POPULATOR_CONFIG'] = os.path.join(
        os.path.dirname(__file__), 'mongo-populator.cfg'
    )

    nose.run_exit(
        argv=argv,
        defaultTest=os.path.abspath(os.path.dirname(__file__))
    )

    del os.environ['MONGO_POPULATOR_CONFIG']


if __name__ == '__main__':
    run_all(sys.argv)
