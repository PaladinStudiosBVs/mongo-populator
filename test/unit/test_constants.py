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

import unittest

import populator.constants as C


class TestConstants(unittest.TestCase):
    def test_make_boolean(self):
        self.assertTrue(C.make_boolean('1'))
        self.assertTrue(C.make_boolean('yes'))
        self.assertTrue(C.make_boolean('on'))
        self.assertTrue(C.make_boolean('true'))
        self.assertTrue(C.make_boolean('t'))
        self.assertTrue(C.make_boolean('y'))
