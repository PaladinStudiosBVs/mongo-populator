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

from test.unit import CLITestCase


class TestCLI(CLITestCase):
    def test_cli_flags_prevail(self):
        TestCLI.populate_environment_variables()
        from populator.cli import CLI
        c = CLI([
            'script_name',
            '--source-db-name', 'test_db',
            '--source-db-user', 'test_user',
            '--source-db-password', 'test_password',
            '--source-use-local-db',
        ])
        c.parse()
        
        self.assertEqual(c.options['source_db_name'], 'test_db')
        self.assertEqual(c.options['source_db_user'], 'test_user')
        self.assertEqual(c.options['source_db_password'], 'test_password')
        self.assertEqual(c.options['source_use_local_db'], True)
        
        kwargs = c._build_kwargs(['source_db'], 'source_')
        self.assertDictEqual(
            kwargs,
            {'db_name': 'test_db', 'db_user': 'test_user', 'db_password': 'test_password'}
        )
